"""Kleine Stichprobe eines Ursprungs mit robots.txt und festen Obergrenzen."""
from collections import deque
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from .network import AGENT, Fetcher, FetchError, normalize_url, origin
from .audit import analyze, add_site_findings


def crawl(url, max_pages=10, fetcher=None):
    if not 1 <= max_pages <= 50:
        raise ValueError("Seitenlimit muss zwischen 1 und 50 liegen")
    start = normalize_url(url)
    base = origin(start)
    fetcher = fetcher or Fetcher(max_requests=2 * max_pages + 10)
    report = new_report("crawl")
    report["scope"] = {"start_url": start, "origin": base, "max_pages": max_pages,
                       "javascript": False, "query_urls_followed": False}
    try:
        response = fetcher.fetch(base + "/robots.txt", allowed_origin=base)
        if response.status in (404, 410):
            lines = []
        elif response.status == 200:
            lines = response.text().splitlines()
        else:
            raise FetchError(f"robots.txt nicht verlässlich abrufbar (HTTP {response.status})")
    except FetchError as exc:
        report["errors"].append({"url": base + "/robots.txt", "message": str(exc)})
        return report
    robots = RobotFileParser()
    robots.parse(lines)
    wait = robots.crawl_delay(AGENT) or robots.crawl_delay("*") or 0
    if hasattr(fetcher, "delay"):
        fetcher.delay = max(fetcher.delay, wait)
    report["discovered_sitemaps"] = robots.site_maps() or []
    queue, seen = deque([start]), set()
    # Das Kandidatenlimit begrenzt auch Seiten mit sehr vielen Links.
    while queue and len(seen) < max_pages:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        if not robots.can_fetch(AGENT, current):
            report["skipped"].append({"url": current, "reason": "robots.txt"})
            continue
        # Weiterleitungsziele werden vor ihrem Abruf gegen robots.txt geprüft.
        try:
            response = fetcher.fetch(current, allowed_origin=base,
                                     permitted=lambda target: robots.can_fetch(AGENT, target))
            if response.status in (429, 503):
                report["errors"].append({"url": current, "message": f"HTTP {response.status}: Prüfung zum Schutz des Servers gestoppt"})
                report["truncated"] = True
                break
            if response.url != current and not robots.can_fetch(AGENT, response.url):
                raise FetchError("Weiterleitungsziel ist durch robots.txt gesperrt")
            if "text/html" not in response.headers.get("content-type", "").lower() and "application/xhtml+xml" not in response.headers.get("content-type", "").lower():
                if response.status >= 400:
                    page, _ = analyze(response.url, "", response.status, response.headers)
                    page["findings"] = [item for item in page["findings"] if item["rule"] == "http-error"]
                    report["pages"].append(page)
                else:
                    report["skipped"].append({"url": current, "reason": "Kein HTML"})
                continue
            if any(page["url"] == response.url for page in report["pages"]):
                continue
            page, links = analyze(response.url, response.text(), response.status, response.headers)
            report["pages"].append(page)
            for link in links:
                if len(queue) + len(seen) >= max_pages * 10:
                    break
                try:
                    candidate = normalize_url(link)
                    if origin(candidate) == base and not urlsplit(candidate).query and candidate not in seen:
                        queue.append(candidate)
                except FetchError:
                    continue
        except FetchError as exc:
            report["errors"].append({"url": current, "message": str(exc)})
    report["truncated"] = report["truncated"] or bool(queue)
    report["requests"] = getattr(fetcher, "requests", None)
    add_site_findings(report["pages"])
    return report


def new_report(mode):
    return {"schema_version": "0.1.0", "tool_version": "0.1.0", "mode": mode,
            "checked_at": datetime.now(timezone.utc).isoformat(), "pages": [],
            "errors": [], "skipped": [], "truncated": False,
            "limitations": ["Nur Quell-HTML, kein JavaScript und keine vollständige Website-Abdeckung.",
              "Keine Messung von Rankings, Suchvolumen, tatsächlicher Indexierung oder Core Web Vitals.",
              "Canonical-Ziele, externe Links und Sitemap-Inhalte werden nicht separat abgerufen.",
              "JSON-LD wird nur syntaktisch geprüft; keine Garantie für Rich Results."]}
