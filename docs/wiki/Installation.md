# Installation

## Voraussetzungen

Python 3.10 oder neuer, lesbarer Projektordner, für Online-Crawls ausgehendes DNS und
HTTP/HTTPS. Laufzeit ohne Fremdpakete. Unter Windows gegebenenfalls `py -3` anstelle
von `python3` verwenden. Diese Befehlsvariante wurde nicht gesondert unter Windows getestet.

Das vollständige Repository wird benötigt: nur `SKILL.md` kopieren reicht für den
Python-Kern nicht. Noch kein GitHub-Remote: keine vermeintlich vorhandene Download-
oder Release-Adresse verwenden. Die lokale Arbeitskopie ist der aktuelle Lieferstand.

## Direktbetrieb

Terminal im Projektordner öffnen, `python3 -B -m mgd_seo doctor` ausführen.
`-B` verhindert Python-Cachedateien. Keine System-Python-Pakete verändern.

## Optional in eine virtuelle Umgebung installieren

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/mgd-seo doctor
```

Diese optionale Installation kann Build-Abhängigkeiten aus dem Paketindex laden.
Sie ist für den Direktbetrieb nicht erforderlich und keine Abnahme sämtlicher
KI-Clients. Unter Windows liegen Programme üblicherweise unter `.venv/Scripts/`.

Akquise läuft auch direkt: `python3 -B Akquise-Skill/scripts/export_csv.py --help`.
Keine globale Installation durch den Entwicklungsauftrag erfolgt.
Weiter: [Codex und Claude](Codex-und-Claude.md).
