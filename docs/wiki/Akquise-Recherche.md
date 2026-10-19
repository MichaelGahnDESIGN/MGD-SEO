# Akquise-Recherche und Datenqualität

Branchen-/Regionsbegriffe mit passenden Zielmerkmalen kombinieren. Suchtreffer liefern
Kandidaten. Aussagen vorzugsweise auf Firmenwebsite, Leistungsseite oder belastbaren
Originalquellen prüfen. Zeitstand und bei Kennzahlen Bezugsjahr festhalten.

Eine CSV-Zeile braucht Unternehmensidentität, Website, Passungsgrund, Quellen-URL,
Prüftag und Recherche-Status. Zusatzfelder benötigen eigene Nachweise, etwa als
Feld→Quelle-Zuordnung in `quellen_details`. Fehlende Werte bleiben leer.

| Status | Aussage |
|---|---|
| belegt | erfasste Passungskriterien sind belegt |
| teilweise belegt | relevante Kriterien/Daten bleiben offen |
| nicht verifiziert | Kandidat, noch kein bestätigter Treffer |

Unbestätigte Kandidaten nur auf Wunsch als solche aufnehmen. Keine Umsätze,
Mitarbeiterzahlen, Rankings, Budgets oder E-Mail-Adressen erraten. SEO-Beobachtung
und vermutete Verkaufschance getrennt beschreiben. Keine falsche Vollständigkeit,
wenn das Zeitlimit vor der gewünschten Firmenzahl erreicht ist.

Dubletten fachlich prüfen: Firmen können mehrere Domains/Standorte haben. Mehrere
Firmen können eine Domain teilen. Der Exporthelfer erkennt nur identischen
normalisierten Firmennamen plus Domain und verweigert dann den Export.

Öffentliche Kontaktdaten sind keine Kontaktfreigabe. Keine privaten Angaben,
Login-Scraping, CAPTCHA-Umgehung oder automatischen Werbenachrichten. Kundenseitige
Ausschlusslisten lokal berücksichtigen. [Datenschutz](Datenschutz-und-Sicherheit.md).
