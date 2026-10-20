<!-- MGD-HEADER -->
<p align="center"><a href="https://Michael-Gahn.de"><img src="assets/mgd-logo.png" alt="Michael Gahn DESIGN" width="48"></a></p>
<p align="center"><img src="assets/banner.svg" alt="MGD-SEO – Erst prüfen. Dann verbessern." width="100%"></p>
<!-- /MGD-HEADER -->

# MGD-SEO

**SEO prüfen, Befunde belegen und sinnvolle Verbesserungen planen.**
Ein deutschsprachiger Skill für Codex und Claude mit einem lokal ausführbaren
Python-Prüfkern. Von Michael Gahn DESIGN.

**Version 0.2.0 · Pre-Alpha · Quellcode auf GitHub · noch kein Release**

## Was schon funktioniert

- Öffentliche HTML-Seiten als begrenzte Stichprobe lesen oder lokale HTML-Dateien prüfen.
- Title, Description, H1, Sprache, Canonicals, noindex, fehlende alt-Attribute und JSON-LD-Syntax erfassen.
- Doppelte Titel innerhalb der Stichprobe erkennen.
- Ergebnisse mit Zeitstempel, URL, Nachweis, Empfehlung und Grenzen als Markdown/JSON ausgeben.
- robots.txt beachten; private Netzwerkziele, fremde Redirect-Ursprünge und übergroße Antworten sperren.

**Kein Rankingversprechen und kein erfundener SEO-Score.** Noch keine JavaScript-Ausführung,
Sitemap-Inhaltsprüfung, Linkzielprüfung, Search-Console-Verbindung oder Shopänderung.
Scrapling, Lighthouse und weitere MCPs sind optionale Integrationen für spätere Stufen,
keine still installierten Bestandteile dieser Version.

## B2B-Akquise-Assistent

Neu: [MGD-Akquise-Skill](Akquise-Skill/README.md) mit Zielkunden-Briefing, öffentlicher
Firmenrecherche und CSV-Ausgabe mit Wunschspalten, Quellen und Prüfdatum. Keine
automatische Kontaktaufnahme. Der Exporthelfer arbeitet ohne Zusatzpakete.

## Wiki

Das vollständige [Wiki](docs/wiki/Home.md) ist im Repository enthalten.
Die Veröffentlichung als separates GitHub-Wiki steht noch aus.

## Sofort lokal verwenden

Python 3.10 oder neuer. Keine Fremdpakete für den Prüfkern erforderlich.
Im Projektordner:

```bash
python3 -B -m mgd_seo doctor
python3 -B -m mgd_seo html tests/fixtures/example.html --url https://example.org/
python3 -B -m mgd_seo crawl https://DEINE-DOMAIN.example/ --max-pages 10
```

Die letzte URL durch eine autorisierte öffentliche Zielseite ersetzen.
Maximal 50 Seitenkandidaten, 120 Sekunden Abrufbudget und 2 MB je Antwort.
DNS-Auflösung unterliegt zusätzlich den System-Resolver-Zeiten; kein harter
Prozesszeitwächter. Seiten mit Queryparametern werden nicht automatisch verfolgt.
Ein Start mit Query ist ausdrücklich möglich. Maximal 5 Weiterleitungen;
HTTP/HTTPS und Standardports 80/443. Keine parallelen Abrufe, mindestens 0,5 Sekunden Abstand.
Cross-Origin-Weiterleitungen werden auch bei www/HTTPS-Wechsel gestoppt.
Bei HTTP 429/503 wird die Prüfung beendet. Fehlgeschlagene robots.txt-Prüfung
stoppt den Crawl; 404/410 erlauben die Prüfung ohne Crawl-Regeln.

Bericht als neue Datei speichern (Zielordner muss existieren):

```bash
python3 -B -m mgd_seo html tests/fixtures/example.html --url https://example.org/ --format json --output .tmp/beispiel.json
```

Bestehende Dateien werden nicht überschrieben. Exitcode 0 bedeutet abgeschlossene
Prüfung, nicht „SEO perfekt“. Exitcode 2 bedeutet Eingabe- oder Abruffehler;
Teilberichte bleiben bei Crawl-Fehlern verfügbar.

## Als Skill nutzen

- **Codex:** Repository vollständig in einen erkannten Skill-Ordner installieren,
  etwa `~/.agents/skills/mgd-seo/`. Danach `$mgd-seo` verwenden.
- **Claude Code:** Repository vollständig unter `~/.claude/skills/mgd-seo/` ablegen.
  Danach `/mgd-seo` in einer neuen Sitzung verwenden.
- **Ohne Installation:** `SKILL.md` und bei Bedarf die verlinkten Referenzen als
  Projektmaterial bereitstellen. Chat ohne Python-/Werkzeugzugriff kann Dateien
  auswerten, aber keinen lokalen Crawler starten.
- **Cowork und Web-Anschlüsse:** Eigene Pakete und jeweilige Abnahme sind für 0.3.0
  geplant. Ein lokaler Skill-Ordner ist keine automatische Cowork-Installation.

Es wurde mit dieser Entwicklung nichts global installiert oder an bestehenden
Claude-/Codex-Konfigurationen geändert. Plattformtests sind getrennt vom Python-Test
zu bewerten. Siehe [Integrationen](references/integrations.md).

## Für Entwickler

```bash
python3 -B -m unittest discover -s tests -v
```

Struktur: `mgd_seo/` Prüfkern, `references/` Fachwissen, `tests/` reproduzierbare
Fixtures, `docs/` Architektur, Plan und Arbeitsberichte. Der Kern nutzt nur die
Python-Standardbibliothek. Ein optionales `pip install .` benötigt Build-Werkzeuge;
für die obigen Befehle ist das nicht nötig.

## Weiterentwicklung

[Plan](docs/plans/2026-10-20-mgd-seo.md) · [Architektur](docs/ARCHITEKTUR.md) ·
[Roadmap](ROADMAP.md) · [Änderungen](CHANGELOG.md) · [Datenschutz und Sicherheit](SECURITY.md)

Später: Messdaten, MGD-Plattform-Builder, WordPress/WooCommerce, Shopware, vorhandenes
MGD JTL SEO & PageSpeed und Shopify. Jeder Adapter bekommt eigene Versions- und
Staging-Tests; es gibt kein universelles Shop-Plugin für alle Systeme.

## Verwandte MGD-Projekte

- [MGD-Plattform-Builder](https://github.com/MichaelGahnDESIGN/MGD-Plattform-Builder)
- [MGD DEV Skill](https://github.com/MichaelGahnDESIGN/MGD_DEV_SKILL)
- [MGD Todo Skill](https://github.com/MichaelGahnDESIGN/MGD_Todo_SKILL)
- [MGD JTL SEO & PageSpeed](https://github.com/MichaelGahnDESIGN/MGD_JTL-SEO-Plugin)

## Lizenz und Herkunft

Eigene Bestandteile: [MIT](LICENSE). [Herkunft und geprüfte Quellen](THIRD_PARTY.md).
Fremdwerkzeuge werden nicht mitgeliefert und behalten ihre eigenen Lizenzen.
[Impressum](IMPRESSUM.md). Keine externen Schrift-, Icon- oder Laufzeitressourcen.
