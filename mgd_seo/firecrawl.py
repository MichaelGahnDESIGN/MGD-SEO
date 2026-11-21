"""Optionale Firecrawl-Anbindung für gerenderte Seiten (JavaScript).

Token sparen: Firecrawl liefert das HTML, ausgewertet wird lokal mit audit.py.
Der KI geht nur der kurze Bericht zu, nie das ganze HTML.
Kostenlos: eigener Firecrawl per Docker (Standard http://localhost:3002, kein Schlüssel)
oder Firecrawl-Cloud mit Gratis-Kontingent und eigenem Schlüssel in FIRECRAWL_API_KEY.
"""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from .audit import add_site_findings, analyze
from .crawl import load_robots, new_report
from .network import AGENT, FetchError, Fetcher, normalize_url, origin, public_addresses

DEFAULT_URL = "http://localhost:3002"
CLOUD_HOST = "api.firecrawl.dev"
LOCAL_HOSTS = ("localhost", "127.0.0.1", "::1")
MAX_RESPONSE = 5_000_000
MAX_HTML = 2_000_000
CACHE_SECONDS = 24 * 3600
MAX_PAGES = 25
MAX_SECONDS = 300
MIN_DELAY = 0.5


class FirecrawlError(FetchError):
    """Firecrawl nicht erreichbar, falsch eingestellt oder Antwort unbrauchbar."""


def endpoint():
    # nur eigener Rechner oder offizielle Cloud, sonst könnte man Daten umleiten
    base = os.environ.get("MGD_SEO_FIRECRAWL_URL", DEFAULT_URL).rstrip("/")
    p = urlsplit(base)
    host = (p.hostname or "").lower()
    local = p.scheme in ("http", "https") and host in LOCAL_HOSTS
    cloud = p.scheme == "https" and host == CLOUD_HOST and p.port in (None, 443)
    if not (local or cloud) or p.username or p.password or p.query or p.fragment:
        raise FirecrawlError("MGD_SEO_FIRECRAWL_URL: nur http://localhost:<port> oder https://api.firecrawl.dev erlaubt")
    key = os.environ.get("FIRECRAWL_API_KEY", "").strip()
    if cloud and not key:
        raise FirecrawlError("Firecrawl-Cloud braucht FIRECRAWL_API_KEY (Gratis-Konto); eigener Docker-Firecrawl braucht keinen")
    # Cloud-Key nie an localhost schicken (da lauscht evtl. was anderes, und nur http)
    return base, key if cloud else "", "cloud" if cloud else "lokal"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Client:
    """Kleiner HTTP-Client ohne Proxy und ohne Weiterleitungen."""
    def __init__(self, base=None, key=None, timeout=70, opener=None):
        if base is None:
            base, key, _ = endpoint()
        self.base, self.key, self.timeout = base, key or "", timeout
        self.opener = opener or urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
        self.calls = 0

    def post(self, path, payload):
        headers = {"Content-Type": "application/json", "User-Agent": AGENT}
        if self.key:
            headers["Authorization"] = "Bearer " + self.key
        request = urllib.request.Request(self.base + path, data=json.dumps(payload).encode(), headers=headers, method="POST")
        self.calls += 1
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                body = response.read(MAX_RESPONSE + 1)
        except urllib.error.HTTPError as exc:
            # Schlüssel nie in Fehlermeldungen
            raise FirecrawlError(f"Firecrawl antwortet mit HTTP {exc.code}") from exc
        except (OSError, ValueError) as exc:
            raise FirecrawlError("Firecrawl nicht erreichbar: " + type(exc).__name__) from exc
        if len(body) > MAX_RESPONSE:
            raise FirecrawlError("Firecrawl-Antwort überschreitet das Größenlimit")
        try:
            data = json.loads(body)
        except ValueError as exc:
            raise FirecrawlError("Firecrawl-Antwort ist kein JSON") from exc
        if not isinstance(data, dict) or data.get("success") is not True:
            raise FirecrawlError("Firecrawl meldet einen Fehler")
        return data

    def scrape(self, url):
        # rawHtml = Seitenquelltext wie geliefert, nur das braucht audit.py
        data = self.post("/v2/scrape", {"url": url, "formats": ["rawHtml"], "onlyMainContent": False,
                                       "blockAds": True, "timeout": 30000, "maxAge": 172800000})
        page = data.get("data") or {}
        meta = page.get("metadata") or {}
        html = page.get("rawHtml")
        if not isinstance(html, str):
            raise FirecrawlError("Firecrawl lieferte kein HTML")
        status = meta.get("statusCode") if isinstance(meta.get("statusCode"), int) else 200
        final = meta.get("url") if isinstance(meta.get("url"), str) else url
        return final, status, html[:MAX_HTML]


class Cache:
    """Lokaler Zwischenspeicher, damit dieselbe Seite nicht nochmal Credits kostet."""
    def __init__(self, folder, seconds=CACHE_SECONDS):
        self.folder, self.seconds = Path(folder), seconds

    def _file(self, url):
        return self.folder / (hashlib.sha256(url.encode()).hexdigest() + ".json")

    def get(self, url):
        try:
            item = json.loads(self._file(url).read_text(encoding="utf-8"))
            final, status, html = item["final"], item["status"], item["html"]
            # kaputte oder manipulierte Datei = einfach neu holen
            if (time.time() - item["time"] <= self.seconds and item["url"] == url and isinstance(final, str)
                    and isinstance(status, int) and isinstance(html, str) and status < 400):
                return final, status, html[:MAX_HTML]
        except (OSError, ValueError, KeyError, TypeError):
            pass
        return None

    def put(self, url, result):
        final, status, html = result
        if status >= 400:
            return  # Fehlerseiten nicht merken, sonst 24 h lang falscher Befund
        try:
            self.folder.mkdir(parents=True, exist_ok=True)
            self._file(url).write_text(json.dumps({"url": url, "time": time.time(), "final": final,
                                                   "status": status, "html": html}), encoding="utf-8")
        except OSError:
            pass  # Cache kaputt/voll ist egal, Bericht geht vor


