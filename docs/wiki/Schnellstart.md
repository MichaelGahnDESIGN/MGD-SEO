# Schnellstart

Alle Befehle aus der Wurzel deiner vollständigen MGD-SEO-Arbeitskopie ausführen.
Vorhandene Python-Version mit `python3 --version` prüfen; ab 3.10 unterstützt.

```bash
python3 -B -m mgd_seo doctor
python3 -B -m mgd_seo html tests/fixtures/example.html --url https://example.org/
```

`doctor` installiert nichts. Die synthetische Beispieldatei benötigt keinen
Netzwerkzugriff. Ihre Bezugs-URL löst relative Links auf; sie wird nicht abgerufen.
Der Offline-HTTP-Status lautet „nicht gemessen“.

## Berichte speichern

```bash
mkdir -p .tmp/wiki-beispiele
python3 -B -m mgd_seo html tests/fixtures/example.html --url https://example.org/ --format json --output .tmp/wiki-beispiele/seo.json
```

Der Zielordner muss bestehen, die Datei darf noch nicht existieren. Wiederholung mit
neuem Namen; kein stilles Überschreiben. Kundendaten im zugehörigen Kundenprojekt ablegen.

## Eine Website prüfen

Nach Festlegung der autorisierten Zielwebsite:

```bash
python3 -B -m mgd_seo crawl https://DEINE-DOMAIN.example/ --max-pages 5
```

Beispieladresse ersetzen. Der Crawler liest zuerst robots.txt, anschließend höchstens
fünf Seitenkandidaten desselben Ursprungs. Eine Sperre ist keine Aufforderung zur Umgehung.

Für Firmenrecherche: [MGD-Akquise](MGD-Akquise.md). Für Optionen: [Kommandozeile](Kommandozeile.md).
