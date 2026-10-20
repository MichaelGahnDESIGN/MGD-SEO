# Architektur 0.1.0

Ein gemeinsamer Fachkern, kleine Adapter je Umgebung. Der Skill erklärt Vorgehen
und Grenzen; Python liefert reproduzierbare Beobachtungen. Kein Modellschlüssel,
Hosting oder Shopzugriff für die erste Version.

## Dateien und Verantwortung

- `network.py`: URL-Prüfung, öffentliche DNS-Adressen, IP-gebundene Verbindung,
  TLS-Zertifikatsprüfung, Weiterleitungen und Abrufbudgets.
- `html.py`: Extraktion ohne Skriptausführung.
- `audit.py`: beobachtbare Befunde und Titelvergleich in der Stichprobe.
- `crawl.py`: robots.txt, Warteschlange, Ursprung und Seitenlimit.
- `report.py`: Markdown-Ausgabe mit maskierten Fremdinhalten.
- `cli.py`: Eingabe, Export und Fehlercodes.

## Datenfluss

Auftrag → begrenzte URL oder lokale Datei → Extraktion → Befunde → JSON/Markdown.
Das JSON enthält schema_version/tool_version/checked_at/mode/pages/errors/skipped/
truncated/limitations. Jede Seite enthält URL, Status, Titel, Description, Canonical,
H1 und Befunde. Jeder Befund enthält rule/priority/certainty/url/evidence/recommendation/verification.
Die URL ist unredigierte Projektdaten: sensible Queryparameter nicht verwenden.

Kein Datenbankserver. Berichte verbleiben lokal, werden nicht automatisch übertragen
und gehören ins Kundenprojekt. Roh-HTML wird online nicht dauerhaft gespeichert.
KI-Auswertung kann Berichtsinhalte an den gewählten Modellanbieter übergeben.

## Bewusste Grenzen

Nur öffentliche Standardports; keine Proxys, Cookies oder Authentifizierung.
Die Online-Prüfung ist eine Stichprobe, kein vollständiger Crawl. Kein JavaScript,
keine Dekompression, kein Rendering, kein semantischer Schema-Validator.
DNS nutzt den Systemresolver; dessen Auflösung kann länger als das HTTP-Budget dauern.
Keine zugesicherte Sandbox und kein für fremde Nutzer öffentlich freigegebener Dienst.
Vor SaaS-Nutzung: isolierte Jobs, Egress-Kontrolle, harte Prozesslimits, Mandantenrechte
und Datenlöschung ergänzen.

## Entscheidung zum Stack

Python-Standardbibliothek hält 0.1.0 ohne Installation benutzbar und passt zu einer
späteren optionalen Scrapling-Anbindung. HTML-Prüfregeln bleiben unabhängig von
Browser, MCP und Shop. Kein kopierter Fremd-App-Code.

## Erweiterung 0.2.0

`Akquise-Skill/` enthält einen eigenständigen, datenarmen B2B-Rechercheworkflow
und Offline-CSV-Export. Der Assistent recherchiert; das Skript prüft Format und
exportiert. Keine eingebauten Versand-/CRM-Zugriffe. Das Handbuch wird ausschließlich im [GitHub-Wiki](https://github.com/MichaelGahnDESIGN/MGD-SEO/wiki) gepflegt.
SEO-Berichtsschema bleibt 0.1.0, Werkzeugversion 0.2.0.
