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
    else:
        raise ValueError(f"Unsupported or unauthorised MCL release state: {state!r}")

    print(f"MCL controlled publication state gate: PASS state={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
