# Implementierte Prüfregeln

Die Priorität ist eine erste technische Einordnung, keine individuelle Geschäftswirkung.
Sie muss mit Seitentyp und Auftrag abgeglichen werden.

| Regel-ID | Beobachtung | Standardpriorität |
|---|---|---|
| `http-error` | HTTP-Status ab 400 | hoch |
| `title` | kein einzelnes ausgefülltes Title-Element | mittel |
| `description` | keine einzelne ausgefüllte Description | mittel |
| `canonical-multiple` | mehrere HTML-Canonicals | hoch |
| `canonical-missing` | kein HTML-Canonical | Hinweis |
| `h1-missing` | keine H1 im Quell-HTML | mittel |
| `h1-multiple` | mehrere H1 | Hinweis |
| `language-missing` | html lang fehlt/leer | Hinweis |
| `image-alt` | img ohne alt-Attribut | mittel |
| `noindex` | noindex in erfassten Meta-/HTTP-Angaben | Hinweis |
| `jsonld-syntax` | JSON-LD lässt sich nicht als JSON lesen | mittel |
| `duplicate-title` | gleiche Titel in gelesener Stichprobe, ohne Groß-/Kleinschreibung | mittel |

Leeres alt ist bei dekorativen Bildern zulässig; die inhaltliche Eignung eines Alttextes
wird nicht automatisch geprüft. JSON-LD-Syntax sagt nichts über semantische Korrektheit,
sichtbaren Inhalt oder Rich-Result-Eignung aus. `lang` wird auf Vorhandensein, nicht
vollständig auf sprachliche Korrektheit geprüft.

`noindex` ist eine Beobachtung, keine Aussage über Googles tatsächlichen Index.
HTTP-Header mit komplexen botbezogenen Regeln müssen bei Bedarf fachlich geprüft werden.
Mehrere H1 und fehlendes Schema sind keine automatischen Rankingfehler.

Noch nicht implementiert: Canonical-Zielketten, externe Linkziele, Sitemap-XML,
hreflang-Rückverweise, vollständige HTTP-Link-Header-Auswertung und DOM-Vergleich.
