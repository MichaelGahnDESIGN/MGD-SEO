# Produkt und Umfang

MGD-SEO verbindet einen deutschsprachigen Agent-Skill mit einem kleinen lokalen
Python-Prüfkern. Fachreferenzen werden bei Bedarf gelesen, nicht bei jedem Auftrag
vollständig geladen. Der eigenständige Ordner `Akquise-Skill/` ergänzt B2B-Recherche.

| Bereich | Stand 0.2.0 |
|---|---|
| Lokale HTML-Dateien | implementiert, ohne Netzwerk |
| Öffentliche Webseiten | begrenzte Quell-HTML-Stichprobe |
| SEO-Befunde | zwölf Regel-IDs, Zeitstempel und Nachweise |
| Berichte | JSON und Markdown |
| Akquise | geführter Skill, freie Wunschspalten, lokaler CSV-Helfer |
| Wiki | lokale Quellen und Export für spätere Veröffentlichung |
| JavaScript/DOM | nicht im Prüfkern implementiert |
| Rankings, Search Console, Lighthouse | keine eingebaute Messung |
| Eigener MCP, Cowork-Paket | geplant |
| Shopänderungen und Kontaktversand | nicht Bestandteil |

Keine Datenbank, kein verpflichtender API-Schlüssel, keine Telemetrie. Für den
Python-Kern reichen Standardbibliothek und Python 3.10+. KI-Nutzung und optionale
externe Dienste können unabhängig davon Kosten verursachen.

„Keine Auffälligkeit“ bezieht sich auf implementierte Regeln und gelesene Stichprobe.
Es bedeutet weder vollständige Barrierefreiheit noch gute Rankings oder Indexierung.
Weiter: [Schnellstart](Schnellstart.md), [Prüfregeln](Pruefregeln.md).
