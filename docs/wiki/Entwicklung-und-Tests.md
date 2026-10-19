# Entwicklung und Tests

Python ab 3.10, Standardbibliothek. Aus der Projektwurzel:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B tools/check_project.py
python3 -B -m mgd_seo doctor
```

SEO-Tests verwenden synthetisches HTML, DNS-/HTTP-Attrappen und lokale Dateien.
Sie prüfen Regeln, robots, Redirects, Privatnetze, TLS-Host, Größenbudgets und
Exporte. Akquise-Tests prüfen freie Spalten, CSV-Quoting, Formelschutz,
Dubletten, Pflichtwerte und verweigertes Überschreiben.

Projektprüfung: Python-Syntax, relative Markdown-Links, Version und Changelog.
Skill-Validator kann zusätzlich verwendet werden, wenn er in der Agentenumgebung
vorhanden ist. Er prüft Format und Metadaten, keine praktische Recherchekompetenz.

GitHub-CI liegt unter `.github/workflows/check.yml`; ohne Push ist kein erfolgreicher
GitHub-Lauf belegt. Version 0.1.0 wurde lokal mit 33 Tests abgenommen, zusätzlich
mit Python 3.13.13. Aktuelle Ergebnisse im Arbeitsbericht 0.2.0 festhalten.

Neue Regeln brauchen ein begründetes beobachtbares Verhalten und aussagekräftige
Fixtures. Keine Tests, die nur kopierten Implementierungstext wiedererkennen.
Kein Live-Angriffstest und keine teuren API-Abfragen als Standardtest.
