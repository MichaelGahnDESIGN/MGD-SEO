"""Validiert lokale Rechercheergebnisse und exportiert eine tabellenfreundliche CSV.

Kein Netzwerk, kein Versand, keine Prüfung von Kaufinteresse oder Werbeerlaubnis.
Frei wählbare Spalten bleiben erhalten; unbekannte Felder und Dubletten sind Fehler.
"""
import argparse
import csv
from datetime import date
import io
import json
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED = {"unternehmen", "website", "passungsgrund", "quelle_url", "geprueft_am",
            "recherche_status", "kontaktfreigabe"}
STATUSES = {"belegt", "teilweise belegt", "nicht verifiziert"}


def web_url(value):
    """Prüft nur die Quell-URL-Syntax, ohne DNS oder Abruf auszuführen."""
    try:
        part = urlsplit(value)
        if part.scheme not in ("http", "https") or not part.hostname or part.username is not None or part.password is not None:
            raise ValueError("Vollständige HTTP/HTTPS-URL ohne Zugangsdaten erforderlich")
        if any(char.isspace() or ord(char) < 32 for char in value):
            raise ValueError("Leer-/Steuerzeichen in URL")
        part.port
        return part.hostname.rstrip(".").lower().encode("idna").decode("ascii")
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Ungültige Website-/Quellen-URL") from exc


def safe_cell(value):
    """CSV-Quoting allein schützt nicht vor Tabellenformeln; Textprefix ergänzen."""
    text = "" if value is None else value
    significant = text.lstrip(" \t\r\n\v\f\ufeff\u200b\u200c\u200d")
    if (significant and significant[0] in "=+-@") or any(ord(char) < 32 for char in text[:len(text) - len(significant)]):
        return "'" + text
    if text and ord(text[0]) < 32:
        return "'" + text
    return text


def validate(data):
    """Vollständige Prüfung vor Dateianlage; gibt Spalten und normalisierte Zellen zurück."""
    if not isinstance(data, dict) or set(data) != {"columns", "leads"}:
        raise ValueError("JSON benötigt genau columns und leads")
    columns, leads = data["columns"], data["leads"]
    if not isinstance(columns, list) or not 1 <= len(columns) <= 100:
        raise ValueError("1 bis 100 Spalten erforderlich")
    if any(not isinstance(c, str) or not c.strip() or len(c) > 80 for c in columns):
        raise ValueError("Spaltennamen müssen nicht leere Texte mit höchstens 80 Zeichen sein")
    if len(set(columns)) != len(columns) or not REQUIRED <= set(columns):
        raise ValueError("Doppelte Spalten oder fehlende Pflichtspalten")
    if not isinstance(leads, list) or len(leads) > 5000:
        raise ValueError("leads muss eine Liste mit höchstens 5000 Firmen sein")
    rows, seen = [], set()
    for index, lead in enumerate(leads, 1):
        if not isinstance(lead, dict) or set(lead) - set(columns):
            raise ValueError(f"Zeile {index}: nicht deklarierte Datenfelder")
        if any(value is not None and not isinstance(value, str) for value in lead.values()):
            raise ValueError(f"Zeile {index}: Werte müssen Texte oder null sein")
        row = {column: lead.get(column) or "" for column in columns}
        if any(not row[key].strip() for key in REQUIRED):
            raise ValueError(f"Zeile {index}: Pflichtwert fehlt")
        if any(len(value) > 20000 for value in row.values()):
            raise ValueError(f"Zeile {index}: Zelle zu lang")
        domain = web_url(row["website"])
        web_url(row["quelle_url"])
        try:
            parsed_date = date.fromisoformat(row["geprueft_am"])
        except ValueError as exc:
            raise ValueError(f"Zeile {index}: Prüfdatum muss YYYY-MM-DD sein") from exc
        if parsed_date.isoformat() != row["geprueft_am"]:
            raise ValueError(f"Zeile {index}: Prüfdatum muss YYYY-MM-DD sein")
        if row["recherche_status"] not in STATUSES or row["kontaktfreigabe"] != "nicht geprüft":
            raise ValueError(f"Zeile {index}: ungültiger Status oder unzulässige Kontaktfreigabe")
        identity = (" ".join(row["unternehmen"].casefold().split()), domain)
        if identity in seen:
            raise ValueError(f"Zeile {index}: doppelte Firma; vor Export fachlich bereinigen")
        seen.add(identity)
        rows.append(row)
    return columns, rows


def render_csv(data, delimiter=";"):
    """Erzeugt reine CSV-Zeichenkette; kein Excel-Formelcode aus Rohdaten übernehmen."""
    if delimiter not in (";", ",", "\t"):
        raise ValueError("Nur Semikolon, Komma oder Tab erlaubt")
    columns, rows = validate(data)
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=delimiter, lineterminator="\r\n")
    writer.writerow([safe_cell(column) for column in columns])
    for row in rows:
        writer.writerow([safe_cell(row[column]) for column in columns])
    return output.getvalue(), len(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="MGD-Akquise – geprüfte JSON-Daten als CSV exportieren")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--delimiter", choices=("semicolon", "comma", "tab"), default="semicolon")
    parser.add_argument("--no-bom", action="store_true")
    args = parser.parse_args(argv)
    try:
        with args.input.open("rb") as source:
            payload = source.read(5_000_001)
        if len(payload) > 5_000_000:
            raise ValueError("JSON-Eingang überschreitet 5 MB")
        data = json.loads(payload.decode("utf-8-sig"))
        text, count = render_csv(data, {"semicolon":";", "comma":",", "tab":"\t"}[args.delimiter])
        with args.output.open("x", encoding="utf-8" if args.no_bom else "utf-8-sig", newline="") as target:
            target.write(text)
        print(f"CSV erstellt: {count} eindeutige Firmen; Kontaktfreigabe nicht geprüft.")
        return 0
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        parser.exit(2, "MGD-Akquise: " + str(exc) + "\n")

if __name__ == "__main__":
    raise SystemExit(main())
