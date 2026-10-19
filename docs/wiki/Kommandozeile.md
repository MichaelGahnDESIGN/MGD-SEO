# Kommandozeile

```bash
python3 -B -m mgd_seo --help
python3 -B -m mgd_seo doctor
python3 -B -m mgd_seo html DATEI --url https://example.org/
python3 -B -m mgd_seo crawl https://DEINE-DOMAIN.example/ --max-pages 10
```

| Option | Gilt für | Bedeutung |
|---|---|---|
| `--url` | html | erforderliche Bezugs-URL; kein Netzwerkabruf |
| `--max-pages` | crawl | 1 bis 50 Kandidaten; Standard 10 |
| `--format markdown` | html/crawl | Standardausgabe für Menschen |
| `--format json` | html/crawl | strukturierte Daten |
| `--output DATEI` | html/crawl | neue Datei statt Standardausgabe |

`doctor` prüft den Python-Einstieg. Es bestätigt weder Browserinstallation noch
Search Console, Lighthouse oder externe MCPs. Keine automatischen Reparaturen.

Exitcode 0: Verarbeitung abgeschlossen, auch wenn Befunde oder übersprungene URLs
vorliegen. Exitcode 2: Eingabe-/Abruffehler. Bei Online-Teilfehlern kann ein Bericht
mit `errors` entstehen. Syntaxfehler in Argumenten werden durch argparse abgelehnt.

Es gibt derzeit keine CLI-Option für Cookies, Authentifizierung, Proxy, Threads,
Rendern, Sitemap-Crawling oder das Abschalten der Privatnetz-Sperre.

Der Akquise-Helfer besitzt eine eigene CLI: [CSV-Ausgabe](Akquise-CSV.md).
