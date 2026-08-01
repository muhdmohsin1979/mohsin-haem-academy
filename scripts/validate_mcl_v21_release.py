#!/usr/bin/env python3
"""Validate the exact MCL v2.1 production release in guidelines/mcl.

This is the v2.1 counterpart to validate_mcl_v2_release.py. It is deliberately
written against the standard library only — no fitz, bs4 or python-docx — so it
runs anywhere the repository is checked out, including environments where the
document toolchain is not installed. DOCX text is read from the OOXML zip and
PDF text from the Flate-compressed content streams.

It differs from the v2.0 validator in one design decision worth stating plainly.
The v2.0 release state binds commit and tree hashes, which creates a bootstrapping
sequence: commit, read the hash, write it back, commit again. v2.1 binds content
hashes instead — the reviewed candidate, the accessibility correction, the frozen
preview and the published manifest. Those pin the exact bytes, which is what the
gate is actually protecting, and they are knowable before the commit exists.

Fails closed on every check.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCL = ROOT / "guidelines" / "mcl"
SOURCE_DIR = ROOT / "sources" / "mcl" / "v2.1"
PREVIEW = ROOT / "docs" / "mcl-v2.1" / "web-preview"
MANIFEST = MCL / "release-manifest-v2.1.json"
RECORD = MCL / "release-record-v2.1.json"

EXPECTED_C4_SHA256 = "f16545565f7cb0c3619aa2ccff87f1fecd2ecc5718d4dae4d0960a09e9f77957"
EXPECTED_C5_SHA256 = "3b073bcaa8887018702cb2af53d4e655c59b82e7c7e2333548feb14d3bb4fba2"
EXPECTED_PREVIEW_SHA256 = "3dfa186d299c9489794be2728b02fac888efbcfe068b4755f11a2e19d50c0a27"

ARTEFACTS = (
    "index.html",
    "guideline-v2.1.docx",
    "guideline-v2.1.pdf",
    "quickref-v2.1.docx",
    "quickref-v2.1.pdf",
    "algorithm-first-line-v2.1.svg",
    "algorithm-first-line-v2.1.excalidraw",
    "algorithm-high-risk-v2.1.svg",
    "algorithm-high-risk-v2.1.excalidraw",
    "algorithm-relapsed-v2.1.svg",
    "algorithm-relapsed-v2.1.excalidraw",
    "algorithm-access-route-v2.1.svg",
    "algorithm-access-route-v2.1.excalidraw",
)

# Phrases that must not appear in a published artefact. Case-insensitive.
# "draft guidance" and "documentary verification pending" are legitimate — the
# first is a real NICE object, the second an accurate statement about the company
# early-access schemes — so a hit is ignored when either appears nearby.
FORBIDDEN = (
    "not for clinical use",
    "no publication authority",
    "controlled reviewed preview",
    "unratified",
    "working draft",
    "this draft",
    "before ratification",
    "preview-rc1",
)
ALLOWED_NEARBY = ("draft guidance", "documentary verification pending", "draft, not final")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", "ignore")
    return re.sub(r"<[^>]+>", " ", xml)


def pdf_text(path: Path) -> str:
    raw = path.read_bytes()
    chunks = []
    for match in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        try:
            chunks.append(zlib.decompress(match.group(1)).decode("latin-1"))
        except Exception:
            continue
    joined = " ".join(chunks)
    return " ".join(re.findall(r"\((?:\\.|[^\\()])*\)", joined))


def readable(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return docx_text(path)
    if suffix == ".pdf":
        return pdf_text(path)
    return path.read_text(encoding="utf-8", errors="replace")


def scan_forbidden(name: str, text: str) -> None:
    lowered = text.lower()
    for phrase in FORBIDDEN:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            window = lowered[max(0, index - 110): index + 110]
            if not any(allowed in window for allowed in ALLOWED_NEARBY):
                raise AssertionError(f"Stale pre-publication state in {name}: {phrase!r}")
            start = index + 1


def validate() -> None:
    require(MANIFEST.is_file(), "v2.1 release manifest is missing from guidelines/mcl")
    require(RECORD.is_file(), "v2.1 release record is missing from guidelines/mcl")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    record = json.loads(RECORD.read_text(encoding="utf-8"))

    require(manifest.get("document_code") == "MHA-MCL-2026-v2.1",
            "Manifest document code is not MHA-MCL-2026-v2.1")
    require(manifest.get("status") == "PUBLISHED",
            f"Manifest status is {manifest.get('status')!r}, not PUBLISHED")
    require(manifest.get("publication_authority") is True,
            "Manifest does not carry publication authority")
    require(manifest.get("clinical_change_from_reviewed_candidate") == "NONE",
            "Clinical-change boundary is not fail-closed")

    ratified = manifest.get("ratified_candidate_manifest_sha256")
    require(bool(ratified), "Manifest does not record the ratified candidate manifest hash")
    require(record.get("ratified_candidate_manifest_sha256") == ratified,
            "Release record and manifest disagree about the ratified hash")
    require(record.get("exact_production_hash_ratification") == "RATIFIED",
            "Release record does not record owner ratification")

    # Provenance: the reviewed bytes must not have moved.
    for path, expected, label in (
        (SOURCE_DIR / "reviewed-candidate-c4.html", EXPECTED_C4_SHA256, "reviewed candidate C4"),
        (SOURCE_DIR / "accessibility-corrected-c5.html", EXPECTED_C5_SHA256, "accessibility-corrected C5"),
        (PREVIEW / "index.html", EXPECTED_PREVIEW_SHA256, "reviewed web preview"),
    ):
        require(path.is_file(), f"Missing {label}: {path.relative_to(ROOT)}")
        require(sha256(path) == expected, f"{label} bytes changed since review")

    records = manifest.get("artefacts")
    require(isinstance(records, dict), "Manifest has no artefact table")
    require(set(records) == set(ARTEFACTS),
            f"Published artefact family is incomplete or unexpected: "
            f"missing {sorted(set(ARTEFACTS) - set(records))}, "
            f"extra {sorted(set(records) - set(ARTEFACTS))}")

    for name in ARTEFACTS:
        path = MCL / name
        require(path.is_file(), f"Published artefact missing: {name}")
        entry = records[name]
        require(entry.get("sha256") == sha256(path), f"Manifest mismatch: {name}")
        require(entry.get("bytes") == path.stat().st_size, f"Manifest size mismatch: {name}")
        if path.suffix.lower() in {".html", ".docx", ".pdf"}:
            scan_forbidden(name, readable(path))

    index = (MCL / "index.html").read_text(encoding="utf-8")
    require('<meta name="robots" content="index, follow">' in index,
            "Published guideline is not indexable")
    require("PUBLISHED 31 JULY 2026" in index,
            "Published guideline does not carry its publication banner")

    superseded = MCL / "superseded" / "v2.0" / "index.html"
    require(superseded.is_file(), "Superseded v2.0 page was not retained")
    require(sha256(superseded) == "0f92a28d1e1822bc4cc7dba19923e2e1ddd90a6de8b57e01a32847a67461c6cd",
            "Retained v2.0 page is not the bytes that were published as v2.0")

    print(f"MCL v2.1 production release: PASS "
          f"artefacts={len(ARTEFACTS)} ratified={ratified[:16]}...")


if __name__ == "__main__":
    try:
        validate()
    except AssertionError as error:
        print(f"MCL v2.1 production release: FAIL — {error}", file=sys.stderr)
        raise SystemExit(1)
