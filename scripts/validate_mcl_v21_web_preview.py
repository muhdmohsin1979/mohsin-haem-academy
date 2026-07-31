#!/usr/bin/env python3
"""Validate the exact MCL v2.1 reviewed web preview and its fail-closed manifest."""

from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "mcl" / "v2.1"
PREVIEW = ROOT / "docs" / "mcl-v2.1" / "web-preview"
MANIFEST = PREVIEW / "manifest-reviewed-web-preview.json"
EXPECTED_C4_SHA256 = "f16545565f7cb0c3619aa2ccff87f1fecd2ecc5718d4dae4d0960a09e9f77957"
EXPECTED_C5_SHA256 = "3b073bcaa8887018702cb2af53d4e655c59b82e7c7e2333548feb14d3bb4fba2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.fragments: list[str] = []
        self.robots: list[str] = []
        self.h1 = 0
        self.tables = 0
        self.captions = 0
        self.regions = 0
        self.named_regions = 0
        self.navs = 0
        self.evidence_records = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(str(attributes["id"]))
        href = attributes.get("href")
        if tag == "a" and href and href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag == "meta" and attributes.get("name") == "robots":
            self.robots.append(str(attributes.get("content", "")))
        if tag == "h1":
            self.h1 += 1
        if tag == "table":
            self.tables += 1
        if tag == "caption":
            self.captions += 1
        if tag == "nav":
            self.navs += 1
        classes = set(str(attributes.get("class", "")).split())
        if {"tbl-wrap", "fig-scroll"} & classes and attributes.get("tabindex") == "0" and attributes.get("role") == "region":
            self.regions += 1
            if attributes.get("aria-label") or attributes.get("aria-labelledby"):
                self.named_regions += 1
        if "evidence-reference" in classes:
            self.evidence_records += 1


def canonical_xml(text: str) -> str:
    return ET.canonicalize(text.strip())


