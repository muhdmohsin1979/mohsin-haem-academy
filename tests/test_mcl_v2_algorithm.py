from __future__ import annotations

import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_mcl_v2_algorithm import build_algorithm, canonical_semantic_texts


class MCLV2AlgorithmGenerationTests(unittest.TestCase):
    def test_svg_and_excalidraw_are_exact_renderings_of_one_semantic_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = build_algorithm(Path(directory))
            expected = {key: " ".join(value.split()) for key, value in canonical_semantic_texts().items()}

            svg_root = ET.fromstring(outputs["svg"].read_text(encoding="utf-8"))
            svg_values = {
                element.attrib["data-semantic-id"]: " ".join(" ".join(element.itertext()).split())
                for element in svg_root.iter()
                if "data-semantic-id" in element.attrib
            }
            excalidraw = json.loads(outputs["excalidraw"].read_text(encoding="utf-8"))
            editable_values = {
                element["customData"]["semanticId"]: " ".join(str(element["text"]).split())
                for element in excalidraw["elements"]
                if element.get("type") == "text" and element.get("customData", {}).get("semanticId")
            }

            self.assertEqual(svg_values, expected)
            self.assertEqual(editable_values, expected)

    def test_builds_editable_and_rendered_preview_algorithm(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = build_algorithm(Path(directory))
            svg = outputs["svg"].read_text(encoding="utf-8")
            excalidraw = json.loads(outputs["excalidraw"].read_text(encoding="utf-8"))

            self.assertIn("MCL v2.0 treatment decision algorithm", svg)
            self.assertIn("WORKING PREVIEW", svg)
            self.assertIn("TP53-MUTATED / HIGH RISK", svg)
            self.assertIn("COVALENT-BTKi PROGRESSION", svg)
            self.assertIn("TA677 CDF MANAGED ACCESS", svg)
            self.assertNotIn("AUTHORISED FOR PUBLICATION", svg)
            self.assertNotIn("PUBLISHED v2.0", svg)

            self.assertEqual(excalidraw["type"], "excalidraw")
            self.assertGreaterEqual(len(excalidraw["elements"]), 40)
            excalidraw_text = json.dumps(excalidraw)
            self.assertIn("WORKING PREVIEW", excalidraw_text)
            self.assertNotIn("AUTHORISED FOR PUBLICATION", excalidraw_text)

    def test_rendered_algorithm_wraps_lower_route_panels_and_connects_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = build_algorithm(Path(directory))
            svg = outputs["svg"].read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            namespace = {"svg": "http://www.w3.org/2000/svg"}
            lower_panel_lines = [
                span.text or ""
                for text in root.findall("svg:text", namespace)
                if text.attrib.get("y") == "1548"
                for span in text.findall("svg:tspan", namespace)
            ]

            self.assertTrue(lower_panel_lines)
            self.assertLessEqual(max(map(len, lower_panel_lines)), 65)
            self.assertIn('d="M500 551 L500 585"', svg)
            self.assertIn('d="M817 1395 L817 1440 L262 1440 L262 1485"', svg)
            self.assertIn('d="M817 1440 L738 1440 L738 1485"', svg)

    def test_editable_and_rendered_algorithms_retain_the_same_safety_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = build_algorithm(Path(directory))
            svg = outputs["svg"].read_text(encoding="utf-8")
            svg_root = ET.fromstring(svg)
            svg_text = " ".join(" ".join(svg_root.itertext()).split())
            excalidraw = json.loads(outputs["excalidraw"].read_text(encoding="utf-8"))
            excalidraw_text = " ".join(" ".join(
                str(element.get("text", ""))
                for element in excalidraw["elements"]
                if element.get("type") == "text"
            ).split())
            required_boundaries = (
                "Do not omit effective maintenance from MRD negativity alone.",
                "No national route does not prove absolute unavailability",
                "non-routine access must never be implied",
                "Use dedicated CAR-T and bispecific toxicity pathways.",
                "Clinical and pharmacy review pending",
            )
            for boundary in required_boundaries:
                self.assertIn(boundary, svg_text)
                self.assertIn(boundary, excalidraw_text)


if __name__ == "__main__":
    unittest.main()
