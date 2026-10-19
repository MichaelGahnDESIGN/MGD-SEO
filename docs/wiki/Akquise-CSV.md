# Akquise-CSV und Exporthelfer

Pfad: `Akquise-Skill/scripts/export_csv.py`. Python 3.10+, ohne Zusatzpakete und
Netzwerk. Er exportiert vorbereitete Daten, recherchiert sie nicht selbst.

```bash
mkdir -p .tmp/akquise-beispiel
python3 -B Akquise-Skill/scripts/export_csv.py Akquise-Skill/examples/kandidaten.json --output .tmp/akquise-beispiel/kandidaten.csv
```

Synthetisches Beispiel, keine echten Firmen. JSON-Eingang besitzt genau `columns`
und `leads`. `columns` legt Namen und Reihenfolge fest; `leads` enthält Firmenobjekte.

Pflichtspalten: `unternehmen`, `website`, `passungsgrund`, `quelle_url`,
`geprueft_am`, `recherche_status`, `kontaktfreigabe`. Frei ergänzbar: Branche, Ort,
Zentrale, Kontaktseite, Produkte, Quellbelege oder andere vereinbarte Daten.
Keine nicht deklarierten Felder, keine stillen Datenverluste. Zellen sind Text/null.

Prüfdatum: YYYY-MM-DD. Status: belegt / teilweise belegt / nicht verifiziert.
Kontaktfreigabe: ausschließlich `nicht geprüft`. Das ist eine Rechercheliste.

Standard: Semikolon, UTF-8 mit BOM, CRLF. `--delimiter comma`, `--delimiter tab`
und `--no-bom` sind optional. `csv.writer` übernimmt Quoting. Formelverdächtige
Zellen/Überschriften erhalten ein Apostroph; auch +Telefonnummern können betroffen
sein. Rohwerte bleiben im JSON. Tabellenprogramm als Text importieren.

Grenzen: 5 MB Eingang, 100 Spalten, 5000 Zeilen, 20000 Zeichen pro Zelle.
Vollständige Eingabeprüfung vor Dateiöffnung. Zielordner muss bestehen, Zieldatei
neu sein. Code 0 bei Erfolg, Code 2 bei Fehler. Keine Einwilligungs-/Wahrheitsprüfung.
