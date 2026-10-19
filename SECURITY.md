# Datenschutz und Sicherheit

0.1.0 ist ein lokales Werkzeug für autorisierte öffentliche Seiten. Keine allgemeine
Hosting-Freigabe, kein vollständiges Sicherheitsaudit. Sicherheitsentscheidungen
wurden mit dem globalen security-audit-Skill im Guidance-Modus berücksichtigt.

## Eingebaute Grenzen

Nur HTTP/HTTPS-Standardports, keine URL-Credentials; alle DNS-Adressen müssen
öffentlich sein. Socket verbindet zur geprüften IP, TLS validiert den ursprünglichen
Host. Auch Redirects werden geprüft. Keine Umgebungsproxys und keine Cookies.
robots.txt gilt vor jedem Seiten-/Redirectabruf. Unklare robots-Antwort stoppt den
Crawl. Mindestabstand, Anfrage-, Seiten-, Zeit- und Größenbudgets; Stopp bei 429/503.
Kein JavaScript, keine Webseitenbefehle. Fremdtext wird im Markdown maskiert.

## Datenschutz

Die Zielwebsite sieht IP, Zeitpunkt und User-Agent. Standardmäßig keine Drittanbieter-
Anbindung, keine Telemetrie. Berichte können URLs, Geschäftsdaten oder personenbezogene
Angaben enthalten: lokal und zugriffsbeschränkt im Kundenprojekt speichern; vor
Weitergabe prüfen. Keine sensiblen Queryparameter, authentifizierten URLs oder
privaten Daten eingeben. Aufbewahrung und Löschung entscheidet das jeweilige Projekt;
kein automatischer Löschdienst. Git ignoriert `.env*`, `.tmp/` und `reports/`.

## Grenzen und Meldungen

Kein öffentlicher Multiuser-Dienst; keine OS-Isolation. DNS-Laufzeit hängt am
Systemresolver. Die HTML-Extraktion ist konservativ, keine vollständige Browser-
Interpretation. Verdächtige Befunde mit minimalen, nicht vertraulichen Beispielen
privat an den Maintainer melden; keine Secrets oder Kundenberichte in öffentliche
Issues. Kein Security-Label als Zertifizierung verwenden.

## Akquise und CSV seit 0.2.0

Nur auftragsbezogene öffentliche Firmenrecherche. Personenbezogene Felder brauchen
einen passenden Verarbeitungsrahmen; Öffentlichkeit ist keine Werbeeinwilligung.
Keine privaten Kontakte, erratenen E-Mails, Nachrichten oder CRM-Übertragung.
Der CSV-Helfer prüft Struktur, Pflichtdaten und Dubletten, nicht deren Wahrheit.
Formelverdächtige Felder und Überschriften werden als Text markiert, UTF-8-BOM
ist Standard. Kontaktfreigabe bleibt nicht geprüft. Echte Listen ins Kundenprojekt.
