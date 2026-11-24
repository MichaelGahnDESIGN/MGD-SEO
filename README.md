<!-- MGD-HEADER -->
<p align="center"><a href="https://Michael-Gahn.de"><img src="assets/mgd-logo.png" alt="Michael Gahn DESIGN" width="48"></a></p>
<p align="center"><img src="assets/banner.svg" alt="MGD-SEO – Erst prüfen. Dann verbessern." width="100%"></p>
<!-- /MGD-HEADER -->

# MGD-SEO

**SEO prüfen, Befunde belegen und sinnvolle Verbesserungen planen.**
Ein deutschsprachiger Skill für Codex und Claude mit einem lokal ausführbaren
Python-Prüfkern. Von Michael Gahn DESIGN.

**Version 0.3.0 · Pre-Alpha · [Pre-Release v0.3.0](https://github.com/MichaelGahnDESIGN/MGD-SEO/releases/tag/v0.3.0)**

## Was schon funktioniert

- Öffentliche HTML-Seiten als begrenzte Stichprobe lesen oder lokale HTML-Dateien prüfen.
- Title, Description, H1, Sprache, Canonicals, noindex, fehlende alt-Attribute und JSON-LD-Syntax erfassen.
- Doppelte Titel innerhalb der Stichprobe erkennen.
- Ergebnisse mit Zeitstempel, URL, Nachweis, Empfehlung und Grenzen als Markdown/JSON ausgeben.
- robots.txt beachten; private Netzwerkziele, fremde Redirect-Ursprünge und übergroße Antworten sperren.
- Neu in 0.3.0: Seiten mit JavaScript über **Firecrawl** prüfen (`render`), kostenlos per eigenem Docker oder Gratis-Kontingent. Kurzbericht `--format compact` spart Tokens. Anleitung: [Firecrawl](docs/FIRECRAWL.md).

**Kein Rankingversprechen und kein erfundener SEO-Score.** JavaScript nur über das optionale Firecrawl,
Sitemap-Inhaltsprüfung, Linkzielprüfung, Search-Console-Verbindung oder Shopänderung.
Scrapling, Lighthouse und weitere MCPs sind optionale Integrationen für spätere Stufen,
keine still installierten Bestandteile dieser Version.

## B2B-Akquise-Assistent

Neu: [MGD-Akquise-Skill](Akquise-Skill/README.md) mit Zielkunden-Briefing, öffentlicher
Firmenrecherche und CSV-Ausgabe mit Wunschspalten, Quellen und Prüfdatum. Keine
automatische Kontaktaufnahme. Der Exporthelfer arbeitet ohne Zusatzpakete.

## Wiki

Das vollständige [GitHub-Wiki](https://github.com/MichaelGahnDESIGN/MGD-SEO/wiki) enthält das Handbuch und wird getrennt vom Quellcode gepflegt.

## Sofort lokal verwenden

Python 3.10 oder neuer. Keine Fremdpakete für den Prüfkern erforderlich.
Im Projektordner:

```bash
python3 -B -m mgd_seo doctor
python3 -B -m mgd_seo html tests/fixtures/example.html --url https://example.org/
python3 -B -m mgd_seo crawl https://DEINE-DOMAIN.example/ --max-pages 10
python3 -B -m mgd_seo render https://DEINE-DOMAIN.example/ --format compact --cache .tmp/firecrawl
```

Der Befehl `render` braucht einen laufenden Firecrawl, siehe [Firecrawl-Anleitung](docs/FIRECRAWL.md).

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

<!-- MGD-RELATED:START -->
## Skill-Empfehlungen

Passt gut dazu:

| Skill | Befehl | Wofür |
|---|---|---|
| [MGD_Divi5-Dev_SKILL](https://github.com/MichaelGahnDESIGN/MGD_Divi5-Dev_SKILL) | `/divi` | WordPress und Divi 5: Animationen, Plugins, Child-Themes |
| [MGD_JTL-OPC_SKILL](https://github.com/MichaelGahnDESIGN/MGD_JTL-OPC_SKILL) | `/jtl-opc` | JTL-Shop-5-Seiten im OnPage Composer automatisch befüllen |
| [MGD_DEV_SKILL](https://github.com/MichaelGahnDESIGN/MGD_DEV_SKILL) | `/dev` | Release, Sync, Backup, Cleanup, Tests und Wissensdokumentation |

## Verwandte MGD Projekte

<details><summary>Alle MGD-Skills und Werkzeuge anzeigen</summary>

| Projekt | Befehl | Wofür |
|---|---|---|
| [MGD_Todo_SKILL](https://github.com/MichaelGahnDESIGN/MGD_Todo_SKILL) | `/todo` | Aufgabenliste in einer HTML-Datei, dazu /board, /wissen, /fragenkatalog, /prozesse |
| [MGD_DEV_SKILL](https://github.com/MichaelGahnDESIGN/MGD_DEV_SKILL) | `/dev` | Release, Sync, Backup, Cleanup, Tests und Wissensdokumentation |
| [MGD_Autopilot_SKILL](https://github.com/MichaelGahnDESIGN/MGD_Autopilot_SKILL) | `/autopilot` | Projektziele sicher unbeaufsichtigt abarbeiten |
| [MGD_Backup_SKILL](https://github.com/MichaelGahnDESIGN/MGD_Backup_SKILL) | `/backup` | Backups lokal, NAS und Cloud mit Prüfsummen |
| [MGD_AI-Thread](https://github.com/MichaelGahnDESIGN/MGD_AI-Thread) | `/thread` | Ehrliche Übergabe, bevor das Kontextfenster voll ist |
| [MGD_ProjectClean_SKILL](https://github.com/MichaelGahnDESIGN/MGD_ProjectClean_SKILL) | `/projectclean` | Abschluss und Aufräumen: Version, Tests, Commit, Doku, Backup |
| [MGD_Living-Documentation](https://github.com/MichaelGahnDESIGN/MGD_Living-Documentation) | `/doku` | Lebendige Dokumentation: keine Entscheidung geht verloren |
| [MGD_BugReport_SKILL](https://github.com/MichaelGahnDESIGN/MGD_BugReport_SKILL) | `/bugreport` | Handbuch für Bug-Reports, Feedback und QA in Apps |
| [MGD_AI-PlayTest_SKILL](https://github.com/MichaelGahnDESIGN/MGD_AI-PlayTest_SKILL) | `/playtest` | Test aus Nutzerperspektive für KI-gebaute Funktionen |
| [MGD_AI-Testaccount_SKILL](https://github.com/MichaelGahnDESIGN/MGD_AI-Testaccount_SKILL) | `/testaccount` | Testkonten per Plus-Adresse mit klaren Sicherheitsregeln |
| [MGD_Software-Updater_SKILL](https://github.com/MichaelGahnDESIGN/MGD_Software-Updater_SKILL) | `/software-updater` | Update-Systeme planen und umsetzen |
| [MGD_Divi5-Dev_SKILL](https://github.com/MichaelGahnDESIGN/MGD_Divi5-Dev_SKILL) | `/divi` | WordPress und Divi 5: Animationen, Plugins, Child-Themes |
| [MGD_JTL-OPC_SKILL](https://github.com/MichaelGahnDESIGN/MGD_JTL-OPC_SKILL) | `/jtl-opc` | JTL-Shop-5-Seiten im OnPage Composer automatisch befüllen |
| [MGD-Motion-Graphics-Video-Skill](https://github.com/MichaelGahnDESIGN/MGD-Motion-Graphics-Video-Skill) | `/mgd-video` | Reels, YouTube, Werbefilme und Animationen |
| [MGD-Foundry-VTT_Skill](https://github.com/MichaelGahnDESIGN/MGD-Foundry-VTT_Skill) | `/vttl-notizbuch` | Foundry VTT und D&D-Notizbücher |
| [MGD_AI-Basic-Projektordner_TOOL](https://github.com/MichaelGahnDESIGN/MGD_AI-Basic-Projektordner_TOOL) | `Vorlage` | Projektordner für ChatGPT Codex, Cowork und Claude Code |
| [MGD_Docker_Projektbuilder](https://github.com/MichaelGahnDESIGN/MGD_Docker_Projektbuilder) | `Generator` | Docker-Plattform-Gerüste aus sechs Fragen |
| [MGD_Claude-Codex_MCP](https://github.com/MichaelGahnDESIGN/MGD_Claude-Codex_MCP) | `MCP` | Lokales MCP für Aufgaben, Chat und Übergaben zwischen KI-Agenten |

</details>

Mit `/skill-update` (im Todo-Skill) holst du alle lokal installierten MGD-Skills auf den neuesten Stand.
<!-- MGD-RELATED:END -->

## Lizenz und Herkunft

Eigene Bestandteile: [MIT](LICENSE). [Herkunft und geprüfte Quellen](THIRD_PARTY.md).
Fremdwerkzeuge werden nicht mitgeliefert und behalten ihre eigenen Lizenzen.
[Impressum](IMPRESSUM.md). Keine externen Schrift-, Icon- oder Laufzeitressourcen.
