"""Bereitet ein neues lokales Wiki-Verzeichnis vor; niemals Netzwerk oder Push.

Quelldateien bleiben unverändert. Erst alle Links prüfen und Texte vorbereiten,
dann das noch nicht bestehende Ziel anlegen. Nur Markdown-Seiten werden exportiert.
"""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([A-Za-z0-9_-]+)\.md(#[^)]*)?\)")


def export(source, destination):
    pages = sorted(source.glob("*.md"))
    names = {page.stem for page in pages}
    if not {"Home", "_Sidebar", "_Footer"} <= names:
        raise ValueError("Startseite oder Navigation fehlt")
    prepared = {}
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            if match.group(1) not in names:
                raise ValueError("Fehlende Wiki-Zielseite: " + match.group(1))
        prepared[page.name] = LINK.sub(lambda m: "](" + m.group(1) + (m.group(2) or "") + ")", text)
    destination.mkdir(parents=True, exist_ok=False)
    for name, text in prepared.items():
        with (destination / name).open("x", encoding="utf-8") as target:
            target.write(text)
    return len(prepared)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Wiki lokal für GitHub vorbereiten – ohne Veröffentlichung")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        count = export(ROOT / "docs/wiki", args.output)
        print(f"{count} Wiki-Dateien lokal exportiert. Kein Upload oder Push.")
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, "MGD-SEO Wiki: " + str(exc) + "\n")

if __name__ == "__main__":
    raise SystemExit(main())
