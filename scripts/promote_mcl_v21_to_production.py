#!/usr/bin/env python3
"""Publish the ratified MCL v2.1 production candidate to guidelines/mcl.

This is the only script in the v2.1 chain that writes to the public path. It does not
transform anything: it verifies that every artefact in the production candidate still
matches the SHA-256 recorded in release-manifest-v2.1.json, then copies. The bytes the
owner ratified are the bytes that go live.

It refuses to run unless --ratified-manifest is given the manifest SHA-256 that the
owner actually approved. That is the interlock: a rebuilt candidate produces a new
manifest hash and the promotion stops.

The superseded v2.0 files are not deleted. They are copied to guidelines/mcl/superseded/
so the previous release stays retrievable.

    python3 scripts/promote_mcl_v21_to_production.py --ratified-manifest <sha256>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "docs" / "mcl-v2.1" / "production-candidate"
OUTPUT = ROOT / "guidelines" / "mcl"
SUPERSEDED = OUTPUT / "superseded" / "v2.0"
MANIFEST = CANDIDATE / "release-manifest-v2.1.json"

V20_FILES = (
    "index.html",
    "guideline-v2.0.docx", "guideline-v2.0.pdf",
    "quickref-v2.0.docx", "quickref-v2.0.pdf",
    "algorithm-v2.0.svg", "algorithm-v2.0.excalidraw",
    "release-manifest-v2.0.json", "release-record-v2.0.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratified-manifest", required=True,
                        help="SHA-256 of release-manifest-v2.1.json as ratified by the accountable owner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Verify everything and report, but write nothing")
    args = parser.parse_args()

    if not MANIFEST.is_file():
        print(f"No production candidate at {CANDIDATE.relative_to(ROOT)}. "
              "Run scripts/build_mcl_v21_production.py first.", file=sys.stderr)
        return 1

    actual_manifest = sha256(MANIFEST)
    if actual_manifest != args.ratified_manifest:
        print("REFUSING TO PUBLISH: manifest hash does not match the ratified value.", file=sys.stderr)
        print(f"  ratified {args.ratified_manifest}", file=sys.stderr)
        print(f"  actual   {actual_manifest}", file=sys.stderr)
        print("  The candidate has been rebuilt since ratification. Re-ratify or rebuild.", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blocks = manifest.get("known_release_blocks") or []
    if blocks:
        print("REFUSING TO PUBLISH: the candidate records outstanding release blocks:", file=sys.stderr)
        for block in blocks:
            print(f"  {block}", file=sys.stderr)
        return 1

    drift = []
    for name, record in manifest["artefacts"].items():
        path = CANDIDATE / name
        if not path.is_file():
            drift.append(f"{name}: missing from the candidate directory")
            continue
        if sha256(path) != record["sha256"]:
            drift.append(f"{name}: bytes changed since the manifest was written")
    if drift:
        print("REFUSING TO PUBLISH: candidate artefacts do not match the manifest.", file=sys.stderr)
        for line in drift:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"Candidate verified against ratified manifest {actual_manifest}")
    print(f"{len(manifest['artefacts'])} artefacts, all matching.")
    if args.dry_run:
        print("\n--dry-run: nothing written. guidelines/mcl is untouched.")
        return 0

    SUPERSEDED.mkdir(parents=True, exist_ok=True)
    kept = []
    for name in V20_FILES:
        source = OUTPUT / name
        if source.is_file():
            shutil.copy2(source, SUPERSEDED / name)
            kept.append(name)
    print(f"\nPrevious release retained: {len(kept)} files in {SUPERSEDED.relative_to(ROOT)}")

    published = []
    for name in sorted(manifest["artefacts"]):
        if name.endswith(".html.tmp"):
            continue
        target = OUTPUT / name
        shutil.copyfile(CANDIDATE / name, target)
        published.append((name, sha256(target)))

    print("\nPublished to guidelines/mcl:")
    for name, digest in published:
        print(f"  {name:38s} {digest}")

    mismatched = [
        name for name, digest in published
        if digest != manifest["artefacts"][name]["sha256"]
    ]
    if mismatched:
        print(f"\nPOST-COPY HASH MISMATCH: {mismatched}", file=sys.stderr)
        return 1

    print("\nPublished bytes are identical to the ratified candidate.")
    print("Commit, push, and confirm the live URL serves these hashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
