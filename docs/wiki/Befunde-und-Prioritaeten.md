# Befunde und Prioritäten

Ein Befund enthält Regel-ID, URL, beobachteten Nachweis, Priorität, Einordnung,
Empfehlung und Nachtest. Der Prüfzeitpunkt steht im umgebenden Bericht.

`certainty: belegt` bedeutet: die beschriebene Beobachtung ist in den Eingangsdaten
vorhanden. Daraus folgt keine bewiesene Rankingwirkung. `Hinweis` fordert eine
Kontextprüfung, etwa bei mehreren H1 oder noindex.

| Einordnung | Beispiel | Nächster Schritt |
|---|---|---|
| Hoch | öffentliche Zielseite liefert HTTP 404 | Absicht und Erreichbarkeit prüfen |
| Mittel | Produktseiten teilen denselben Titel | Suchintention und Titelvorlage prüfen |
| Hinweis | Canonical fehlt im HTML | weitere Kanonisierungssignale prüfen |
| Nicht geprüft | JavaScript-DOM, Suchleistung | gesonderte Messung einplanen |
| Nicht anwendbar | Produkt-Schema bei Kontaktseite | begründet ausschließen |

Die letzten beiden Zustände formuliert der Assistent im Berichtskontext; der
Python-Kern erzeugt dafür nicht automatisch einzelne Regel-Befunde.

Vorher-/Nachher-Vergleich: gleiche URLs, Regeln und Datenquelle. Keinen Erfolg
behaupten, wenn die betroffene Seite im zweiten Lauf übersprungen wurde. Maßnahmen
nach Risiko und geschäftlicher Bedeutung priorisieren, nicht allein nach Anzahl.

Weiter: [Prüfregeln](Pruefregeln.md), [SEO-Ablauf](SEO-Arbeitsablauf.md).
