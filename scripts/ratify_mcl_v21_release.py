#!/usr/bin/env python3
"""Stamp owner ratification into the published MCL v2.1 release record.

The manifest and release record that ship beside a published guideline were written
before ratification, so they still describe the release as a candidate awaiting
approval. A reader who fetches the manifest — which is the reason for publishing one —
is told the guideline is not authorised. This script corrects that, and only that.

It does not touch index.html, the documents, the diagrams or any hash of them. It
rewrites two JSON files in guidelines/mcl:

  release-manifest-v2.1.json  status and publication authority
  release-record-v2.1.json    ratification state, publication date, authority

The SHA-256 the owner actually ratified is recorded permanently in both files as
ratified_candidate_manifest_sha256. That value is what makes the ratification
auditable: it names the exact bytes that were approved, and it does not change when
this script rewrites the manifest around it.

Every published artefact is verified against the manifest before the rewrite and the
run aborts if anything has drifted.

    python3 scripts/ratify_mcl_v21_release.py \\
        --ratified-manifest 8e6d1c19... --publication-date 2026-07-31
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "guidelines" / "mcl"
MANIFEST = OUTPUT / "release-manifest-v2.1.json"
RECORD = OUTPUT / "release-record-v2.1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratified-manifest", required=True,
                        help="SHA-256 of the candidate manifest the owner ratified")
    parser.add_argument("--publication-date", required=True,
                        help="ISO date the guideline was published, e.g. 2026-07-31")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for path in (MANIFEST, RECORD):
        if not path.is_file():
            print(f"Missing {path.relative_to(ROOT)}. Publish the release first.", file=sys.stderr)
            return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    already = manifest.get("ratified_candidate_manifest_sha256")
    if already:
        if already != args.ratified_manifest:
            print("REFUSING: this release is already stamped with a different ratified hash.", file=sys.stderr)
            print(f"  stamped  {already}", file=sys.stderr)
            print(f"  supplied {args.ratified_manifest}", file=sys.stderr)
            return 1
        print("Already stamped with this ratified hash; nothing to do.")
        return 0

    current = sha256(MANIFEST)
    if current != args.ratified_manifest:
        print("REFUSING: the published manifest is not the ratified one.", file=sys.stderr)
        print(f"  ratified {args.ratified_manifest}", file=sys.stderr)
        print(f"  found    {current}", file=sys.stderr)
        return 1

    drift = []
    for name, record in manifest["artefacts"].items():
        path = OUTPUT / name
        if not path.is_file():
            drift.append(f"{name}: not published")
        elif sha256(path) != record["sha256"]:
            drift.append(f"{name}: published bytes differ from the manifest")
    if drift:
        print("REFUSING: published artefacts do not match the manifest.", file=sys.stderr)
        for line in drift:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"Verified {len(manifest['artefacts'])} published artefacts against the ratified manifest.")
    if args.dry_run:
        print("--dry-run: nothing written.")
        return 0

    manifest["status"] = "PUBLISHED"
    manifest["publication_authority"] = True
    manifest["published"] = args.publication_date
    manifest["ratified_candidate_manifest_sha256"] = args.ratified_manifest
    manifest["ratification"] = (
        "The accountable owner ratified the exact artefact hashes recorded below, identified by the "
        f"candidate manifest SHA-256 {args.ratified_manifest}. This file was then rewritten to record "
        "publication; the artefact hashes are unchanged by that rewrite."
    )
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    record = json.loads(RECORD.read_text(encoding="utf-8"))
    record["exact_production_hash_ratification"] = "RATIFIED"
    record["ratified_candidate_manifest_sha256"] = args.ratified_manifest
    record["publication_authority"] = True
    record["published"] = args.publication_date
    record["supersedes_retained_at"] = "guidelines/mcl/superseded/v2.0/"
    record.pop("manifest_sha256", None)
    record["review_due"] = (
        "The access and regulatory layer is volatile: NICE, SMC and commissioning positions in this "
        "guideline were checked on 2026-07-30 and require scheduled re-checking."
    )
    RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    post = []
    for name, rec in manifest["artefacts"].items():
        if sha256(OUTPUT / name) != rec["sha256"]:
            post.append(name)
    if post:
        print(f"POST-WRITE MISMATCH in {post}", file=sys.stderr)
        return 1

    print()
    print(f"  release-manifest-v2.1.json  {sha256(MANIFEST)}")
    print(f"  release-record-v2.1.json    {sha256(RECORD)}")
    print()
    print("Guideline, documents and diagrams are untouched and still match their ratified hashes.")
    print("Commit and push, then the branch is ready to merge.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
