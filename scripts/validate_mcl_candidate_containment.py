#!/usr/bin/env python3
"""Validate fail-closed deployment containment for an MCL production candidate."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "_worker.js"
ROUTES = ROOT / "_routes.json"

CANDIDATE_PATHS = {
    "/guidelines/mcl",
    "/guidelines/mcl/",
    "/guidelines/mcl/index.html",
    "/guidelines/mcl/guideline-v2.0.docx",
    "/guidelines/mcl/guideline-v2.0.pdf",
    "/guidelines/mcl/quickref-v2.0.docx",
    "/guidelines/mcl/quickref-v2.0.pdf",
    "/guidelines/mcl/algorithm-v2.0.svg",
    "/guidelines/mcl/algorithm-v2.0.excalidraw",
    "/guidelines/mcl/release-manifest-v2.0.json",
    "/guidelines/mcl/release-record-v2.0.json",
}


def validate_candidate_containment() -> None:
    worker = WORKER.read_text(encoding="utf-8")
    active_worker = re.sub(r"/\*.*?\*/", "", worker, flags=re.DOTALL)
    active_worker = "\n".join(
        line.split("//", 1)[0] for line in active_worker.splitlines()
        if not line.lstrip().startswith("//")
    )
    match = re.search(
        r"const\s+BLOCKED_FILES\s*=\s*new\s+Set\s*\(\s*\[(.*?)\]\s*\)",
        active_worker,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("Worker BLOCKED_FILES declaration is missing")
    blocked = set(re.findall(r'["\']([^"\']+)["\']', match.group(1)))
    if not CANDIDATE_PATHS <= blocked:
        raise AssertionError(f"Production candidate paths are not blocked: {sorted(CANDIDATE_PATHS - blocked)}")

    routes = json.loads(ROUTES.read_text(encoding="utf-8"))
    if set(routes) != {"version", "include", "exclude"} or routes["version"] != 1:
        raise AssertionError("Cloudflare routes schema is invalid")
    if routes["exclude"] != []:
        raise AssertionError("Cloudflare routes bypass the containment worker")
    included = set(routes["include"])
    if not CANDIDATE_PATHS <= included:
        raise AssertionError(f"Production candidate paths bypass the worker: {sorted(CANDIDATE_PATHS - included)}")
    print(f"MCL production-candidate containment: PASS blocked_routes={len(CANDIDATE_PATHS)}")


if __name__ == "__main__":
    validate_candidate_containment()
