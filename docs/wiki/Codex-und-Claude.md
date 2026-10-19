# Codex und Claude

Der gemeinsame Skill-Einstieg steht in `SKILL.md`, Fachwissen unter `references/`.
Der Akquise-Unterordner enthält einen zweiten Skill mit dem Namen `mgd-akquise`.

| Umgebung | Nutzung und Grenze |
|---|---|
| Codex | Vollständiger Ordner in einem erkannten Skillpfad, z. B. `~/.agents/skills/mgd-seo/`; Aufruf `$mgd-seo` |
| Claude Code | Vollständiger Ordner unter `~/.claude/skills/mgd-seo/`; Aufruf `/mgd-seo` |
| Separater Akquise-Skill | Inhalt von `Akquise-Skill/` als Ordner `mgd-akquise` installieren |
| Cowork | Eigenes Paket und Client-Abnahme geplant; kein automatischer Import durch Skillordner |
| ChatGPT/Claude ohne Shell | Skilltexte und bereitgestellte Berichte auswerten; lokaler Python-Aufruf nicht automatisch möglich |

Den vorgegebenen Quellordner `Akquise-Skill` für die separate Installation in
`mgd-akquise` umbenennen. Eine verschachtelte SKILL.md wird nicht von jedem Client
automatisch entdeckt; der SEO-Skill kann sie aber gezielt lesen.

Alle Pfade sind Installationsbeispiele, keine automatisch ausgeführten Änderungen.
Aufruf, Dateizugriff und Werkzeuge hängen von der Umgebung ab. Verfügbarkeit prüfen,
keine Shell-, Browser- oder MCP-Funktionen erfinden. Bestehende Autorisierung und
Projektregeln gelten weiter. Keine Tokens in Skilldateien hinterlegen.

Referenz: https://learn.chatgpt.com/docs/build-skills und
https://support.claude.com/en/articles/13837440-use-plugins-in-claude

Weiter: [Integrationen](Integrationen-und-Kosten.md), [MGD-Akquise](MGD-Akquise.md).
