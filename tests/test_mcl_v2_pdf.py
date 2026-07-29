from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_mcl_v2_preview import build_multiformat_preview


class MCLV2PDFGenerationTests(unittest.TestCase):
    def test_manifest_binds_every_controlled_input_and_generator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = build_multiformat_preview(Path(directory))
            manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8"))
            expected = {
                "sources/mcl/source-v2.0.html",
                "sources/mcl/status-matrix-v2.0.json",
                "sources/mcl/release-state-v2.0.json",
                "docs/mcl-v2/evidence-ledger.json",
                "docs/mcl-v2/claims-matrix.json",
                "docs/mcl-v2/access-evidence-ledger.json",
                "docs/mcl-v2/source-register.json",
                "scripts/generate_mcl_v2_release.py",
                "scripts/generate_mcl_v2_documents.py",
                "scripts/generate_mcl_v2_algorithm.py",
                "scripts/build_mcl_v2_preview.py",
            }
            self.assertEqual(set(manifest["controlled_inputs"]), expected)
            for relative_path in expected:
                path = ROOT / relative_path
                self.assertEqual(
                    manifest["controlled_inputs"][relative_path],
                    {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
                )

    def test_builds_pdf_pair_and_keeps_quick_reference_to_three_pages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = build_multiformat_preview(Path(directory))

            guideline_pdf = outputs["guideline_pdf"]
            quickref_pdf = outputs["quickref_pdf"]
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
