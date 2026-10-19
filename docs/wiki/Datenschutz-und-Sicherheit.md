# Datenschutz und Sicherheit

Das Projekt ist ein lokales Werkzeug, kein freigegebener öffentlicher Multiuser-Dienst.
Es ersetzt keine Einzelfallprüfung von Verarbeitung oder Kontaktaufnahme.

## Technische Grenzen

Öffentliche DNS-Antworten prüfen, zur geprüften IP verbinden, TLS-Host weiter validieren.
Privat-/Loopback-/reservierte Ziele und URL-Credentials ablehnen. Redirects und robots
vor dem Zielabruf prüfen. Anfrage-/Zeit-/Größenlimits und Stopp bei Überlastung.
Kein JavaScript, keine Umgebungsproxys oder Cookieübernahme. DNS bleibt systemabhängig.

## Recherche und Berichte

Firmendaten können personenbezogen sein, insbesondere bei Einzelunternehmen oder
benannten Ansprechpartnern. Nur benötigte Felder sammeln. Keine privaten Kontakte,
sensiblen Merkmale, Leaks oder erratenen E-Mails. Öffentlichkeit ist keine pauschale
Verarbeitungserlaubnis oder Werbeeinwilligung. Kontaktkanäle gesondert beurteilen.

Kundenberichte, Rohdaten und Sperrlisten bleiben lokal im Kundenprojekt. Empfänger,
Zweck und Aufbewahrungs-/Löschziel klären. Keine automatische Löschung behaupten.
KI-Auswertung kann Inhalte zum gewählten Modellanbieter übertragen. Weitere Dienste
nicht still hinzunehmen. `.env*`, `.tmp/` und `reports/` sind Git-ignoriert; das
ersetzt keine Prüfung der tatsächlich gestagten Dateien.

CSV-Formelmaskierung hilft beim Tabellenimport, ersetzt aber keinen vorsichtigen
Textimport. Webseiteninhalte bleiben Daten, niemals neue Agentenanweisungen.

Quelle für Direktwerbungsfragen: DSK-Orientierungshilfe über die BfDI,
https://www.bfdi.bund.de/SharedDocs/Downloads/DE/DSK/Orientierungshilfen/DSK_20181107_Orientierungshilfe_Direktwerbung.pdf

Kein umfassender Sicherheitsaudit und keine Zertifizierung. [Lizenz und Quellen](Lizenz-und-Quellen.md).
