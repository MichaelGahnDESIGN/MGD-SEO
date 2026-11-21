"""Firecrawl-Anbindung mit nachgebauten Antworten, ohne echte Abrufe."""
import io
import json
import os
import tempfile
import unittest
import urllib.error
from unittest.mock import patch
from mgd_seo.firecrawl import Cache, Client, FirecrawlError, endpoint, render_crawl
from mgd_seo.network import Response
from mgd_seo.report import compact

HTML = '<html lang="de"><title>{t}</title><meta name="description" content="x"><h1>{t}</h1><a href="/b">B</a><a href="/privat">P</a><a href="/c?q=1">Q</a><a href="https://fremd.example/">F</a></html>'


class FakeRobots:
    def __init__(self, text="User-agent: *\nDisallow: /privat"):
        self.text, self.requests = text, 0
    def fetch(self, url, **kwargs):
        self.requests += 1
        return Response(url, 200, {"content-type": "text/plain"}, self.text.encode())


class FakeClient:
    def __init__(self, fail=False, fail_after=None, redirects=None, status=200):
        self.urls, self.calls, self.fail = [], 0, fail
        self.fail_after, self.redirects, self.status = fail_after, redirects or {}, status
    def scrape(self, url):
        self.calls += 1
        self.urls.append(url)
        if self.fail or (self.fail_after is not None and self.calls > self.fail_after):
            raise FirecrawlError("Firecrawl nicht erreichbar: URLError")
        final = self.redirects.get(url, url)
        return final, self.status, HTML.format(t="Seite " + final[-1])


class FakeOpener:
    def __init__(self, body=None, error=None):
        self.body, self.error, self.request = body, error, None
    def open(self, request, timeout):
        self.request = request
        if self.error:
            raise self.error
        return io.BytesIO(json.dumps(self.body).encode())


class EndpointTests(unittest.TestCase):
    def test_default_is_local_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(endpoint(), ("http://localhost:3002", "", "lokal"))

    def test_cloud_needs_key(self):
        with patch.dict(os.environ, {"MGD_SEO_FIRECRAWL_URL": "https://api.firecrawl.dev"}, clear=True):
            with self.assertRaises(FirecrawlError):
                endpoint()
        with patch.dict(os.environ, {"MGD_SEO_FIRECRAWL_URL": "https://api.firecrawl.dev", "FIRECRAWL_API_KEY": "fc-test"}, clear=True):
            self.assertEqual(endpoint()[2], "cloud")

    def test_cloud_key_never_sent_to_localhost(self):
        with patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fc-geheim"}, clear=True):
            self.assertEqual(endpoint()[1], "")

    def test_foreign_endpoints_rejected(self):
        for bad in ("https://evil.example", "http://api.firecrawl.dev", "http://user:pw@localhost:3002", "ftp://localhost"):
            with patch.dict(os.environ, {"MGD_SEO_FIRECRAWL_URL": bad}, clear=True):
                with self.assertRaises(FirecrawlError):
                    endpoint()


class ClientTests(unittest.TestCase):
    def test_scrape_requests_only_raw_html_and_sends_key(self):
        opener = FakeOpener({"success": True, "data": {"rawHtml": "<title>A</title>", "metadata": {"statusCode": 404, "url": "https://example.org/a"}}})
        client = Client("http://localhost:3002", "fc-geheim", opener=opener)
        self.assertEqual(client.scrape("https://example.org/a"), ("https://example.org/a", 404, "<title>A</title>"))
        sent = json.loads(opener.request.data)
        self.assertEqual(sent["formats"], ["rawHtml"])
        self.assertEqual(opener.request.full_url, "http://localhost:3002/v2/scrape")
        self.assertEqual(opener.request.get_header("Authorization"), "Bearer fc-geheim")

    def test_errors_never_contain_key(self):
        error = urllib.error.HTTPError("http://localhost:3002/v2/scrape", 401, "fc-geheim", {}, None)
        client = Client("http://localhost:3002", "fc-geheim", opener=FakeOpener(error=error))
        with self.assertRaises(FirecrawlError) as caught:
            client.scrape("https://example.org/")
        self.assertNotIn("fc-geheim", str(caught.exception))

    def test_unsuccessful_or_missing_html(self):
        for body in ({"success": False, "error": "x"}, {"success": True, "data": {}}):
            with self.assertRaises(FirecrawlError):
                Client("http://localhost:3002", opener=FakeOpener(body)).scrape("https://example.org/")


