"""Synthetische B2B-Daten prüfen; keine wirklichen Kontakte oder Webrecherche."""
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mgd_acquisition_export", ROOT / "Akquise-Skill/scripts/export_csv.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def dataset():
    return json.loads((ROOT/"Akquise-Skill/examples/kandidaten.json").read_text())


class AcquisitionTests(unittest.TestCase):
    def test_custom_columns_preserved_in_order(self):
        data=dataset()
        data["columns"].insert(0,"wunschfeld")
        data["leads"][0]["wunschfeld"]='Wert; mit "Zitat"\nzweite Zeile'
        text,count=module.render_csv(data)
        rows=list(csv.reader(io.StringIO(text),delimiter=";"))
        self.assertEqual(count,1)
        self.assertEqual(rows[0][0],"wunschfeld")
        self.assertEqual(rows[1][0],data["leads"][0]["wunschfeld"])

    def test_missing_optional_is_empty(self):
        data=dataset()
        del data["leads"][0]["telefon_zentrale"]
        text,_=module.render_csv(data)
        rows=list(csv.reader(io.StringIO(text),delimiter=";"))
        self.assertEqual(rows[1][rows[0].index("telefon_zentrale")],"")

    def test_unknown_field_not_silently_discarded(self):
        data=dataset(); data["leads"][0]["neues_feld"]="Wert"
        with self.assertRaises(ValueError): module.render_csv(data)

    def test_formula_protection(self):
        for value in ('=1+1',' +491234','-1+1','@SUM(A1)','\t=1+1','\r=1+1','\ufeff=1+1','\u200b=1+1'):
            with self.subTest(value=value): self.assertTrue(module.safe_cell(value).startswith("'"))
        self.assertEqual(module.safe_cell("Normale Firma"),"Normale Firma")

    def test_formula_header_protected(self):
        data=dataset(); data["columns"].append("=1+1")
        text,_=module.render_csv(data)
        self.assertIn("'=1+1",text.splitlines()[0])

    def test_duplicate_company_rejected(self):
        data=dataset(); other=dict(data["leads"][0]); other["website"]+="leistung?x=1"
        other["unternehmen"]="  "+other["unternehmen"].upper()+" "
        data["leads"].append(other)
        with self.assertRaises(ValueError): module.render_csv(data)

    def test_shared_domain_different_company_kept(self):
        data=dataset(); other=dict(data["leads"][0]); other["unternehmen"]="Andere Beispielfirma"
        data["leads"].append(other)
        self.assertEqual(module.render_csv(data)[1],2)

    def test_bad_dates_and_permission_rejected(self):
        for key,value in [("geprueft_am","20.10.2026"),("geprueft_am","2026-02-30"),("kontaktfreigabe","ja"),("recherche_status","kaufbereit"),("quelle_url","https://user:secret@example.org/")]:
            data=dataset(); data["leads"][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): module.render_csv(data)

    def test_missing_required_rejected(self):
        data=dataset(); del data["leads"][0]["passungsgrund"]
        with self.assertRaises(ValueError): module.render_csv(data)

    def test_non_scalar_rejected(self):
        data=dataset(); data["leads"][0]["ort"]=["Stadt"]
        with self.assertRaises(ValueError): module.render_csv(data)

    def test_empty_result_is_header_only(self):
        data=dataset(); data["leads"]=[]
        text,count=module.render_csv(data)
        self.assertEqual(count,0)
        self.assertEqual(len(list(csv.reader(io.StringIO(text),delimiter=";"))),1)

    def test_comma_and_tab_roundtrip(self):
        for sep in (",","\t"):
            text,count=module.render_csv(dataset(),sep)
            self.assertEqual(len(list(csv.reader(io.StringIO(text),delimiter=sep))),2)

    def test_existing_file_never_overwritten(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as caught:
            module.main([str(ROOT/"Akquise-Skill/examples/kandidaten.json"),"--output",str(ROOT/"README.md")])
        self.assertEqual(caught.exception.code,2)

    def test_duplicate_columns_rejected(self):
        data=dataset(); data["columns"].append("unternehmen")
        with self.assertRaises(ValueError): module.render_csv(data)

    def test_limits(self):
        data=dataset(); data["leads"][0]["ort"]="a"*20001
        with self.assertRaises(ValueError): module.render_csv(data)

if __name__ == "__main__": unittest.main()
