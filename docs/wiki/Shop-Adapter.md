# WordPress, JTL, Shopware und Shopify

Aktuell prüft der Kern öffentliches HTML systemunabhängig. Es gibt keine eingebaute
Admin-Anbindung und keine automatische Änderung eines Shops.

| System | Geplanter Adapter und wichtige Grenzen |
|---|---|
| WordPress/WooCommerce | bestehende SEO-Plugins erkennen, doppelte Metadaten/Schema vermeiden |
| JTL-Shop | vorhandenes MGD JTL SEO & PageSpeed zuerst prüfen und weiterentwickeln |
| Shopware | SEO-URLs, Verkaufskanäle, Varianten und Sprachen berücksichtigen |
| Shopify | App/Theme-Erweiterung, eigene Rechte und Veröffentlichungswege |

Produkte, Kategorien, Filter und Varianten brauchen unterschiedliche Empfehlungen.
Nicht lieferbar bedeutet nicht automatisch löschen oder noindex. Keine pauschale
JavaScript-Verzögerung, die Variantenwahl, Warenkorb oder Checkout beschädigt.

Das bestehende JTL-Projekt ist eine Quelle, keine hier getestete Installation:
https://github.com/MichaelGahnDESIGN/MGD_JTL-SEO-Plugin
Vor Übernahme aktuelle Version, Lizenz, Kompatibilität und Quellstand prüfen.

Jede spätere Umsetzung braucht Zielversion, Staging, Backup, Rückfallweg und Tests
von Produktseite, Suche/Filtern, Warenkorb, Checkout, Sprache und Mobilansicht.
Kundendaten werden für öffentliche SEO-Prüfung nicht benötigt.
