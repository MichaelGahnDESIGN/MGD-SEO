# Architektur und Datenfluss

Der SEO-Skill steuert das Vorgehen; Python liefert beobachtbare Daten. Die Fachtexte
stehen in kleinen Referenzen. Akquise besitzt einen eigenen Einstieg und Exporthelfer.

| Datei/Bereich | Verantwortung |
|---|---|
| `mgd_seo/network.py` | URL/DNS, geprüfte IP, TLS, Redirects und Budgets |
| `mgd_seo/html.py` | Metadaten ohne Skriptausführung |
| `mgd_seo/audit.py` | Regeln und Titelvergleich |
| `mgd_seo/crawl.py` | robots, Ursprung, Stichprobe und Berichtskontext |
| `mgd_seo/report.py` | maskierte Markdown-Darstellung |
| `mgd_seo/cli.py` | Argumente, Dateieingang, Export und Exitcodes |
| `Akquise-Skill/` | Briefing, Rechercheverfahren, CSV-Validierung |
| `docs/wiki/` | lokale Wiki-Quelle mit Navigation |
| `tools/` | Projektprüfung und lokaler Wiki-Export |

SEO-Datenfluss: Auftrag → URL/Datei → Extraktion → Befunde → JSON/Markdown.
Akquise-Datenfluss: Briefing → öffentliche Quellen → lokale Kandidaten-JSON → CSV.
Es gibt keinen gemeinsamen personenbezogenen Datenpool, keinen Server und keine
Hintergrundsynchronisation. Kundendaten werden nicht in dieses Projekt übernommen.

Kein kopierter Fremd-App-Code und kein obligatorischer MCP. Spätere Browser- und
Shop-Adapter sollen den Kern erweitern, ohne Fachregeln in jeder Oberfläche neu
zu erfinden. Programmversion und SEO-Berichtsschema sind getrennt versioniert.
