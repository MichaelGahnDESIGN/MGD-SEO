# Technische SEO-Prüfung

Zuerst Statuscodes und beabsichtigten Seitenzweck verstehen. robots.txt steuert
Crawling, ist keine Zugriffskontrolle und garantiert keine Deindexierung. noindex
in HTML und HTTP-Header erfassen; bei robots-Sperre kann ein Crawler das HTML
nicht lesen. HTTP-Link-Header können Canonicals enthalten: der Kern 0.1.0 wertet
sie nicht aus. Fehlenden HTML-Canonical deshalb nur als Hinweis melden.

## Umfang 0.1.0

Title, Description, H1, html lang, HTML-Canonicals, noindex, alt-Attribute,
JSON-LD-Syntax, HTTP-Fehler und doppelte Titel in der Stichprobe. Ein vorhandenes
leeres alt-Attribut ist für dekorative Bilder zulässig. Fehlende Messungen sind
weder bestanden noch fehlgeschlagen. Ohne Vergleich des sichtbaren Inhalts keine
semantische Schema-Abnahme behaupten.

## Spätere Prüfungen

Sitemap-XML und deren URL-Mengen, Canonical-Ketten, interne Linkziele, hreflang-
Rückverweise und HTTP-Link-Header separat implementieren. Für JS-Inhalte
Quell-HTML und gerenderten DOM vergleichen. Lighthouse-Laborwerte und CrUX-Felddaten
mit Messumgebung, Datum und Aggregation ausweisen. Keinen INP aus einem bloßen
Lighthouse-Seitenladevorgang erfinden.

Quellen: https://developers.google.com/search/docs/crawling-indexing/robots/intro
https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
https://developers.google.com/speed/docs/insights/v5/about
