#!/usr/bin/env python3
"""Validate publication surfaces and route exposure for the ratified MCL production release."""

from __future__ import annotations

import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

from scripts.validate_mcl_candidate_containment import CANDIDATE_PATHS

ROOT = Path(__file__).resolve().parents[1]


def validate_production_publication() -> None:
    worker = (ROOT / "_worker.js").read_text(encoding="utf-8")
    active_worker = re.sub(r"/\*.*?\*/", "", worker, flags=re.DOTALL)
    match = re.search(
        r"const\s+BLOCKED_FILES\s*=\s*new\s+Set\s*\(\s*\[(.*?)\]\s*\)",
        active_worker,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("Worker BLOCKED_FILES declaration is missing")
    blocked = set(re.findall(r'["\']([^"\']+)["\']', match.group(1)))
    exposed_blocks = CANDIDATE_PATHS & blocked
    if exposed_blocks:
        raise AssertionError(f"Ratified production paths remain worker-blocked: {sorted(exposed_blocks)}")

    routes = json.loads((ROOT / "_routes.json").read_text(encoding="utf-8"))
    if routes.get("exclude") != []:
        raise AssertionError("Cloudflare worker route exclusions changed")
    still_routed = CANDIDATE_PATHS & set(routes.get("include", []))
    if still_routed:
        raise AssertionError(f"Ratified production paths remain routed to blocking worker: {sorted(still_routed)}")

    for filename in ("guidelines.html", "tools.html"):
        document = BeautifulSoup((ROOT / filename).read_text(encoding="utf-8"), "html.parser")
        links = [link for link in document.select('a[href="/guidelines/mcl/"]')]
        if len(links) != 1:
            raise AssertionError(f"{filename} must expose exactly one MCL production card")
        if not links[0].select_one(".badge-live") or "Published" not in links[0].get_text(" ", strip=True):
            raise AssertionError(f"{filename} MCL card is not visibly published")
        visible = document.get_text(" ", strip=True).casefold()
        if "mantle cell lymphoma" not in visible or "withdrawn pending controlled update" in visible:
            raise AssertionError(f"{filename} retains an invalid MCL publication state")

    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    locations = [
        element.text for element in sitemap.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text
    ]
    production_url = "https://mohsinhaemacademy.com/guidelines/mcl/"
    if locations.count(production_url) != 1:
        raise AssertionError("Sitemap must expose the MCL production URL exactly once")

    record = json.loads((ROOT / "guidelines" / "mcl" / "release-record-v2.0.json").read_text(encoding="utf-8"))
    if record.get("release_state") != "PRODUCTION":
        raise AssertionError("Release record is not in PRODUCTION state")
    if record.get("owner_decisions", {}).get("production_hash_ratification") != "RATIFIED":
        raise AssertionError("Release record lacks exact-hash ratification")
    candidate = record.get("production_candidate", {})
    if candidate.get("commit") != "3f6f7103f27805ab3ac8abed7ba9c67bd5e91b1e":
        raise AssertionError("Release record candidate commit changed")
    if candidate.get("tree") != "a53f0be496dfcc3ccf2e406adc1629511a82be3c":
        raise AssertionError("Release record candidate tree changed")
    presentation = record.get("presentation_change", {})
    if presentation.get("commit") != "da70eeeda6a0cfbae5637c72a2f406c941f2031f":
        raise AssertionError("Presentation-change commit is not the ratified candidate")
    if presentation.get("tree") != "442fb44f3dd9b70c026732c9883e6a6c66c2c6aa":
        raise AssertionError("Presentation-change tree is not the ratified candidate")
    if presentation.get("owner_approval") != "RATIFIED":
        raise AssertionError("Presentation change lacks owner ratification")
    if presentation.get("deployment") != "AUTHORISED_PENDING_MERGE":
        raise AssertionError("Presentation change is not authorised for merge")
    print("MCL production publication gate: PASS hubs=2 sitemap=1 v2_routes=EXPOSED")


if __name__ == "__main__":
    validate_production_publication()
