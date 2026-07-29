from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_mcl_v2_preview import strict_json_load


class MCLV2ValidatorTests(unittest.TestCase):
    def test_every_evidence_record_is_claim_bound_or_explicitly_disposed(self) -> None:
        base = ROOT / "docs" / "mcl-v2"
        evidence = json.loads((base / "evidence-ledger.json").read_text(encoding="utf-8"))["records"]
        claims = json.loads((base / "claims-matrix.json").read_text(encoding="utf-8"))["claims"]
        referenced = {source_id for claim in claims for source_id in claim["source_ids"]}
        orphaned = [record["id"] for record in evidence if record["id"] not in referenced and not record.get("relationship_disposition")]
        self.assertEqual(orphaned, [])

    def test_source_register_hashes_match_every_registered_file(self) -> None:
        base = ROOT / "docs" / "mcl-v2"
        register = json.loads((base / "source-register.json").read_text(encoding="utf-8"))
        for source in register["sources"]:
            path = base / source["path"]
            self.assertEqual(source["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), source["id"])

    def test_claim_source_arrays_match_their_explicit_source_expressions(self) -> None:
        claims = json.loads((ROOT / "docs" / "mcl-v2" / "claims-matrix.json").read_text(encoding="utf-8"))["claims"]
        by_id = {claim["id"]: claim for claim in claims}
        self.assertEqual(
            by_id["C21"]["source_ids"],
            ["S14", "S15", "S16", "S17", "S18", "S19", "S20"],
        )
        self.assertEqual(
            by_id["C22"]["source_ids"],
            ["S06", "S16", "S18", "S19", "S21", "S22", "S23"],
        )

    def test_registered_audit_and_claim_matrix_state_the_same_atomic_claims(self) -> None:
        base = ROOT / "docs" / "mcl-v2"
        claims = json.loads((base / "claims-matrix.json").read_text(encoding="utf-8"))["claims"]
        audit = (base / "audits" / "2026-07-28-clinical-evidence-audit.md").read_text(encoding="utf-8")
        by_id = {claim["id"]: claim for claim in claims}
        for claim_id in ("C14", "C24"):
            self.assertIn(f"| {claim_id} | {by_id[claim_id]['atomic_statement']} |", audit)

    def test_manifest_and_preview_metadata_bind_the_access_ledger(self) -> None:
        preview = ROOT / "docs" / "mcl-v2" / "preview"
        access = ROOT / "docs" / "mcl-v2" / "access-evidence-ledger.json"
        digest = hashlib.sha256(access.read_bytes()).hexdigest()
        manifest = json.loads((preview / "build-manifest-working.json").read_text(encoding="utf-8"))
        metadata = json.loads((preview / "preview-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["controlled_inputs"]["docs/mcl-v2/access-evidence-ledger.json"],
            {"bytes": access.stat().st_size, "sha256": digest},
        )
        self.assertEqual(metadata["access_evidence_ledger_sha256"], digest)

    def test_duplicate_authority_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text('{"publication_authority": false, "publication_authority": true}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
                strict_json_load(path)


if __name__ == "__main__":
    unittest.main()