def validate() -> None:
    source = SOURCE_DIR / "reviewed-candidate-c4.html"
    if sha256(source) != EXPECTED_C4_SHA256:
        raise AssertionError("Reviewed C4 source hash changed")
    corrected = SOURCE_DIR / "accessibility-corrected-c5.html"
    if sha256(corrected) != EXPECTED_C5_SHA256:
        raise AssertionError("Accessibility-corrected C5 source hash changed")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "REVIEWED_WEB_PREVIEW_INCOMPLETE_RELEASE_FAMILY":
        raise AssertionError("Reviewed web preview status changed")
    if manifest["publication_authority"] is not False:
        raise AssertionError("Incomplete web preview claims publication authority")
    if manifest["reviewed_substantive_candidate"]["sha256"] != EXPECTED_C4_SHA256:
        raise AssertionError("Manifest is not bound to exact C4")
    if manifest["accessibility_corrected_candidate"]["sha256"] != EXPECTED_C5_SHA256:
        raise AssertionError("Manifest is not bound to exact C5")
    required_blocks = {
        "OFFICIAL_EXCALIDRAW_RENDER_NOT_VERIFIED",
        "EXACT_PRODUCTION_HASH_RATIFICATION_PENDING",
    }
    if set(manifest["known_release_blocks"]) != required_blocks:
        raise AssertionError("Known release blocks are incomplete or unexpected")
    assurance = manifest.get("accessibility_assurance", {})
    axe_report = PREVIEW / "axe-report.json"
    if (
        assurance.get("status") != "PASS"
        or assurance.get("axe_version") != "4.10.2"
        or assurance.get("viewports") != ["1280", "375"]
        or assurance.get("report_sha256") != sha256(axe_report)
    ):
        raise AssertionError("Offline Axe assurance is absent or not bound to its exact report")

    for name, record in manifest["artefacts"].items():
        path = PREVIEW / name
        if not path.is_file() or path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise AssertionError(f"Preview manifest mismatch: {name}")

    html = (PREVIEW / "index.html").read_text(encoding="utf-8")
    parser = AuditParser()
    parser.feed(html)
    duplicates = [key for key, count in Counter(parser.ids).items() if count > 1]
    broken = sorted(set(parser.fragments) - set(parser.ids))
    if duplicates or broken:
        raise AssertionError(f"DOM identifiers invalid duplicates={duplicates} broken={broken}")
    if parser.robots != ["noindex, nofollow, noarchive"]:
        raise AssertionError(f"Unexpected preview robots directive: {parser.robots}")
    if (parser.h1, parser.tables, parser.captions, parser.regions, parser.named_regions, parser.navs, parser.evidence_records) != (1, 17, 17, 20, 20, 2, 53):
        raise AssertionError("Reviewed preview structural counts changed")

    required = (
        "CONTROLLED REVIEWED PREVIEW — NOT FOR CLINICAL USE",
        "Independent clinical review</th><td>PASS — reviewer identity retained privately",
        "Pharmacy verification</th><td>COMPLETE — verifier identity retained privately",
        "Publication authority</th><td>FALSE — complete release family and exact production-hash ratification pending",
        EXPECTED_C4_SHA256,
        EXPECTED_C5_SHA256,
        "PHARMACY_VERIFIED — exact MHRA SmPC quotations validated",
        "Attestation record",
        "published guideline remains v2.0",
    )
    for phrase in required:
        if phrase not in html:
            raise AssertionError(f"Required reviewed-preview wording missing: {phrase}")
    forbidden = (
        "AUTHORISED FOR PUBLICATION",
        "PUBLISHED v2.1",
        "publication authority</th><td>TRUE",
        "Independent clinical review</th><td>PENDING",
        "Pharmacy verification</th><td>PENDING",
        "REPORT_ONLY_NOT_PHARMACY_VERIFIED",
        "REPORT_ONLY_TRIAL_AND_GUIDELINE_SCHEDULE_NOT_PHARMACY_VERIFIED",
        "REPORT_ONLY_TRIAL_SCHEDULE_NOT_PHARMACY_VERIFIED",
    )
    for phrase in forbidden:
        if phrase in html:
            raise AssertionError(f"Forbidden preview wording present: {phrase}")

    inline = re.findall(r'(<svg class="pathway"[\s\S]*?</svg>)', html)
    if len(inline) != 4:
        raise AssertionError(f"Expected four inline diagrams, found {len(inline)}")
    inline_by_title: dict[str, str] = {}
    for text in inline:
        root = ET.fromstring(text)
        title = root.find("{http://www.w3.org/2000/svg}title")
        if title is None or not title.text:
            raise AssertionError("Inline diagram title missing")
        inline_by_title[title.text] = canonical_xml(text)
    standalone_by_title: dict[str, str] = {}
    for path in (PREVIEW / "first-line.svg", PREVIEW / "high-risk.svg", PREVIEW / "relapsed.svg", PREVIEW / "access-route.svg"):
        text = path.read_text(encoding="utf-8")
        root = ET.fromstring(text)
        title = root.find("{http://www.w3.org/2000/svg}title")
        if title is None or not title.text:
            raise AssertionError(f"Standalone diagram title missing: {path.name}")
        standalone_by_title[title.text] = canonical_xml(text)
    if inline_by_title != standalone_by_title:
        raise AssertionError("Inline and standalone v2.1 SVGs differ")

    for name in ("first-line", "high-risk", "relapsed", "access-route"):
        svg_root = ET.fromstring((PREVIEW / f"{name}.svg").read_text(encoding="utf-8"))
        svg_texts = ["".join(element.itertext()) for element in svg_root.findall("{http://www.w3.org/2000/svg}text")]
        scene = json.loads((PREVIEW / f"{name}.excalidraw").read_text(encoding="utf-8"))
        editable_texts = [str(element["text"]) for element in scene.get("elements", []) if element.get("type") == "text"]
        if editable_texts != svg_texts:
            raise AssertionError(f"Editable text drift in {name}.excalidraw")
        if len(scene.get("elements", [])) < len(svg_texts):
            raise AssertionError(f"Editable scene is structurally incomplete: {name}.excalidraw")

    print(
        "MCL v2.1 reviewed web preview: PASS "
        "c4=exact c5=exact artefacts=5 tables=17 regions=20 evidence_records=53 publication_authority=false"
    )


if __name__ == "__main__":
    validate()
