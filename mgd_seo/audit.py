"""Deterministische Beobachtungen; keine Rankingprognosen oder erfundenen Scores."""
import json
from .html import PageParser


def analyze(url, html, status=200, headers=None):
    page = PageParser(url)
    page.feed(html)
    findings = []
    def add(rule, priority, evidence, recommendation, certainty="belegt"):
        findings.append({"rule": rule, "priority": priority, "certainty": certainty,
                         "url": url, "evidence": evidence, "recommendation": recommendation,
                         "verification": "Dieselbe URL nach der Änderung erneut abrufen und den dokumentierten Nachweis vergleichen; DOM und Suchleistungsdaten bei Bedarf separat prüfen."})
    if status >= 400:
        add("http-error", "hoch", f"HTTP {status}", "Erreichbarkeit und beabsichtigten Seitenstatus prüfen.")
    if len(page.titles) != 1 or not page.titles[0]:
        add("title", "mittel", f"Title-Elemente: {len(page.titles)}", "Einen aussagekräftigen Seitentitel ausgeben.")
    if len(page.descriptions) != 1 or not page.descriptions[0]:
        add("description", "mittel", f"Description-Elemente: {len(page.descriptions)}", "Eine passende Beschreibung prüfen; kein garantierter Rankingfaktor.")
    if len(page.canonicals) > 1:
        add("canonical-multiple", "hoch", page.canonicals, "Widersprüchliche Canonicals vermeiden.")
    elif not page.canonicals:
        add("canonical-missing", "hinweis", "Kein HTML-Canonical gefunden", "Beabsichtigte URL-Kanonisierung einschließlich HTTP-Link-Header prüfen.", "Hinweis")
    if not page.headings:
        add("h1-missing", "mittel", "Keine H1 im Quell-HTML", "Eine verständliche Hauptüberschrift prüfen; gerenderten DOM bei JavaScript gesondert ansehen.")
    elif len(page.headings) > 1:
        add("h1-multiple", "hinweis", f"H1-Anzahl: {len(page.headings)}", "Inhaltliche Hierarchie prüfen; mehrere H1 sind kein automatischer Rankingfehler.", "Hinweis")
    if not page.lang:
        add("language-missing", "hinweis", "html lang fehlt", "Sprache für Browser und assistive Werkzeuge angeben.", "Hinweis")
    if page.images_missing_alt:
        add("image-alt", "mittel", f"Bilder ohne alt-Attribut: {page.images_missing_alt}", "Inhaltsbilder beschreiben; dekorative Bilder mit leerem alt kennzeichnen.")
    robots = page.robots + [(headers or {}).get("x-robots-tag", "").lower()]
    if any("noindex" in value.replace(";", ",").replace(" ", ",").split(",") for value in robots):
        add("noindex", "hinweis", robots, "Prüfen, ob der Indexierungsausschluss beabsichtigt ist; kein Beweis tatsächlicher Deindexierung.", "Hinweis")
    for index, block in enumerate(page.jsonld):
        try:
            json.loads(block)
        except (ValueError, RecursionError):
            add("jsonld-syntax", "mittel", f"JSON-LD-Block {index + 1} ist syntaktisch ungültig", "JSON-Syntax korrigieren; semantische Validierung separat durchführen.")
    result = {"url": url, "http_status": status, "title": page.titles,
              "description": page.descriptions, "canonical": page.canonicals,
              "h1": page.headings, "findings": findings}
    return result, page.links


def add_site_findings(pages):
    """Doppelte Titel nur innerhalb der tatsächlich gelesenen Stichprobe melden."""
    titles = {}
    for page in pages:
        if len(page["title"]) == 1 and page["title"][0]:
            titles.setdefault(page["title"][0].casefold(), []).append(page)
    for group in titles.values():
        if len(group) > 1:
            urls = [page["url"] for page in group]
            for page in group:
                page["findings"].append({"rule": "duplicate-title", "priority": "mittel", "certainty": "belegt",
                    "url": page["url"], "evidence": urls,
                    "recommendation": "Prüfen, ob diese Seiten unterschiedliche Suchintentionen bedienen und eigene Titel brauchen.",
                    "verification": "Dieselben Seiten erneut prüfen und die Titelgruppen vergleichen."})