def _same_site(url, base, allow_query=False):
    try:
        candidate = normalize_url(url)
    except FetchError:
        return None
    if origin(candidate) != base or (urlsplit(candidate).query and not allow_query):
        return None
    return candidate


class _Run:
    """Zustand eines Laufs: Warteschlange, Pausen, Zeitgrenze."""
    def __init__(self, start, max_pages, delay, max_seconds):
        self.queue, self.seen, self.cached = [start], set(), 0
        self.max_pages, self.delay = max_pages, max(MIN_DELAY, delay)
        self.deadline = time.monotonic() + max_seconds
        self.last = 0.0

    def wait(self):
        # robots Crawl-delay einhalten, auch wenn Firecrawl abruft
        pause = self.delay - (time.monotonic() - self.last)
        if time.monotonic() + max(0, pause) >= self.deadline:
            raise FirecrawlError("Zeitbudget für den Lauf überschritten")
        if pause > 0:
            time.sleep(pause)
        self.last = time.monotonic()


def _get(run, current, client, cache):
    result = cache.get(current) if cache else None
    if result:
        run.cached += 1
        return result
    run.wait()
    result = client.scrape(current)
    if cache:
        cache.put(current, result)
    return result


def _visit(run, current, base, robots, client, cache, report):
    """Eine Seite holen und auswerten. False = Lauf abbrechen."""
    final, status, html = _get(run, current, client, cache)
    if final != current:
        target = _same_site(final, base, allow_query=True)
        if target is None:
            raise FetchError("Firecrawl landete auf anderem Ursprung: " + str(final)[:200])
        if not robots.can_fetch(AGENT, target):
            report["skipped"].append({"url": target, "reason": "Weiterleitungsziel durch robots.txt gesperrt"})
            return True
        final = target
        run.seen.add(final)
    if status in (429, 503):
        report["errors"].append({"url": current, "message": f"HTTP {status}: Prüfung zum Schutz des Servers gestoppt"})
        return False
    if any(page["url"] == final for page in report["pages"]):
        return True
    page, links = analyze(final, html, status)
    report["pages"].append(page)
    for link in links:
        candidate = _same_site(link, base)
        if candidate and candidate not in run.seen and candidate not in run.queue and len(run.queue) < run.max_pages * 10:
            run.queue.append(candidate)
    return True


def render_crawl(url, max_pages=5, client=None, fetcher=None, cache=None, check_dns=True, max_seconds=MAX_SECONDS):
    """Wie crawl(), aber Seiten kommen gerendert über Firecrawl."""
    if not 1 <= max_pages <= MAX_PAGES:
        raise ValueError(f"Seitenlimit muss zwischen 1 und {MAX_PAGES} liegen")
    start = normalize_url(url)
    base = origin(start)
    if check_dns:
        # Vorprüfung, keine Isolation: Firecrawl löst selbst auf (siehe docs/FIRECRAWL.md)
        p = urlsplit(start)
        public_addresses(p.hostname, 443 if p.scheme == "https" else 80)
    report = new_report("firecrawl")
    report["scope"] = {"start_url": start, "origin": base, "max_pages": max_pages,
                       "javascript": True, "query_urls_followed": False, "renderer": "Firecrawl"}
    fetcher = fetcher or Fetcher(max_requests=3)
    robots = load_robots(fetcher, base, report)
    if robots is None:
        return report
    client = client or Client()
    run = _Run(start, max_pages, getattr(fetcher, "delay", 0) or 0, max_seconds)
    stopped = False
    while run.queue and len(run.seen) < max_pages:
        current = run.queue.pop(0)
        if current in run.seen:
            continue
        run.seen.add(current)
        if not robots.can_fetch(AGENT, current):
            report["skipped"].append({"url": current, "reason": "robots.txt"})
            continue
        try:
            if not _visit(run, current, base, robots, client, cache, report):
                stopped = True
                break
        except FirecrawlError as exc:
            # Firecrawl weg, Kontingent leer oder Zeit um: nicht weiter Seiten verbrennen
            report["errors"].append({"url": current, "message": str(exc)})
            stopped = True
            break
        except FetchError as exc:
            report["errors"].append({"url": current, "message": str(exc)})
    report["truncated"] = stopped or bool(run.queue)
    report["requests"] = getattr(client, "calls", None)
    report["cache_hits"] = run.cached
    add_site_findings(report["pages"])
    report["limitations"] = [item for item in report["limitations"] if not item.startswith("Nur Quell-HTML")] + [
        "Gerendert über Firecrawl; ob JavaScript ausgeführt wurde, entscheidet die Firecrawl-Engine.",
        "HTTP-Header wie X-Robots-Tag liefert Firecrawl nicht; dafür den normalen crawl nutzen.",
        "Stichprobe, keine vollständige Website-Abdeckung."]
    return report
