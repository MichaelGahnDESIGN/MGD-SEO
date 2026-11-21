# Firecrawl mit MGD-SEO nutzen

Stand: 21.11.2026 · ab MGD-SEO 0.3.0 · optional

## Wofür ist das?

Manche Webseiten bauen ihren Inhalt erst im Browser mit JavaScript auf.
Der normale Befehl `crawl` sieht dann nur eine leere Hülle.

**Firecrawl** öffnet die Seite wie ein Browser und gibt das fertige HTML zurück.
MGD-SEO prüft dieses HTML danach **lokal auf deinem Rechner**.

## Warum spart das Tokens?

- Die KI bekommt **nie** das ganze HTML einer Seite (das wären oft 50.000 Tokens und mehr).
- Sie bekommt nur den fertigen Bericht. Mit `--format compact` ist das **eine Zeile pro Befund**.
- Mit `--cache` wird jede Seite 24 Stunden lang gespeichert. Ein zweiter Lauf kostet keinen neuen Abruf.
- Standard sind höchstens **5 Seiten** pro Lauf (einstellbar bis 25).

## Kostenlos nutzen: zwei Wege

| Weg | Kosten | Schlüssel nötig? | Für wen? |
|---|---|---|---|
| **A: Eigener Firecrawl mit Docker** (empfohlen) | 0 € | nein | Wenn Docker Desktop läuft |
| **B: Firecrawl-Cloud, Gratis-Kontingent** | 0 € bis zum Kontingent | ja, eigener Schlüssel | Ohne Docker |

Firecrawl selbst ist Open Source (Lizenz AGPL-3.0). MGD-SEO enthält **keinen** Firecrawl-Code.
Es ruft nur dessen Schnittstelle auf.

### Weg A: Eigener Firecrawl mit Docker (Schritt für Schritt)

1. Docker Desktop starten.
2. Im Terminal einen Ordner **außerhalb** von MGD-SEO wählen und Firecrawl holen:

   ```bash
   git clone https://github.com/firecrawl/firecrawl.git
   cd firecrawl
   ```

3. Auf das neueste Release wechseln. Das steht unter https://github.com/firecrawl/firecrawl/releases, zum Beispiel:

   ```bash
   git checkout v2.11.0
   ```

4. Im Ordner `firecrawl` eine Datei `.env` anlegen. Inhalt (das Passwort durch einen langen Zufallswert ersetzen):

   ```text
   USE_DB_AUTHENTICATION=false
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=HIER-LANGES-ZUFALLSPASSWORT
   POSTGRES_DB=postgres
   ```

5. Starten (das erste Mal dauert einige Minuten):

   ```bash
   docker compose up --build -d
   ```

6. Fertig. Firecrawl läuft jetzt unter `http://localhost:3002`. MGD-SEO nutzt diese Adresse automatisch.

Stoppen mit `docker compose down` im Ordner `firecrawl`.

⚠️ Diese Einrichtung ist nur für deinen eigenen Rechner gedacht. Den Port 3002 nicht ins Internet freigeben.
Die offizielle Anleitung steht unter https://docs.firecrawl.dev/contributing/self-host.

### Weg B: Firecrawl-Cloud mit Gratis-Kontingent

1. Auf https://www.firecrawl.dev ein kostenloses Konto anlegen und einen API-Schlüssel erstellen.
2. Den Schlüssel **nur** im Terminal setzen, nie in eine Datei im Repository:

   ```bash
   export MGD_SEO_FIRECRAWL_URL=https://api.firecrawl.dev
   export FIRECRAWL_API_KEY=fc-DEIN-SCHLÜSSEL
   ```

3. Jede geprüfte Seite verbraucht Guthaben aus dem Gratis-Kontingent. Darum `--cache` und kleine `--max-pages` nutzen.

## Benutzen

Erst prüfen, ob alles eingestellt ist:

```bash
python3 -B -m mgd_seo doctor
```

Dann eine Seite gerendert prüfen:

```bash
python3 -B -m mgd_seo render https://DEINE-DOMAIN.example/ --format compact --cache .tmp/firecrawl
```

| Option | Bedeutung |
|---|---|
| `--max-pages 5` | Wie viele Seiten höchstens (1 bis 25) |
| `--format compact` | Kurzbericht, spart Tokens (für KI-Agenten) |
| `--format markdown` | Ausführlicher Bericht für Menschen |
| `--format json` | Rohdaten für andere Programme |
| `--cache ORDNER` | Seiten 24 Stunden lang speichern |

## Was MGD-SEO dabei absichert

- robots.txt wird **vorher** von MGD-SEO selbst gelesen. Gesperrte Seiten gehen nicht an Firecrawl.
- Interne Adressen (zum Beispiel `localhost` oder `192.168.…`) werden nie an Firecrawl gegeben.
  Das ist eine **Vorprüfung, kein vollständiger Schutz** (siehe Warnung unten).
- Pause zwischen den Seiten (mindestens 0,5 Sekunden oder `Crawl-delay` aus robots.txt). Bei HTTP 429/503 stoppt der Lauf.
- Ein Lauf dauert höchstens 5 Minuten. Fällt Firecrawl aus oder ist das Kontingent leer, stoppt der Lauf sofort.

⚠️ **Wichtig beim eigenen Docker-Firecrawl (Weg A):** Firecrawl ruft die Seite selbst ab und führt dabei
deren JavaScript aus. Eine präparierte Webseite könnte so versuchen, Geräte in deinem Heimnetz anzusprechen
(Router, NAS, andere Docker-Dienste). MGD-SEO kann das nicht vollständig verhindern.

So bleibst du sicher:

1. Im Weg A nur **eigene oder bekannte Websites** prüfen (zum Beispiel Kunden-Shops mit Auftrag).
2. Für fremde oder unbekannte Websites den normalen `crawl` (ohne JavaScript) oder Weg B (Cloud) nutzen.
   In der Cloud läuft der Abruf bei Firecrawl, nicht in deinem Netz.
3. Wer Weg A für alles nutzen will: Firecrawl auf einem eigenen Rechner oder in einer VM ohne Zugang
   zum Heimnetz betreiben (eigenes Netz, Firewall lässt nur Internet-Adressen zu).
- Firecrawl-Adresse: nur `http://localhost:<port>` oder `https://api.firecrawl.dev`. Andere Ziele werden abgelehnt.
- Der Schlüssel erscheint nie in Berichten oder Fehlermeldungen.
- Fällt Firecrawl aus, stoppt der Lauf mit einer Fehlermeldung. Dann geht der normale `crawl` weiter (ohne JavaScript).

## Grenzen

- Ob JavaScript wirklich ausgeführt wurde, entscheidet die Firecrawl-Engine. Bei Zweifel eine Seite im Browser gegenprüfen.
- HTTP-Header wie `X-Robots-Tag` liefert Firecrawl nicht mit. Dafür den normalen `crawl` nutzen.
- Keine Logins, keine Formulare, keine Screenshots.
