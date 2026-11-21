# Werkzeuge, Fähigkeiten und Kosten

Stand: Recherche 20.10.2026. Beschreibungen sind keine praktische Integrationsabnahme.

| Werkzeug | Geplanter Zweck | Kosten und Grenze |
|---|---|---|
| Python-Kern | HTML-Stichprobe und lokale Dateien | Ohne Fremdpakete; implementiert |
| Firecrawl | Gerenderte Seiten für `render`, Auswertung lokal | AGPL-3.0, optional; eigener Docker kostenlos oder Cloud-Gratiskontingent mit eigenem Schlüssel; eingebaut seit 0.3.0, siehe [Anleitung](../docs/FIRECRAWL.md) |
| Scrapling | Gerenderte Inhalte und gezielte Extraktion | BSD-3-Clause, optional; nicht eingebaut |
| Lighthouse | Lokale Labormessung | Apache-2.0, optional; nicht eingebaut |
| Playwright MCP | Gezielte Browserkontrolle | Optional; vorhandenes Werkzeug bevorzugen |
| Search Console | Eigene Suchleistungsdaten | Import zuerst; API nur mit freigegebenem Lesezugriff |
| CrUX/PageSpeed | Feld- und Labordaten | Kontingente und Datenaustausch vorher prüfen |
| Ahrefs | Externe SEO-Messdaten | Kostenpflichtig; alten lokalen MCP nicht verwenden |
| DataForSEO/OpenSEO | SERP-/Keyword-Daten | Verbrauchskosten; kein Pflichtbestandteil |

## KI-Umgebungen

Codex/Claude Code können den vollständigen Skill mit lokalem Python verwenden,
wenn die jeweilige Umgebung das erlaubt. In Web-Chats nur verfügbare Werkzeuge
oder bereitgestellte Daten nutzen. Das Repo allein registriert keinen Connector.
Für Cowork sind ein Plugin-Paket, Rechteprüfung und Abnahme geplant. Lokale MCPs
in Claude-Plugins sind nicht automatisch im normalen Chat verfügbar.

## Projektwahl statt Sammelinstallation

Nur benötigte Module laden. Keine Pflichtdelegation, versteckte Werbung oder
kostenpflichtige Fallbacks. Ein Werkzeugausfall ersetzt fehlende Messwerte nicht
mit Schätzungen. OAuth und Tokens pro Nutzer/Projekt, kleinste Rechte, keine
Zugangsdaten in Git, Berichten oder Prompts.

Quellen:
- https://github.com/D4Vinci/Scrapling
- https://github.com/GoogleChrome/lighthouse
- https://github.com/microsoft/playwright-mcp
- https://docs.ahrefs.com/en/mcp/docs/introduction
- https://github.com/every-app/open-seo
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- https://learn.chatgpt.com/docs/build-skills