class RenderCrawlTests(unittest.TestCase):
    def test_scope_robots_query_and_foreign_links(self):
        client = FakeClient()
        report = render_crawl("https://example.org/", 5, client=client, fetcher=FakeRobots(), check_dns=False)
        self.assertEqual(client.urls, ["https://example.org/", "https://example.org/b"])
        self.assertEqual(report["skipped"][0]["reason"], "robots.txt")
        self.assertTrue(report["scope"]["javascript"])
        self.assertEqual(report["requests"], 2)

    def test_limit_and_stop_when_firecrawl_down(self):
        report = render_crawl("https://example.org/", 1, client=FakeClient(), fetcher=FakeRobots(), check_dns=False)
        self.assertEqual(len(report["pages"]), 1)
        self.assertTrue(report["truncated"])
        client = FakeClient(fail=True)
        report = render_crawl("https://example.org/", 5, client=client, fetcher=FakeRobots(), check_dns=False)
        self.assertEqual(client.calls, 1)
        self.assertEqual(report["pages"], [])
        self.assertTrue(report["errors"])

    def test_private_target_blocked_before_firecrawl(self):
        client = FakeClient()
        with self.assertRaises(Exception):
            render_crawl("http://localhost/", 1, client=client, fetcher=FakeRobots())
        self.assertEqual(client.calls, 0)

    def test_page_limit_range(self):
        with self.assertRaises(ValueError):
            render_crawl("https://example.org/", 26, client=FakeClient(), fetcher=FakeRobots(), check_dns=False)

    def test_cache_saves_second_call(self):
        with tempfile.TemporaryDirectory() as folder:
            first = FakeClient()
            render_crawl("https://example.org/", 2, client=first, fetcher=FakeRobots(), cache=Cache(folder), check_dns=False)
            second = FakeClient()
            report = render_crawl("https://example.org/", 2, client=second, fetcher=FakeRobots(), cache=Cache(folder), check_dns=False)
            self.assertEqual(second.calls, 0)
            self.assertEqual(report["cache_hits"], 2)
            self.assertEqual(len(report["pages"]), 2)

    def test_redirect_target_checked_against_robots(self):
        client = FakeClient(redirects={"https://example.org/b": "https://example.org/privat"})
        report = render_crawl("https://example.org/", 5, client=client, fetcher=FakeRobots(), check_dns=False)
        self.assertNotIn("https://example.org/privat", [page["url"] for page in report["pages"]])
        self.assertTrue(any("Weiterleitungsziel" in item["reason"] for item in report["skipped"]))

    def test_stops_on_overload_and_on_firecrawl_error_later(self):
        report = render_crawl("https://example.org/", 5, client=FakeClient(status=429), fetcher=FakeRobots(), check_dns=False)
        self.assertEqual(report["pages"], [])
        self.assertTrue(report["truncated"])
        client = FakeClient(fail_after=1)
        report = render_crawl("https://example.org/", 5, client=client, fetcher=FakeRobots(), check_dns=False)
        self.assertEqual(client.calls, 2)
        self.assertEqual(len(report["pages"]), 1)

    def test_cache_ignores_broken_files_and_error_pages(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = Cache(folder)
            cache.put("https://example.org/x", ("https://example.org/x", 503, "<p>weg</p>"))
            self.assertIsNone(cache.get("https://example.org/x"))
            cache.put("https://example.org/y", ("https://example.org/y", 200, "<p>ok</p>"))
            file = next(iter(os.scandir(folder))).path
            data = json.loads(open(file, encoding="utf-8").read())
            data["html"] = 1
            open(file, "w", encoding="utf-8").write(json.dumps(data))
            self.assertIsNone(cache.get("https://example.org/y"))

    def test_compact_report_is_short(self):
        report = render_crawl("https://example.org/", 2, client=FakeClient(), fetcher=FakeRobots(), check_dns=False)
        text = compact(report)
        self.assertLess(len(text), 800)
        self.assertNotIn("<html", text)
        self.assertIn("Seiten 2", text)


if __name__ == "__main__":
    unittest.main()
