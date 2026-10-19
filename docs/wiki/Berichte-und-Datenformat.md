# Berichte und Datenformat

Markdown ist für Menschen, JSON für Weiterverarbeitung. Der Export legt ausschließlich
neue Dateien an. JSON-Berichte sind ein versionierter Datenvertrag, kein SEO-Score.

| Feld | Bedeutung |
|---|---|
| `schema_version` | Strukturversion des Berichts |
| `tool_version` | Programmstand des Laufs |
| `checked_at` | UTC-Zeitstempel mit Zeitzone |
| `mode` | offline-html oder crawl |
| `pages` | erfasste Seiten einschließlich ihrer Befunde |
| `errors` | Abruffehler mit URL und Meldung |
| `skipped` | übersprungene URLs und Gründe |
| `truncated` | Grenze/Abbruch mit verbleibendem Umfang |
| `limitations` | fachliche und technische Einschränkungen |
| `scope` | beim Crawl Startadresse, Ursprung, Seitenlimit, JS-/Query-Verhalten |
| `discovered_sitemaps` | nach robots-Auswertung gefundene Sitemap-Adressen |
| `requests` | Anfragezähler, sofern verfügbar |

Einige Crawl-Felder fehlen bei frühem Abbruch oder Offline-Modus. Nicht als Nullwert
für eine echte Messung interpretieren. Eine Seite enthält `url`, `http_status`,
`title`, `description`, `canonical`, `h1`, `findings`. Offline ist der Status null.
Ein Befund enthält `rule`, `priority`, `certainty`, `url`, `evidence`,
`recommendation`, `verification`.

Seit Version 0.2.0 bleibt `schema_version` 0.1.0, weil die SEO-Struktur unverändert
ist; `tool_version` gibt den aktuellen Werkzeugstand an. Fremdtext wird in Markdown
maskiert. JSON bleibt Quelldatenmaterial und darf nicht ungeprüft als HTML ausgegeben werden.

Kundenberichte gehören ins Kundenprojekt. Eine Weitergabe an KI-Systeme kann deren
Anbieter einbeziehen. Siehe [Datenschutz](Datenschutz-und-Sicherheit.md).
