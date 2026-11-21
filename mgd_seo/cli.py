"""Kommandozeile: Offline-HTML oder begrenzte öffentliche URL-Stichprobe prüfen."""
import argparse
import json
import os
from pathlib import Path
from .audit import analyze
from .crawl import crawl, new_report
from .network import FetchError, normalize_url
from .report import compact, markdown

FORMATS = {"markdown": markdown, "compact": compact}


def main(argv=None):
    parser = argparse.ArgumentParser(description="MGD-SEO 0.3.0 – lokale SEO-Prüfung")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Verfügbarkeit ohne Installation prüfen")
    offline = commands.add_parser("html", help="Lokale HTML-Datei ohne Netzwerk prüfen")
    offline.add_argument("file", type=Path)
    offline.add_argument("--url", required=True, help="Öffentliche Bezugs-URL für relative Links")
    online = commands.add_parser("crawl", help="Öffentliche Website begrenzt prüfen")
    online.add_argument("url")
    online.add_argument("--max-pages", type=int, default=10)
    rendered = commands.add_parser("render", help="Gerenderte Seiten über Firecrawl prüfen (optional)")
    rendered.add_argument("url")
    rendered.add_argument("--max-pages", type=int, default=5)
    rendered.add_argument("--cache", type=Path, help="Ordner für Zwischenspeicher (24 h), spart Firecrawl-Credits")
    for command in (offline, online, rendered):
        command.add_argument("--format", choices=("json", "markdown", "compact"), default="markdown")
        command.add_argument("--output", type=Path, help="Neue Datei; bestehende Dateien werden nicht überschrieben")
    args = parser.parse_args(argv)
    if args.command == "doctor":
        return doctor()
    try:
        if args.command == "html":
            if args.file.stat().st_size > 2_000_000:
                raise ValueError("HTML-Datei überschreitet 2 MB")
            url = normalize_url(args.url)
            report = new_report("offline-html")
            page, _ = analyze(url, args.file.read_text(encoding="utf-8", errors="replace"))
            page["http_status"] = None
            report["pages"].append(page)
            report["limitations"].append("Offline-Datei: HTTP-Status und Header wurden nicht gemessen.")
        elif args.command == "render":
            from .firecrawl import Cache, render_crawl
            report = render_crawl(args.url, args.max_pages, cache=Cache(args.cache) if args.cache else None)
        else:
            report = crawl(args.url, args.max_pages)
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else FORMATS[args.format](report)
        if args.output:
            with args.output.open("x", encoding="utf-8") as target:
                target.write(output)
        else:
            print(output, end="")
        return 2 if report["errors"] else 0
    except (OSError, ValueError) as exc:
        parser.exit(2, "MGD-SEO: " + str(exc) + "\n")


def doctor():
    print("MGD-SEO 0.3.0: Python-Kern verfügbar; keine Zusatzpakete erforderlich.")
    from .firecrawl import FirecrawlError, endpoint
    try:
        base, key, kind = endpoint()
        # nur Einstellung zeigen, kein Abruf und nie den Schlüssel
        print(f"Firecrawl ({kind}): {base} · Schlüssel {'gesetzt' if key else 'nicht gesetzt'}"
              + ("" if os.environ.get("MGD_SEO_FIRECRAWL_URL") else " (Standard, nicht geprüft ob er läuft)"))
    except FirecrawlError as exc:
        print("Firecrawl: " + str(exc))
    print("JavaScript per Scrapling-MCP, Lighthouse und Search Console: nicht durch diesen Befehl geprüft.")
    return 0
