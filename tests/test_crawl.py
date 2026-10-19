"""Stichproben-Crawl mit festgelegten Antworten statt öffentlichen Abrufen."""
import unittest
from mgd_seo.crawl import crawl
from mgd_seo.network import Response, FetchError

HTML='<html lang="de"><title>Seite</title><h1>Seite</h1><a href="/next">Weiter</a><a href="/private">Privat</a><a href="/filter?q=x">Filter</a><a href="https://other.example/">Extern</a></html>'
class FakeFetcher:
    def __init__(self, robots="User-agent: *\nDisallow: /private", code=200):
        self.robots, self.code, self.requests, self.urls = robots, code, 0, []
    def fetch(self,url,**kwargs):
        self.requests += 1
        self.urls.append(url)
        if url.endswith("robots.txt"):
            if self.robots is None: raise FetchError("DNS fehlgeschlagen")
            return Response(url,200,{"content-type":"text/plain"},self.robots.encode())
        return Response(url,self.code,{"content-type":"text/html; charset=utf-8"},HTML.encode())

class CrawlTests(unittest.TestCase):
    def test_scope_robots_and_duplicates(self):
        fetcher=FakeFetcher()
        report=crawl("https://example.org/",max_pages=10,fetcher=fetcher)
        self.assertEqual(len(report["pages"]),2)
        self.assertTrue(report["skipped"])
        self.assertFalse(any("?" in url or "other.example" in url or url.endswith("private") for url in fetcher.urls))
        self.assertTrue(all(any(f["rule"]=="duplicate-title" for f in page["findings"]) for page in report["pages"]))

    def test_missing_robots_stops(self):
        report=crawl("https://example.org/",fetcher=FakeFetcher(robots=None))
        self.assertEqual(report["pages"],[])
        self.assertEqual(len(report["errors"]),1)

    def test_limit_and_truncated(self):
        report=crawl("https://example.org/",max_pages=1,fetcher=FakeFetcher())
        self.assertEqual(len(report["pages"]),1)
        self.assertTrue(report["truncated"])

    def test_overload_stops(self):
        for status in (429,503):
            report=crawl("https://example.org/",fetcher=FakeFetcher(code=status))
            self.assertEqual(report["pages"],[])
            self.assertTrue(report["errors"])

    def test_non_html_http_error_is_reported(self):
        class ErrorFetcher(FakeFetcher):
            def fetch(self,url,**kwargs):
                if url.endswith("robots.txt"): return super().fetch(url,**kwargs)
                return Response(url,404,{"content-type":"text/plain"},b"Not found")
        report=crawl("https://example.org/",fetcher=ErrorFetcher())
        self.assertEqual(report["pages"][0]["http_status"],404)
        self.assertEqual([item["rule"] for item in report["pages"][0]["findings"]],["http-error"])

    def test_limits_validate(self):
        for count in (0,51,-1):
            with self.assertRaises(ValueError): crawl("https://example.org/",count,FakeFetcher())

if __name__ == "__main__": unittest.main()
