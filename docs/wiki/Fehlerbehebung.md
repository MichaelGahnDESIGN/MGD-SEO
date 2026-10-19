# Fehlerbehebung

| Symptom | Ursache/weiteres Vorgehen |
|---|---|
| No module named mgd_seo | Terminal in vollständiger Projektwurzel öffnen oder Paketumgebung prüfen |
| Python zu alt | unterstützten Interpreter ab 3.10 wählen |
| File exists | Export verweigert Überschreiben; anderen Dateinamen nehmen |
| No such file or directory | Eingang/Zielordner prüfen und Ausgabeordner ausdrücklich anlegen |
| Privat-/reserviertes Ziel | Schutzgrenze; kein lokales Intranet-/Admin-Crawl mit diesem Kern |
| Redirect verlässt Ursprung | beabsichtigte Endadresse prüfen, dort neu beginnen |
| Redirect-Limit | Weiterleitungskette/Serververhalten prüfen; nicht pauschal Schutz abschalten |
| robots nicht abrufbar | Rechte/Erreichbarkeit klären; Crawl wurde nicht durchgeführt |
| HTTP 429/503 | Server verlangt Pause/ist nicht verfügbar; nicht automatisch weiter belasten |
| Kein HTML/komprimiert | Inhaltstyp/Encoding prüfen; keine Aussage über SEO der ungelesenen Seite |
| Keine DOM-Inhalte | JS-Rendering nicht Teil des Kerns |
| CSV: Pflichtfeld fehlt | vereinbarte Pflichtspalten und vollständige Werte prüfen |
| CSV: doppelte Firma | Quelle und Identität fachlich bereinigen |
| CSV: Kontaktfreigabe | Feld muss `nicht geprüft` sein; CSV ist keine Versandfreigabe |

Fehlermeldung, Befehl, Python-Version und redigiertes Minimalbeispiel aufbewahren.
Keine Zugangsdaten, privaten URLs oder echten Kundenlisten in öffentliche Issues.
Offline-Fixture und `doctor` grenzen Umgebung von Zielwebsite ab.
