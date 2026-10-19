# MGD-Plattform-Builder

MGD-SEO funktioniert eigenständig. Eine spätere Plattformintegration ist ein
separates Adaptermodul, keine Pflicht für Nutzer des Skills.

Bereits vorhandene Bausteine des Builders: Projektprofile, Modulmanifest,
Capability Registry, Datenklassifikation, Release-Nachweise und Governance.
Das Release-Evidence-Schema ist nicht automatisch ein vollständiges SEO-Datenmodell.

Vorgeschlagene Rechte: `seo.project.read`, `seo.audit.run`, `seo.report.export`,
`seo.content.draft.write`, `seo.changes.apply`. Lesen und Schreiben trennen;
keine allgemeinen Adminrechte. Akquise-Listen und Ausschlüsse müssen projektbezogen
bleiben. Eine UI-Trennung allein schützt keine Mandanten.

Für eine spätere SEO-Plattform kommen Aufträge, Verlauf und Aufgaben hinzu.
Benutzerverwaltung, Abrechnung, Warteschlangen, Egress-Regeln und isolierte Jobs
sind eigene Betriebsentscheidungen. Keine lokalen Scraper ungeprüft öffentlich anbieten.

Lizenzgrenzen des Builders beachten: MIT-Werkzeuge und MGD-lizenzierte Starter/
Referenzplattform nicht gleichsetzen. Der lokale Builder-Bestand wurde nicht verändert.
https://github.com/MichaelGahnDESIGN/MGD-Plattform-Builder

Weiter: [Architektur](Architektur.md), [Roadmap](Versionen-und-Roadmap.md).
