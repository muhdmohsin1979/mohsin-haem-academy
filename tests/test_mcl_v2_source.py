from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_mcl_v2_release import build_preview


class MCLV2PreviewGenerationTests(unittest.TestCase):
    def test_preview_generation_is_fail_closed_and_non_public(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "index.html"
            metadata = build_preview(
                source_path=ROOT / "sources" / "mcl" / "source-v2.0.html",
                status_path=ROOT / "sources" / "mcl" / "status-matrix-v2.0.json",
                state_path=ROOT / "sources" / "mcl" / "release-state-v2.0.json",
                evidence_path=ROOT / "docs" / "mcl-v2" / "evidence-ledger.json",
                claims_path=ROOT / "docs" / "mcl-v2" / "claims-matrix.json",
                output_path=output,
            )

            html = output.read_text(encoding="utf-8")
            self.assertIn('<meta name="robots" content="noindex, nofollow, noarchive">', html)
            self.assertIn("CONTROLLED WORKING PREVIEW — NOT FOR CLINICAL USE", html)
            self.assertIn("England access framework", html)
            self.assertNotIn("AUTHORISED FOR PUBLICATION", html)
            self.assertNotIn("[VERIFY]", html)
            self.assertIn('data="algorithm-working.svg"', html)
            self.assertIn('href="guideline-working.pdf"', html)
            self.assertIn('href="quickref-working.pdf"', html)
            self.assertIn('href="algorithm-working.excalidraw"', html)
            self.assertEqual(metadata["state"], "PREVIEW")
            self.assertFalse(metadata["publication_authority"])
            self.assertEqual(metadata["document_code"], "MHA-MCL-2026-v2.0")
            self.assertGreaterEqual(metadata["clinical_unit_count"], 8)
            self.assertGreaterEqual(metadata["treatment_count"], 10)

            self.assertIn('<aside class="warning" role="note"', html)
            self.assertIn('<nav aria-label="MCL preview sections">', html)
            self.assertIn('<ul class="artefact-links">', html)
            self.assertIn('id="evidence-boundary"', html)
            self.assertIn("Scientific extraction is abstract-only except where the controlled evidence ledger states otherwise.", html)
            self.assertIn('id="evidence-references"', html)
            self.assertEqual(html.count('class="evidence-reference"'), 33)
            self.assertIn('id="release-control"', html)
            self.assertIn("Publication authority", html)
            self.assertIn("FALSE", html)
            self.assertIn("MHRA SmPC —", html)
            self.assertNotIn("Official source 1", html)
            self.assertIn('<footer class="page-footer">', html)
            self.assertNotIn("data-claim-ids", html)
            self.assertIn('data-claims-supporting="C04 C05 C28 C33"', html)
            self.assertIn('data-claims-refuted="C20"', html)

            saved_metadata = json.loads((output.parent / "preview-metadata.json").read_text())
            self.assertEqual(saved_metadata, metadata)

    def test_preview_declares_mobile_safe_layout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "index.html"
            build_preview(output_path=output)
            html = output.read_text(encoding="utf-8")

            self.assertIn(".sources a { overflow-wrap:anywhere; }", html)
            self.assertIn(".status-card { background:white; border:1px solid var(--line); border-top:5px solid var(--navy); border-radius:9px; padding:1rem; overflow-wrap:anywhere; }", html)
            self.assertNotIn("body { margin:0; color:var(--ink); background:var(--paper); font:17px/1.58 Georgia,serif; overflow-wrap:anywhere; }", html)
            self.assertIn("minmax(min(310px,100%),1fr)", html)
            self.assertIn("@media (max-width:600px)", html)
            self.assertIn("font-size:clamp(1.9rem,10vw,3.4rem)", html)
            self.assertIn("aspect-ratio:1000/2050", html)
            self.assertIn(".mobile-algorithm-link { display:none", html)
            self.assertIn(".algorithm-preview { display:none; }", html)
            self.assertIn(".algorithm-caption { display:none; }", html)
            self.assertIn("Open the full-size algorithm", html)
            self.assertIn('class="skip-link" href="#main-content"', html)
            self.assertIn(":focus-visible", html)
            self.assertIn("outline:3px solid", html)


if __name__ == "__main__":
    unittest.main()
