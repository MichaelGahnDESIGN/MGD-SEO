# Wiki pflegen und später veröffentlichen

Quelle ist `docs/wiki/` im Projekt. Alle Seiten sind Markdown mit lokal auflösbaren
`.md`-Links. `Home.md` ist die Startseite; `_Sidebar.md` und `_Footer.md` sind die
GitHub-Wiki-Navigationsdateien. Keine Kundenberichte in das Wiki aufnehmen.

## Lokale Prüfung und Export

```bash
python3 -B tools/check_project.py
python3 -B tools/export_wiki.py --output .tmp/wiki-export
```

Der Export erzeugt einen neuen Ordner, verweigert bestehende Ziele und wandelt
interne `.md`-Links in GitHub-Wiki-Seitennamen um. Er enthält alle Wiki-Seiten,
keine Projektdateien, keinen Netzwerkzugriff und keinen Push. Links vorher prüfen.

## Veröffentlichung als gesonderter Auftrag

Derzeit ist kein Remote eingerichtet. Vor Veröffentlichung Repositoryidentität,
Sichtbarkeit, Zugriffsrechte und Freigabe klären. GitHub-Wikis besitzen ein eigenes
Git-Repository neben dem Code-Repository. Eine erste Wiki-Seite muss gegebenenfalls
auf GitHub angelegt werden. Erst danach dessen Wiki-Repository beziehen, exportierte
Seiten vergleichen, Änderungen reviewen und mit eigener Freigabe übertragen.

Kein erzwungener Push, kein Löschen fremder Seiten und keine Geheimnisse in
Git-Remotes. Eine lokale Wiki-Datei bedeutet noch keine veröffentlichte Seite.
Nach Veröffentlichung Navigation und Inhalt im tatsächlichen GitHub-Wiki prüfen.

GitHub-Dokumentation:
https://docs.github.com/en/communities/documenting-your-project-with-wikis/creating-a-footer-or-sidebar-for-your-wiki
