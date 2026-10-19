---
name: mgd-akquise
description: Führt ein B2B-Recherchebriefing durch, sucht passende Unternehmen anhand öffentlicher Quellen und erstellt eine belegte CSV mit den gewünschten Spalten. Verwenden für Zielkundenlisten, Firmenrecherche, B2B-Prospecting und Akquisevorbereitung; kein Versand oder automatische Kontaktaufnahme.
---

# MGD-Akquise-Skill

Von Michael Gahn DESIGN. Bestandteil von MGD-SEO, auch als eigener Skill nutzbar.
Ziel: passende Unternehmen recherchieren und eine nachvollziehbare CSV liefern.
Kein Kontaktversand, keine Werbeeinwilligungen ableiten, keine erfundenen Daten.

## 1. Briefing als Assistent

Zuerst [Fragenkatalog](references/briefing.md) lesen. Bereits genannte Informationen
übernehmen und nur Lücken abfragen. In kurzen Runden mit höchstens drei Themenblöcken
fragen; Antwortmöglichkeiten und verständliche Beispiele anbieten. Nicht sofort alle
Fragen als lange Liste ausgeben. Noch keine breite Recherche bei ungeklärtem Angebot,
Zielkundentyp, Gebiet oder Umfang. Unabhängige Quellenorientierung darf parallel erfolgen.

Am Ende ein kurzes Arbeitsprofil zeigen: Angebot/Ziel, Zielkunden, Gebiet/Sprache,
Muss-/Ausschlusskriterien, Anzahl und Aufwand, Datenfelder, erlaubte Quellen,
Quellenqualität, Personenbezug, CSV-Format und Ablage. Unkritische technische Defaults
benennen statt unnötiger Bestätigung. Offene auftragsentscheidende Fragen auflösen;
keine fehlende Zustimmung durch Zeitablauf ersetzen.

## 2. Öffentlich recherchieren

[Recherche und Datenschutz](references/recherche.md) beachten. Nur verfügbare
Such-/Browser-/MCP-Werkzeuge verwenden; keine API, kein Scraper und kein Account
wird ungefragt installiert oder verbunden. Kein Werkzeug ist zwingend erforderlich.
Bei fehlendem Webzugriff bereitgestellte Quellen auswerten und Grenze nennen.

Suchanfragen aus Branche, Region, angebotener Lösung und konkreten Zielmerkmalen
bilden. Suchtreffer sind Kandidaten, kein Beleg. Firmenwebsite, Leistungsseite,
Kontaktseite und relevante weitere Primärquellen lesen. Keine Kontaktformulare senden.
Pro Firma: Unternehmensidentität, Webadresse, belegte Zielmerkmale, Passungsgrund,
Quellen-URL und Prüfdatum erfassen. Kurzbelege und Quellen je Zusatzfeld dokumentieren,
bei Bedarf in `quellen_details`. Kein Umsatz, Budget, Mitarbeiterstand oder Bedarf
schätzen. Anbieterbehauptung und eigene Schlussfolgerung unterscheiden.

Öffentlich sichtbare technische Schwächen sind Beobachtungen, kein Nachweis eines
Kaufinteresses. SEO-Tiefenprüfungen nur im beauftragten Umfang mit MGD-SEO ausführen.
Keine Behauptung „braucht dringend SEO“, kein pauschaler Lead-Score ohne erklärte Kriterien.

## 3. Auswahl und Qualität

Muss-/Ausschlusskriterien pro Kandidat prüfen. Quellenkonflikte und unbekannte Werte
markieren. Mehrere Standorte derselben Firma nach Briefing behandeln. Keine doppelte
Firma nur wegen unterschiedlicher Tracking-URL. Andere Firmen mit gemeinsamer Domain
nicht automatisch zusammenlegen. Kontakt-/Sperrlisten des Nutzers lokal berücksichtigen;
keine fremden Listen hochladen. Nicht passende oder widersprechende Datensätze nicht
heimlich ergänzen, nur um die gewünschte Anzahl zu erreichen. Bei erreichtem Aufwandlimit
mit Teilmenge und klarer Abdeckung abschließen.

## 4. CSV erstellen

[CSV-Vertrag](references/csv.md) lesen. Gewünschte Spalten sind verbindlich und können
über die Standardfelder hinausgehen. Fehlende Werte bleiben leer; Quellen und Status
bleiben vorhanden. Standard: Semikolon, UTF-8 mit BOM für Excel, eine Firma je Zeile.
Rohdaten als JSON und fertige CSV im Kundenprojekt unter `.tmp/<Aufgabe>/` oder einem
explizit gewünschten Ergebnisordner anlegen, niemals im installierten Skill ablegen.
Keine echte Kundenliste, Personen- oder Kontaktdaten in dieses öffentliche Skill-Repo.

Lokaler Exporthelfer, Pfad relativ zu diesem Skill-Ordner:

```bash
python3 -B scripts/export_csv.py /PFAD/ZUM/KUNDENPROJEKT/.tmp/akquise/kandidaten.json --output /PFAD/ZUM/KUNDENPROJEKT/.tmp/akquise/kandidaten.csv
```

Das JSON enthält `columns` und `leads`; Strukturbeispiel: `examples/kandidaten.json`.
Bei anderem Trennzeichen `--delimiter comma` oder `--delimiter tab` verwenden.
Mit `--no-bom` reines UTF-8 ausgeben. Bestehende Dateien werden nicht überschrieben.
Der Helfer prüft Format, nicht Wahrheit oder Rechtmäßigkeit der Recherche.
Ohne Python dieselben CSV-Regeln mit vorhandenem Dateitool erfüllen. Wenn keine Datei
angelegt werden kann, echte CSV als Codeblock liefern und fehlenden Dateiexport nennen.

## 5. Abschluss

CSV-Datei verlinken. Anzahl eindeutiger Firmen, Suchraum, Zeitstand, fehlende Felder,
Ausschlüsse und offene Validierungen knapp berichten. Bei Teilmenge die Ursache nennen.
Keine Treffer als Kaufinteressenten oder kontaktierte Kunden bezeichnen.
`kontaktfreigabe` lautet standardmäßig und im Exporthelfer immer `nicht geprüft`.
Recherche und Kontaktaufnahme bleiben getrennte Aufträge. Aufbewahrungs-/Löschziel
im Briefing festhalten; keine automatische Hintergrundüberwachung oder Wiederholung.
