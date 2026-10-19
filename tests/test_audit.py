"""Reproduzierbare fachliche Prüfungen ohne Netzwerk oder Kundendaten."""
import unittest
from mgd_seo.audit import analyze, add_site_findings
from mgd_seo.report import markdown
from mgd_seo.crawl import new_report

GOOD = '<html lang="de"><head><title>Gut</title><meta name="description" content="Beschreibung"><link rel="canonical" href="/x"></head><body><h1>Gut</h1><img alt=""></body></html>'

def rules(page):
    return {item["rule"] for item in page["findings"]}

class AuditTests(unittest.TestCase):
    def test_valid_page_and_relative_canonical(self):
        page, _ = analyze("https://example.org/", GOOD)
        self.assertEqual(page["findings"], [])
        self.assertEqual(page["canonical"], ["https://example.org/x"])

    def test_missing_fields(self):
        page, _ = analyze("https://example.org/", '<img src="a">')
        self.assertTrue({"title", "description", "h1-missing", "language-missing", "image-alt"} <= rules(page))

    def test_duplicate_metadata_and_canonical(self):
        page, _ = analyze("https://example.org/", GOOD + '<title>Zwei</title><link rel="canonical" href="/y">')
        self.assertTrue({"title", "canonical-multiple"} <= rules(page))

    def test_multiple_h1_is_hint(self):
        page, _ = analyze("https://example.org/", GOOD + '<h1>Zwei</h1>')
        finding = next(item for item in page["findings"] if item["rule"] == "h1-multiple")
        self.assertEqual(finding["certainty"], "Hinweis")

    def test_noindex_header_and_html(self):
        for html, headers in [(GOOD, {"x-robots-tag": "noindex, follow"}), (GOOD + '<meta name="robots" content="noindex">', {})]:
            page, _ = analyze("https://example.org/", html, headers=headers)
            self.assertIn("noindex", rules(page))

    def test_jsonld_invalid(self):
        page, _ = analyze("https://example.org/", GOOD + '<script type="application/ld+json">{bad}</script>')
        self.assertIn("jsonld-syntax", rules(page))

    def test_jsonld_invalid_newline_not_normalized_away(self):
        page, _ = analyze("https://example.org/", GOOD + '<script type="application/ld+json">{"x":"a\nb"}</script>')
        self.assertIn("jsonld-syntax", rules(page))

    def test_duplicate_titles_in_sample(self):
        pages = [analyze("https://example.org/" + part, GOOD)[0] for part in ("a", "b")]
        add_site_findings(pages)
        self.assertTrue(all("duplicate-title" in rules(page) for page in pages))

    def test_report_escapes_active_content(self):
        page, _ = analyze("https://example.org/", '<title>&lt;img src=x&gt; ![x](https://tracker.example/)</title>')
        report = new_report("test")
        page["findings"].append({"rule":"x", "priority":"hinweis", "certainty":"Hinweis", "evidence":page["title"], "recommendation":"prüfen"})
        report["pages"] = [page]
        text = markdown(report)
        self.assertNotIn("<img", text)
        self.assertNotIn("![x]", text)

if __name__ == "__main__":
    unittest.main()
