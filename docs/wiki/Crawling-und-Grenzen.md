# Crawling und Grenzen

Die Prüfung beginnt bei robots.txt des Startursprungs. HTTP 200 wird mit Pythons
`urllib.robotparser` ausgewertet, 404/410 bedeuten keine dort gefundenen Regeln.
Andere Statuscodes oder Abruffehler stoppen die Prüfung. Der Parser ist keine
vollständige Nachbildung von Googlebot oder sämtlichen robots.txt-Dialekten.

| Grenze | Wert/Verhalten |
|---|---|
| Seitenkandidaten | Standard 10, maximal 50; auch Sperren zählen zum Kandidatenlimit |
| Anfragenbudget | `2 * max_pages + 10`, einschließlich robots/Redirects |
| Ziel | derselbe Ursprung aus Schema, Host und Port |
| Ports | HTTP 80, HTTPS 443 |
| Antwortgröße | maximal 2.000.000 Bytes |
| Abrufbudget | 120 Sekunden; DNS zusätzlich systemabhängig |
| Socket-Timeout | bis zu 10 Sekunden, durch Restbudget begrenzt |
| Mindestabstand | 0,5 Sekunden; erkannter Crawl-delay kann ihn verlängern |
| Redirects | höchstens fünf Weiterleitungen, Ziel vor Abruf geprüft |
| Überlastung | HTTP 429/503 stoppt Crawl |

Keine Parallelabrufe, keine automatisch verfolgten Query-URLs; eine ausdrücklich
angegebene Start-URL darf Queryparameter enthalten. Fragmente werden entfernt.
Sitemap-Adressen aus robots.txt werden nur aufgelistet. Komprimierte Antworten
werden abgelehnt. Keine Logins, Cookies oder Proxyübernahme aus der Umgebung.

HTTPS-/www-Wechsel sind andere Ursprünge und werden gestoppt. Die beabsichtigte
Endadresse als neuen Start wählen. Privatnetze bleiben gesperrt. Kein Browser-
Rendering und keine zugesicherte Prozessisolation für einen öffentlichen SaaS-Dienst.
