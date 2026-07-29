from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.tone_guard import scan_file


class ToneGuardClinicalTerminologyTests(unittest.TestCase):
    def test_exact_clinical_systemic_phrases_are_not_treated_as_filler(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clinical.md"
            path.write_text(
                "Adults after at least two systemic lines.\n"
                "Follow-up should continue after first-line systemic treatment.\n"
                "The licence applies after two lines of systemic therapy.\n"
                "Avoid prophylactic systemic corticosteroids.\n"
                "There was no statistically significant OS difference.\n"
                "Grade 3 thrombocytopenia with significant bleeding.\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_file(path), [])

    def test_generic_systemic_word_remains_banned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prose.md"
            path.write_text("We need systemic change.\n", encoding="utf-8")
            hits = scan_file(path)
            self.assertEqual([word.casefold() for _, word, _ in hits], ["systemic"])


if __name__ == "__main__":
    unittest.main()
