#!/usr/bin/env python3
"""State-aware, fail-closed gate for the controlled MCL publication lifecycle."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_mcl_containment import main as validate_containment
from scripts.validate_mcl_v2_preview import validate_current_preview

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
    if state != "PREVIEW":
        raise ValueError(f"Unsupported or unauthorised MCL release state: {state!r}")

    validate_containment()
    validate_current_preview()
    print("MCL controlled publication state gate: PASS state=PREVIEW")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
