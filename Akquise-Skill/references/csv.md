# CSV-Vertrag

## JSON-Eingang für den lokalen Exporthelfer

`columns`: eindeutige nicht leere Spaltennamen in gewünschter Reihenfolge.
`leads`: Liste von Objekten, deren Schlüssel ausschließlich in `columns` stehen.
Alle Zellwerte sind Zeichenketten oder null; Objekte/Listen vorher als verständlichen
Text oder explizite JSON-Zeichenkette aufbereiten. Keine Felder still verwerfen.

Pflichtspalten: `unternehmen`, `website`, `passungsgrund`, `quelle_url`,
`geprueft_am`, `recherche_status`, `kontaktfreigabe`. Andere Spalten sind frei wählbar.
Pflichtwerte müssen ausgefüllt sein. `geprueft_am` ist YYYY-MM-DD.
`recherche_status`: belegt / teilweise belegt / nicht verifiziert.
`kontaktfreigabe`: nicht geprüft. Der Exporthelfer akzeptiert keine behauptete Freigabe.

Ein Datensatz je Firma. Identische Kombination aus normalisiertem Firmennamen und
Domain wird vor dem Export abgewiesen; nichts wird still zusammengeführt oder gelöscht.
www und Subdomains werden nicht automatisch als identische Firma behandelt; vor Export
fachlich prüfen. Filialen bei gewünschter eigener Zeile eindeutig im Unternehmensnamen
kennzeichnen. Verschiedene Firmen auf derselben Domain bleiben möglich.

## Ausgabe und Tabellenprogramme

Standard: Semikolon, UTF-8 mit BOM, CRLF-Zeilenenden. Komma/Tab und ohne BOM optional.
Anführungszeichen, Trennzeichen und Zeilenumbrüche werden mit dem Python-CSV-Modul
korrekt maskiert. Beim Import Telefonnummern, Postleitzahlen und IDs als Text behandeln.

Zellen, deren erster Nicht-Leerraumwert =, +, -, @ oder ein Steuerzeichen ist, erhalten
für den Export ein vorangestelltes Apostroph. Das betrifft auch internationale
Telefonnummern mit +. Diese sichtbare Transformation verhindert in gängigen Tabellen-
Importpfaden eine direkte Formelauswertung; sie ist keine universelle Sicherheitsgarantie
für jedes Programm. CSV als Text importieren, Formeln nicht aktivieren. Rohwerte stehen
im lokalen JSON. Spaltenüberschriften werden ebenfalls geschützt.

Maximal 5 MB JSON-Eingang, 100 Spalten, 5000 Zeilen und 20000 Zeichen je Zelle.
Das sind Exportobergrenzen, kein erlaubter Rechercheumfang. Bestehende Ausgabedateien
werden nicht überschrieben. Vor dem Schreiben wird die komplette Eingabe geprüft.
