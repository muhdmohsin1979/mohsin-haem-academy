#!/usr/bin/env python3
"""State-aware, fail-closed gate for the controlled MCL publication lifecycle."""

from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_mcl_containment import main as validate_containment
from scripts.validate_mcl_candidate_containment import validate_candidate_containment
from scripts.validate_mcl_production_publication import validate_production_publication
from scripts.validate_mcl_v2_preview import validate_current_preview
from scripts.validate_mcl_v2_release import MANIFEST as PRODUCTION_MANIFEST
from scripts.validate_mcl_v2_release import validate as validate_production_candidate

STATE = ROOT / "sources" / "mcl" / "release-state-v2.0.json"


def strict_json_load(path: Path) -> object:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def main() -> int:
    value = strict_json_load(STATE)
    if not isinstance(value, dict):
        raise ValueError("MCL release state must be a JSON object")
    state = value.get("state")
    if state == "PREVIEW":
        validate_containment()
        validate_current_preview()
    elif state == "PRODUCTION_CANDIDATE":
        required = {
            "publication_authority": True,
            "owner_scope_approval": True,
            "independent_clinical_review": "PASS",
            "pharmacy_verification": "COMPLETE",
            "production_hash_ratification": "PENDING",
            "pharmacy_verifier_identity": "RETAINED_PRIVATELY",
        }
        for key, expected in required.items():
            if value.get(key) != expected:
                raise ValueError(f"Invalid production-candidate control {key}: {value.get(key)!r}")
        expected_manifest_hash = value.get("production_manifest_sha256")
        actual_manifest_hash = hashlib.sha256(PRODUCTION_MANIFEST.read_bytes()).hexdigest()
        if expected_manifest_hash != actual_manifest_hash:
            raise ValueError("Production candidate manifest is not bound to the release state")
        validate_candidate_containment()
        validate_production_candidate()
    elif state == "PRODUCTION":
        required = {
            "publication_authority": True,
            "owner_scope_approval": True,
            "independent_clinical_review": "PASS",
            "pharmacy_verification": "COMPLETE",
            "production_hash_ratification": "RATIFIED",
            "pharmacy_verifier_identity": "RETAINED_PRIVATELY",
            "production_candidate_commit": "3f6f7103f27805ab3ac8abed7ba9c67bd5e91b1e",
            "production_candidate_tree": "a53f0be496dfcc3ccf2e406adc1629511a82be3c",
        }
        for key, expected in required.items():
            if value.get(key) != expected:
                raise ValueError(f"Invalid production control {key}: {value.get(key)!r}")
        expected_manifest_hash = value.get("production_manifest_sha256")
        actual_manifest_hash = hashlib.sha256(PRODUCTION_MANIFEST.read_bytes()).hexdigest()
        if expected_manifest_hash != actual_manifest_hash:
            raise ValueError("Ratified production manifest is not bound to the release state")
        validate_production_candidate()
        validate_production_publication()
    elif state == "PRODUCTION_CHANGE_CANDIDATE":
        required = {
            "publication_authority": True,
            "owner_scope_approval": True,
            "independent_clinical_review": "PASS",
            "pharmacy_verification": "COMPLETE",
            "production_hash_ratification": "RATIFIED",
            "change_candidate_owner_approval": "PENDING",
            "pharmacy_verifier_identity": "RETAINED_PRIVATELY",
            "live_production_merge_commit": "60e9e2b26f2d2d7f9cb3c1fbfee86d1fcc5dc124",
            "live_production_manifest_sha256": "70da66ac5d25644df7360ad6a7d64af6060bd105769e0105e5a28a9d00f62af1",
            "change_candidate_index_sha256": "0f92a28d1e1822bc4cc7dba19923e2e1ddd90a6de8b57e01a32847a67461c6cd",
        }
        for key, expected in required.items():
            if value.get(key) != expected:
                raise ValueError(f"Invalid production-change control {key}: {value.get(key)!r}")
        expected_manifest_hash = value.get("change_candidate_manifest_sha256")
        actual_manifest_hash = hashlib.sha256(PRODUCTION_MANIFEST.read_bytes()).hexdigest()
        if expected_manifest_hash != actual_manifest_hash:
            raise ValueError("Presentation-change candidate manifest is not bound to the release state")
        validate_production_candidate()
        validate_production_publication()
    else:
        raise ValueError(f"Unsupported or unauthorised MCL release state: {state!r}")

    print(f"MCL controlled publication state gate: PASS state={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
