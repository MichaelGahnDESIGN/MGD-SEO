"""Kommandozeile: Offline-HTML oder begrenzte öffentliche URL-Stichprobe prüfen."""
import argparse
import json
from pathlib import Path
from .audit import analyze
from .crawl import crawl, new_report
from .network import FetchError, normalize_url
from .report import markdown


def main(argv=None):
    parser = argparse.ArgumentParser(description="MGD-SEO 0.1.0 – lokale SEO-Prüfung")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Verfügbarkeit ohne Installation prüfen")
    offline = commands.add_parser("html", help="Lokale HTML-Datei ohne Netzwerk prüfen")
    offline.add_argument("file", type=Path)
    offline.add_argument("--url", required=True, help="Öffentliche Bezugs-URL für relative Links")
    online = commands.add_parser("crawl", help="Öffentliche Website begrenzt prüfen")
    online.add_argument("url")
    online.add_argument("--max-pages", type=int, default=10)
    for command in (offline, online):
        command.add_argument("--format", choices=("json", "markdown"), default="markdown")
        command.add_argument("--output", type=Path, help="Neue Datei; bestehende Dateien werden nicht überschrieben")
    args = parser.parse_args(argv)
    if args.command == "doctor":
        print("MGD-SEO 0.1.0: Python-Kern verfügbar; keine Zusatzpakete erforderlich.")
        print("JavaScript, Scrapling-MCP, Lighthouse und Search Console: nicht durch diesen Befehl geprüft.")
        return 0
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
        else:
            report = crawl(args.url, args.max_pages)
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown(report)
        if args.output:
            with args.output.open("x", encoding="utf-8") as target:
                target.write(output)
        else:
            print(output, end="")
        return 2 if report["errors"] else 0
    except (OSError, ValueError) as exc:
        parser.exit(2, "MGD-SEO: " + str(exc) + "\n")
