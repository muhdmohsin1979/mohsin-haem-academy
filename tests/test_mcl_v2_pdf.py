from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "docs" / "mcl-v2" / "preview"
REVIEWED_MANIFEST_SHA256 = "be160f955203e33b3a72e4b9829328358568bb8ba5337eb9922fb2f8bdff95fb"


class MCLV2PDFGenerationTests(unittest.TestCase):
    def test_frozen_reviewed_preview_manifest_and_artefacts_are_exact(self) -> None:
        manifest_path = PREVIEW / "build-manifest-working.json"
        self.assertEqual(hashlib.sha256(manifest_path.read_bytes()).hexdigest(), REVIEWED_MANIFEST_SHA256)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for name, record in manifest["artefacts"].items():
            path = PREVIEW / name
            self.assertEqual(path.stat().st_size, record["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record["sha256"])

    def test_builds_pdf_pair_and_keeps_quick_reference_to_three_pages(self) -> None:
        guideline_pdf = PREVIEW / "guideline-working.pdf"
        quickref_pdf = PREVIEW / "quickref-working.pdf"
        self.assertTrue(guideline_pdf.is_file())
        self.assertTrue(quickref_pdf.is_file())

        with fitz.open(guideline_pdf) as guideline:
                guideline_text = "\n".join(page.get_text() for page in guideline)
                self.assertGreaterEqual(guideline.page_count, 8)
                self.assertIn("CONTROLLED WORKING PREVIEW", guideline_text)
                self.assertNotIn("AUTHORISED FOR PUBLICATION", guideline_text)
                treatment_titles = (
                    "Zanubrutinib monotherapy",
                    "TRIANGLE ibrutinib regimen",
                    "Pirtobrutinib monotherapy",
                    "Ibrutinib plus venetoclax",
                )
                page_texts = [page.get_text() for page in guideline]
                for treatment_title in treatment_titles:
                    title_page = next(text for text in page_texts if treatment_title in text)
                    self.assertIn("Provisional public wording", title_page, treatment_title)

        with fitz.open(quickref_pdf) as quickref:
                quickref_text = "\n".join(page.get_text() for page in quickref)
                self.assertEqual(quickref.page_count, 3)
                self.assertIn("PART 1 OF 3", quickref_text)
                self.assertIn("PART 2 OF 3", quickref_text)
                self.assertIn("PART 3 OF 3", quickref_text)
                self.assertIn("Clinical and pharmacy review pending", quickref_text)


if __name__ == "__main__":
    unittest.main()
