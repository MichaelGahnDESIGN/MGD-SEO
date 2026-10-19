"""CLI-Verhalten einschließlich lokaler Exporte und Nichtüberschreiben prüfen."""
import contextlib
import io
import json
import unittest
from unittest.mock import mock_open, patch
from mgd_seo.cli import main
from mgd_seo.report import markdown
from mgd_seo.crawl import new_report

class CliTests(unittest.TestCase):
    def test_offline_json(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            result=main(["html","tests/fixtures/example.html","--url","https://example.org/","--format","json"])
        report=json.loads(out.getvalue())
        self.assertEqual(result,0)
        self.assertIsNone(report["pages"][0]["http_status"])
        self.assertEqual(report["pages"][0]["findings"],[])
        self.assertIn("nicht gemessen",markdown(report))

    def test_existing_export_not_overwritten(self):
        # README existiert; exklusives Öffnen muss scheitern, bevor geschrieben wird.
        err=io.StringIO()
        with contextlib.redirect_stderr(err),self.assertRaises(SystemExit) as caught:
            main(["html","tests/fixtures/example.html","--url","https://example.org/","--output","README.md"])
        self.assertEqual(caught.exception.code,2)

    def test_invalid_url_exit(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as caught:
            main(["html","tests/fixtures/example.html","--url","file:///a"])
        self.assertEqual(caught.exception.code,2)

    def test_doctor(self):
        with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(main(["doctor"]),0)

    def test_crawl_partial_report_exit(self):
        report=new_report("crawl")
        report["errors"]=[{"url":"https://example.org/","message":"Testfehler"}]
        out=io.StringIO()
        with patch("mgd_seo.cli.crawl",return_value=report),contextlib.redirect_stdout(out):
            self.assertEqual(main(["crawl","https://example.org/","--format","json"]),2)
        self.assertTrue(json.loads(out.getvalue())["errors"])

if __name__ == "__main__": unittest.main()
