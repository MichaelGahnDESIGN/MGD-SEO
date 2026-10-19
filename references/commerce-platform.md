# Shops und Plattform-Builder

0.1.0 verändert keine Systeme. Im Bericht Plattform und bekannte Version nennen.
Produkte, Varianten, Filter, Kategorien und nicht lieferbare Artikel getrennt
betrachten; nicht pauschal noindex oder Löschung empfehlen.

## Vorhandene Systeme respektieren

WordPress/WooCommerce: bestehende SEO-Plugins erkennen, doppelte Canonicals und
Schema-Ausgaben vermeiden. JTL: vorhandenes MGD JTL SEO & PageSpeed zuerst prüfen.
Shopware: Verkaufskanäle, SEO-URLs und Sprachen berücksichtigen. Shopify: App und
Theme-Erweiterung sind ein eigener Integrationsweg.

## Plattform-Anschluss, geplant

Separater Adapter, der das MGD-Modulmanifest und die Capability Registry verwendet.
Vorgeschlagene Rechte: seo.project.read, seo.audit.run, seo.report.export,
seo.content.draft.write, seo.changes.apply. Prüfungen und Schreibrechte trennen.
Das Release-Evidence-Schema nicht ungeprüft als vollständiges SEO-Datenmodell nutzen.
MGD-Starter und Referenzplattform haben andere Lizenzbedingungen als die MIT-Schemas.

Vor Shopänderungen: konkreter Auftrag, Version, Staging, Backup, Rückfallweg und
Prüfung von Produktseite, Warenkorb, Checkout, Sprache und Mobilansicht.
