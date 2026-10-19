# MGD-Akquise-Skill

B2B-Zielkunden finden, Rechercheziele im Dialog klären und eine belegte CSV erstellen.
Teil von MGD-SEO 0.2.0. Kein Versand und kein automatisches Kontaktieren.

Einstieg: [SKILL.md](SKILL.md). Der Assistent fragt Angebot, Zielkunden, Gebiet,
Umfang, Muss-/Ausschlusskriterien, Wunschdaten, Quellen und CSV-Format ab. Danach
recherchiert er mit verfügbaren Webwerkzeugen. Die CSV enthält Quellen und Prüfstatus.

Als eigener Skill: diesen gesamten Ordner unter dem Installationsnamen `mgd-akquise`
in einen erkannten Codex-/Claude-Code-Skillpfad kopieren. Der vorgegebene Quellordner
heißt bewusst `Akquise-Skill`; installierter Ordner und Frontmatter verwenden
`mgd-akquise`. Ohne Installation die SKILL.md und Referenzen als Projektmaterial nutzen.
Keine automatische Cowork-Registrierung und keine verifizierte Client-Installation.

Beispielaufforderung: „Nutze MGD-Akquise und frage mich zuerst nach meinen Zielkunden.
Ich möchte am Ende eine CSV mit Unternehmen, Website, Standort und belegtem Bedarfshinweis.“

## Exportbeispiel ohne echte Firmen

Aus dem MGD-SEO-Projektordner:

```bash
mkdir -p .tmp/akquise-beispiel
python3 -B Akquise-Skill/scripts/export_csv.py Akquise-Skill/examples/kandidaten.json --output .tmp/akquise-beispiel/kandidaten.csv
```

Die Beispieldatei enthält ausschließlich synthetische Daten und .example-Domains.
Der Helfer recherchiert nicht selbst: er validiert die vom Assistenten zusammengestellte
JSON-Datei und exportiert die CSV. Details: [CSV-Vertrag](references/csv.md).

Python 3.10+, keine Zusatzpakete. Lizenz: MIT wie das Hauptprojekt. Neue Kundenlisten
gehören ins jeweilige Kundenprojekt. Quellen und Kontaktfreigabe sind unterschiedliche Dinge.
