#!/usr/bin/env python3
"""Generate a blocked, non-public MCL v2.0 working preview.

This first build slice deliberately cannot generate a published artefact. The live
withdrawal page remains authoritative until later clinical, pharmacy, preview and
owner gates are complete.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "sources" / "mcl" / "source-v2.0.html"
DEFAULT_STATUS = ROOT / "sources" / "mcl" / "status-matrix-v2.0.json"
DEFAULT_STATE = ROOT / "sources" / "mcl" / "release-state-v2.0.json"
DEFAULT_EVIDENCE = ROOT / "docs" / "mcl-v2" / "evidence-ledger.json"
DEFAULT_CLAIMS = ROOT / "docs" / "mcl-v2" / "claims-matrix.json"
DEFAULT_ACCESS_EVIDENCE = ROOT / "docs" / "mcl-v2" / "access-evidence-ledger.json"
DEFAULT_OUTPUT = ROOT / "docs" / "mcl-v2" / "preview" / "index.html"

STATE_KEYS = {
    "schema_version",
    "document_code",
    "version",
    "state",
    "evidence_cut_off",
    "access_cut_off",
    "publication_date",
    "publication_authority",
    "owner_scope_approval",
    "independent_clinical_review",
    "pharmacy_verification",
    "territorial_model",
    "algorithm_model",
    "audience",
    "quick_reference_target_pages",
}
STATUS_KEYS = {
    "id",
    "title",
    "population",
    "evidence_position",
    "marketing_authorisation",
    "nice_status",
    "england_access",
    "devolved_notes",
    "public_wording",
    "regimen",
    "dose_schedule_duration",
    "administration_monitoring_boundary",
    "pharmacy_evidence_status",
    "pharmacy_source_ids",
    "official_source_urls",
}
PROHIBITED_MARKERS = (
    "[VERIFY]",
    "AUTHORISED FOR PUBLICATION",
    "PUBLISHED EDUCATIONAL GUIDELINE",
)


def strict_json_load(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def require_exact_keys(value: dict[str, object], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} schema mismatch; missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}"
        )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ClinicalSourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.units: list[tuple[str, list[str]]] = []
        self.ids: list[str] = []
        self.prohibited_attributes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.casefold(): value or "" for key, value in attrs}
        if "id" in attr_map:
            self.ids.append(attr_map["id"])
        for key in attr_map:
            if key.startswith("on") or key in {"style", "srcdoc"}:
                self.prohibited_attributes.append(key)
        if tag.casefold() == "section" and "data-clinical-unit" in attr_map:
            unit_id = attr_map["data-clinical-unit"].strip()
            if "data-claim-ids" in attr_map:
                raise ValueError("Canonical source uses ambiguous data-claim-ids; split supporting and refuted claims")
            if "data-claims-supporting" not in attr_map or "data-claims-refuted" not in attr_map:
                raise ValueError(f"Clinical unit {unit_id} must declare supporting and refuted claim lists")
            supporting = attr_map["data-claims-supporting"].split()
            refuted = attr_map["data-claims-refuted"].split()
            if set(supporting) & set(refuted):
                raise ValueError(f"Clinical unit {unit_id} classifies the same claim as supporting and refuted")
            self.units.append((unit_id, supporting + refuted))
        if tag.casefold() in {"script", "iframe", "object", "embed"}:
            self.prohibited_attributes.append(tag.casefold())


def validate_state(state: object) -> dict[str, object]:
    if not isinstance(state, dict):
        raise ValueError("Release state must be a JSON object")
    require_exact_keys(state, STATE_KEYS, "release state")
    if state["schema_version"] != 1:
        raise ValueError("Unsupported release-state schema")
    if state["document_code"] != "MHA-MCL-2026-v2.0" or state["version"] != "2.0":
        raise ValueError("Release-state identity is inconsistent")
    if state["state"] != "PREVIEW":
        raise ValueError("This generator is fail-closed and supports PREVIEW only")
    if state["publication_authority"] is not False or state["publication_date"] is not None:
        raise ValueError("Working preview cannot carry publication authority or a publication date")
    if state["independent_clinical_review"] != "PENDING" or state["pharmacy_verification"] != "PENDING":
        raise ValueError("Initial working preview must preserve pending clinical and pharmacy gates")
    if state["territorial_model"] != "England access framework with separate devolved-nation notes":
        raise ValueError("Unapproved territorial model")
    return state


def validate_status_matrix(value: object, state: dict[str, object]) -> list[dict[str, object]]:
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "document_code",
        "access_cut_off",
        "jurisdiction_model",
        "status",
        "treatments",
    }:
        raise ValueError("Status matrix root schema mismatch")
    if value["schema_version"] != 1 or value["document_code"] != state["document_code"]:
        raise ValueError("Status matrix identity mismatch")
    if value["access_cut_off"] != state["access_cut_off"]:
        raise ValueError("Status matrix access cut-off mismatch")
    if value["jurisdiction_model"] != state["territorial_model"]:
        raise ValueError("Status matrix territorial model mismatch")
    if value["status"] != "WORKING_DRAFT":
        raise ValueError("Initial status matrix must remain a working draft")
    treatments = value["treatments"]
    if not isinstance(treatments, list) or len(treatments) < 10:
        raise ValueError("Status matrix must contain at least 10 treatment records")
    ids: list[str] = []
    for index, treatment in enumerate(treatments):
        if not isinstance(treatment, dict):
            raise ValueError(f"Treatment {index} must be an object")
        require_exact_keys(treatment, STATUS_KEYS, f"treatment {index}")
        treatment_id = treatment["id"]
        if not isinstance(treatment_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", treatment_id):
            raise ValueError(f"Treatment {index} has an invalid ID")
        ids.append(treatment_id)
        for key in STATUS_KEYS - {"official_source_urls", "pharmacy_source_ids"}:
            if not isinstance(treatment[key], str) or not treatment[key].strip():
                raise ValueError(f"Treatment {treatment_id} has an empty {key}")
        urls = treatment["official_source_urls"]
        if not isinstance(urls, list) or not urls or any(not isinstance(url, str) or not url.startswith("https://") for url in urls):
            raise ValueError(f"Treatment {treatment_id} requires official HTTPS source URLs")
        pharmacy_source_ids = treatment["pharmacy_source_ids"]
        if not isinstance(pharmacy_source_ids, list) or any(not isinstance(source_id, str) or not source_id for source_id in pharmacy_source_ids):
            raise ValueError(f"Treatment {treatment_id} has malformed pharmacy source IDs")
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate treatment IDs")
    return treatments


def validate_source(source: str, claim_ids: set[str]) -> list[tuple[str, list[str]]]:
    for marker in PROHIBITED_MARKERS:
        if marker.casefold() in source.casefold():
            raise ValueError(f"Canonical source contains prohibited marker: {marker}")
    parser = ClinicalSourceParser()
    parser.feed(source)
    parser.close()
    if parser.prohibited_attributes:
        raise ValueError(f"Canonical source contains prohibited active markup: {sorted(set(parser.prohibited_attributes))}")
    if len(parser.ids) != len(set(parser.ids)):
        raise ValueError("Canonical source contains duplicate HTML IDs")
    unit_ids = [unit_id for unit_id, _ in parser.units]
    if len(unit_ids) < 8 or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", unit_id) for unit_id in unit_ids):
        raise ValueError("Canonical source requires at least eight valid clinical-unit IDs")
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("Canonical source contains duplicate clinical-unit IDs")
    missing = sorted({claim for _, claims in parser.units for claim in claims} - claim_ids)
    if missing:
        raise ValueError(f"Canonical source references unknown claims: {missing}")
    return parser.units


def treatment_cards(treatments: list[dict[str, object]]) -> str:
    cards: list[str] = []
    for treatment in treatments:
        urls = treatment["official_source_urls"]
        if not isinstance(urls, list):
            raise ValueError(f"Treatment {treatment['id']} source URLs must be a list")
        links = " ".join(
            f'<a href="{html.escape(str(url), quote=True)}" rel="noreferrer">'
            f'{html.escape(official_source_label(str(url)))} — {html.escape(str(treatment["title"]))}</a>'
            for url in urls
        )
        cards.append(
            '<article class="status-card" id="status-' + html.escape(str(treatment["id"]), quote=True) + '">'
            '<h3>' + html.escape(str(treatment["title"])) + '</h3>'
            '<p><strong>Population:</strong> ' + html.escape(str(treatment["population"])) + '</p>'
            '<p><strong>Evidence:</strong> ' + html.escape(str(treatment["evidence_position"])) + '</p>'
            '<p><strong>Marketing authorisation:</strong> ' + html.escape(str(treatment["marketing_authorisation"])) + '</p>'
            '<p><strong>NICE:</strong> ' + html.escape(str(treatment["nice_status"])) + '</p>'
            '<p><strong>England access:</strong> ' + html.escape(str(treatment["england_access"])) + '</p>'
            '<p><strong>Devolved nations:</strong> ' + html.escape(str(treatment["devolved_notes"])) + '</p>'
            '<p><strong>Regimen:</strong> ' + html.escape(str(treatment["regimen"])) + '</p>'
            '<p><strong>Dose, schedule and duration:</strong> ' + html.escape(str(treatment["dose_schedule_duration"])) + '</p>'
            '<p><strong>Administration and monitoring boundary:</strong> ' + html.escape(str(treatment["administration_monitoring_boundary"])) + '</p>'
            '<p><strong>Pharmacy evidence status:</strong> ' + html.escape(str(treatment["pharmacy_evidence_status"])) + '</p>'
            '<p class="public-wording"><strong>Provisional public wording:</strong> ' + html.escape(str(treatment["public_wording"])) + '</p>'
            '<p class="sources">' + links + '</p>'
            '</article>'
        )
    return "\n".join(cards)


def official_source_label(url: str) -> str:
    lowered = url.casefold()
    if "mhraproducts" in lowered:
        return "MHRA SmPC"
    if "nice.org.uk" in lowered:
        return "NICE guidance or appraisal page"
    if "england.nhs.uk" in lowered:
        return "NHS England commissioning source"
    if "scottishmedicines.org.uk" in lowered:
        return "Scottish Medicines Consortium source"
    if "awttc.nhs.wales" in lowered:
        return "NHS Wales source"
    if "hscni.net" in lowered:
        return "HSC Northern Ireland source"
    return "Official source"


def plain_markdown(text: str) -> str:
    text = re.sub(r"\[([^]]+)]\(([^)]+)\)", r"\1 (\2)", text)
    return re.sub(r"\s+", " ", text.replace("**", "").replace("*", "").replace("`", "")).strip()


def evidence_reference_list(records: list[dict[str, object]]) -> str:
    items = []
    for record in records:
        source_id = str(record["id"])
        items.append(
            f'<li class="evidence-reference" id="reference-{html.escape(source_id, quote=True)}">'
            f'<strong>{html.escape(source_id)}:</strong> {html.escape(plain_markdown(str(record["bibliographic_identity_markdown"])))}'
            f'<br><strong>Design/population:</strong> {html.escape(str(record["design_population"]))}'
            f'<br><strong>Verified extraction:</strong> {html.escape(str(record["abstract_supported_result"]))}'
            f'<br><strong>Integrity:</strong> {html.escape(str(record["verification_integrity"]))}'
            '</li>'
        )
    return "\n".join(items)


def section_navigation(source: str) -> str:
    links = []
    for section_id, heading in re.findall(r'<section\s+id="([^"]+)"[^>]*>\s*<h2>(.*?)</h2>', source, flags=re.DOTALL | re.IGNORECASE):
        label = re.sub(r"<[^>]+>", "", heading)
        links.append(f'<li><a href="#{html.escape(section_id, quote=True)}">{html.escape(label.strip())}</a></li>')
    links.extend((
        '<li><a href="#access-status">Regulatory and access matrix</a></li>',
        '<li><a href="#evidence-references">Evidence references</a></li>',
        '<li><a href="#release-control">Release control</a></li>',
    ))
    return "\n".join(links)


def release_control_table(state: dict[str, object]) -> str:
    rows = (
        ("Document code", state["document_code"]),
        ("State", state["state"]),
        ("Evidence cut-off", state["evidence_cut_off"]),
        ("Access cut-off", state["access_cut_off"]),
        ("Owner scope approval", str(state["owner_scope_approval"]).upper()),
        ("Independent clinical review", state["independent_clinical_review"]),
        ("Pharmacy verification", state["pharmacy_verification"]),
        ("Publication authority", str(state["publication_authority"]).upper()),
    )
    return "\n".join(
        f'<tr><th scope="row">{html.escape(str(label))}</th><td>{html.escape(str(value))}</td></tr>'
        for label, value in rows
    )


def apply_cll_navigation_pattern(document: str, aria_label: str) -> str:
    style = '''
    html { scroll-behavior:smooth; }
    .anchor-nav { position:sticky; top:0; z-index:100; margin:1rem 0; padding:.55rem .7rem; box-shadow:0 4px 14px rgba(23,32,51,.12); }
    .anchor-nav h2 { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
    .anchor-nav ul { display:flex; gap:.25rem; columns:auto; margin:0; padding:0; overflow-x:auto; list-style:none; scrollbar-width:thin; }
    .anchor-nav li { flex:0 0 auto; }
    .anchor-nav a { display:block; padding:.42rem .65rem; border-radius:6px; white-space:nowrap; font:700 .78rem/1.3 Arial,sans-serif; text-decoration:none; }
    .anchor-nav a:hover { color:white; background:var(--navy); }
    .mcl-layout { display:grid; grid-template-columns:minmax(0,1fr) 280px; gap:2rem; align-items:start; }
    .mcl-content { min-width:0; }
    .mcl-content > section { scroll-margin-top:4.8rem; }
    .mcl-sidebar { position:sticky; top:4.35rem; align-self:start; max-height:calc(100vh - 5.35rem); overflow-y:auto; padding-right:.25rem; scrollbar-width:thin; }
    .mcl-sidebar::-webkit-scrollbar { width:6px; }
    .mcl-sidebar::-webkit-scrollbar-thumb { background:var(--line); border-radius:3px; }
    .sidebar-nav { padding:.85rem; }
    .sidebar-nav h2 { margin:.1rem 0 .65rem; padding-bottom:.45rem; font:700 .84rem/1.3 Arial,sans-serif; text-transform:uppercase; letter-spacing:.06em; }
    .sidebar-nav ul { columns:auto; margin:0; padding:0; list-style:none; }
    .sidebar-nav a { display:block; padding:.38rem .45rem; border-radius:5px; font:400 .79rem/1.35 Arial,sans-serif; text-decoration:none; }
    .sidebar-nav a:hover { color:white; background:var(--navy); }
    @media (max-width:900px) {
      .mcl-layout { grid-template-columns:1fr; }
      .mcl-sidebar { display:none; }
    }
'''
    document = document.replace("  </style>", style + "  </style>", 1)
    opening = f'  <nav aria-label="{aria_label}">'
    start = document.find(opening)
    if start < 0:
        raise ValueError(f"MCL section navigation is missing: {aria_label}")
    end = document.find("  </nav>", start)
    if end < 0:
        raise ValueError("MCL section navigation is not closed")
    end += len("  </nav>")
    navigation = document[start:end]
    anchor_navigation = navigation.replace(opening, f'  <nav class="anchor-nav" aria-label="{aria_label}">', 1)
    sidebar_navigation = navigation.replace(opening, f'    <nav class="sidebar-nav" aria-label="{aria_label} sidebar">', 1)
    layout_open = anchor_navigation + '\n  <div class="mcl-layout">\n    <div class="mcl-content">'
    document = document[:start] + layout_open + document[end:]
    closing = f'''    </div>
    <aside class="mcl-sidebar" aria-label="Independently scrolling section navigation">
{sidebar_navigation}
    </aside>
  </div>
</main>'''
    if document.count("</main>") != 1:
        raise ValueError("MCL document must contain exactly one main element")
    return document.replace("</main>", closing, 1)


def render_preview(
    source: str,
    treatments: list[dict[str, object]],
    state: dict[str, object],
    evidence_records: list[dict[str, object]],
    evidence_boundary: str,
) -> str:
    rendered = f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>MCL v2.0 controlled working preview</title>
  <style>
    :root {{ --navy:#1B2A4A; --red:#C41E3A; --paper:#F7F8FA; --ink:#172033; --line:#D7DCE2; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:var(--paper); font:17px/1.58 Georgia,serif; }}
    header {{ padding:2.3rem max(1rem,calc((100% - 1120px)/2)); color:white; background:linear-gradient(115deg,var(--navy),#29406d); }}
    header h1 {{ margin:.25rem 0; font-size:clamp(1.9rem,10vw,3.4rem); line-height:1.08; }}
    .preview {{ display:inline-block; padding:.45rem .7rem; background:var(--red); font:700 .82rem Arial,sans-serif; letter-spacing:.04em; }}
    main {{ width:min(1120px,calc(100% - 2rem)); margin:1.5rem auto 4rem; }}
    .warning {{ border:3px solid var(--red); background:#fff1f3; padding:1rem 1.2rem; margin-bottom:1.5rem; }}
    section {{ background:white; border:1px solid var(--line); border-radius:10px; padding:1.1rem 1.3rem; margin:1rem 0; }}
    h2,h3 {{ color:var(--navy); }}
    h2 {{ border-bottom:3px solid var(--red); padding-bottom:.35rem; }}
    .status-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(310px,100%),1fr)); gap:1rem; }}
    .status-card {{ background:white; border:1px solid var(--line); border-top:5px solid var(--navy); border-radius:9px; padding:1rem; overflow-wrap:anywhere; }}
    .status-card h3 {{ margin-top:0; }}
    .public-wording {{ border-left:4px solid var(--red); padding-left:.7rem; }}
    nav {{ background:white; border:1px solid var(--line); border-radius:10px; padding:1rem 1.3rem; }}
    nav ul {{ columns:2; padding-left:1.3rem; }}
    .artefact-links {{ display:flex; flex-wrap:wrap; gap:.65rem 1rem; padding-left:1.2rem; }}
    .artefact-links li {{ padding-right:1rem; }}
    .sources a {{ overflow-wrap:anywhere; }}
    .evidence-reference {{ margin-bottom:1rem; }}
    table {{ width:100%; border-collapse:collapse; }}
    th,td {{ border:1px solid var(--line); padding:.55rem; text-align:left; vertical-align:top; }}
    th {{ background:#eef2f7; }}
    .page-footer {{ padding:1.2rem max(1rem,calc((100% - 1120px)/2)); color:white; background:var(--navy); }}
    .algorithm-preview {{ display:block; width:100%; aspect-ratio:1000/2050; margin-top:1rem; border:1px solid var(--line); background:var(--paper); }}
    .mobile-algorithm-link {{ display:none; margin-top:1rem; padding:.8rem; border:2px solid var(--navy); text-align:center; font-weight:700; }}
    a {{ color:#173f7a; }}
    :focus-visible {{ outline:3px solid #F6C344; outline-offset:3px; }}
    .skip-link {{ position:absolute; left:1rem; top:-5rem; z-index:10; padding:.7rem 1rem; color:white; background:var(--navy); }}
    .skip-link:focus {{ top:1rem; }}
    @media (max-width:600px) {{
      body {{ font-size:16px; }}
      header {{ padding:1.35rem 1rem; }}
      .preview {{ max-width:100%; white-space:normal; }}
      main {{ width:calc(100% - 1rem); margin-top:.75rem; }}
      section,.warning {{ padding:.9rem; }}
      h2 {{ font-size:1.35rem; line-height:1.2; }}
      .algorithm-preview {{ display:none; }}
      .mobile-algorithm-link {{ display:block; }}
      .algorithm-caption {{ display:none; }}
      nav ul {{ columns:1; }}
    }}
    @media print {{ .preview {{ color:black; border:2px solid black; background:white; }} body {{ background:white; }} }}
  </style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<header>
  <span class="preview">CONTROLLED WORKING PREVIEW — NOT FOR CLINICAL USE</span>
  <h1>Mantle Cell Lymphoma v2.0</h1>
  <p>{html.escape(str(state['document_code']))} · evidence and access cut-off {html.escape(str(state['evidence_cut_off']))}</p>
</header>
<main id="main-content">
  <aside class="warning" role="note" aria-labelledby="preview-warning-heading">
    <strong id="preview-warning-heading">Non-public working build.</strong>
    Clinical and pharmacy review are pending. This preview has no publication authority and must not be used for treatment, prescribing, consent, referral or commissioning decisions.
  </aside>
  <p><strong>Publication model:</strong> England access framework with separate devolved-nation notes. Clinical evidence and access status are deliberately presented as separate determinations.</p>
  <nav aria-label="MCL preview sections">
    <h2>Contents</h2>
    <ul>
      {section_navigation(source)}
    </ul>
  </nav>
  <section id="review-artefacts">
    <h2>Working review artefacts</h2>
    <p>All files below are non-public working previews. They have no publication authority and remain subject to clinical, pharmacy and publication review.</p>
    <ul class="artefact-links">
      <li><a href="guideline-working.pdf" download>Full guideline (PDF)</a></li>
      <li><a href="guideline-working.docx" download>Editable guideline (DOCX)</a></li>
      <li><a href="quickref-working.pdf" download>Three-page quick reference (PDF)</a></li>
      <li><a href="quickref-working.docx" download>Editable quick reference (DOCX)</a></li>
      <li><a href="algorithm-working.svg" download>Algorithm (SVG)</a></li>
      <li><a href="algorithm-working.excalidraw" download>Editable algorithm source (Excalidraw)</a></li>
    </ul>
    <figure>
      <a class="mobile-algorithm-link" href="algorithm-working.svg">Open the full-size algorithm</a>
      <object class="algorithm-preview" data="algorithm-working.svg" type="image/svg+xml" aria-labelledby="algorithm-caption">
        <a href="algorithm-working.svg">Open the MCL v2.0 working treatment algorithm</a>
      </object>
      <figcaption class="algorithm-caption" id="algorithm-caption">Evidence-first treatment pathway with explicit access labels. Working preview only.</figcaption>
    </figure>
  </section>
  {source}
  <section id="access-status">
    <h2>13. Working regulatory and access matrix</h2>
    <p>These entries are time-sensitive working text for specialist review. Recheck official sources before preview freeze and before any publication decision.</p>
    <div class="status-grid">
      {treatment_cards(treatments)}
    </div>
  </section>
  <section id="evidence-boundary">
    <h2>14. Evidence boundary</h2>
    <p><strong>Scientific extraction is abstract-only except where the controlled evidence ledger states otherwise.</strong></p>
    <p>{html.escape(evidence_boundary)}</p>
  </section>
  <section id="evidence-references">
    <h2>15. Evidence references</h2>
    <p>Bibliographic identity and integrity status are retained with each record. A verified citation identity does not support claims absent from the checked evidence text.</p>
    <ol>
      {evidence_reference_list(evidence_records)}
    </ol>
  </section>
  <section id="release-control">
    <h2>16. Release control</h2>
    <table>
      <caption>Current controlled-preview authority state</caption>
      <tbody>
        {release_control_table(state)}
      </tbody>
    </table>
  </section>
</main>
<footer class="page-footer">
  <strong>Mohsin Haematology Academy</strong> · Accountable owner: Dr Muhammad Mohsin, Consultant Haematologist · {html.escape(str(state['document_code']))} · controlled working preview
</footer>
</body>
</html>
'''
    return apply_cll_navigation_pattern(rendered, "MCL preview sections")


def build_preview(
    *,
    source_path: Path = DEFAULT_SOURCE,
    status_path: Path = DEFAULT_STATUS,
    state_path: Path = DEFAULT_STATE,
    evidence_path: Path = DEFAULT_EVIDENCE,
    claims_path: Path = DEFAULT_CLAIMS,
    access_evidence_path: Path = DEFAULT_ACCESS_EVIDENCE,
    output_path: Path = DEFAULT_OUTPUT,
) -> dict[str, object]:
    state = validate_state(strict_json_load(state_path))
    evidence = strict_json_load(evidence_path)
    claims = strict_json_load(claims_path)
    if not isinstance(evidence, dict) or not isinstance(claims, dict):
        raise ValueError("Evidence and claims ledgers must be JSON objects")
    evidence_rows = evidence.get("records", [])
    evidence_ids = {row["id"] for row in evidence_rows if isinstance(row, dict) and isinstance(row.get("id"), str)}
    if not isinstance(evidence_rows, list) or len(evidence_rows) != evidence.get("record_count") or any(not isinstance(row, dict) for row in evidence_rows):
        raise ValueError("Evidence ledger record count or structure is inconsistent")
    evidence_records = [row for row in evidence_rows if isinstance(row, dict)]
    evidence_boundary = evidence.get("evidence_boundary")
    if not isinstance(evidence_boundary, str) or not evidence_boundary.strip():
        raise ValueError("Evidence ledger requires a non-empty evidence boundary")
    claim_rows = claims.get("claims", [])
    claim_ids = {row["id"] for row in claim_rows if isinstance(row, dict) and isinstance(row.get("id"), str)}
    if evidence.get("record_count") != len(evidence_ids) or claims.get("claim_count") != len(claim_ids):
        raise ValueError("Evidence or claim counts are inconsistent")
    referenced = {source_id for row in claim_rows for source_id in row.get("source_ids", []) if isinstance(row, dict)}
    if not referenced <= evidence_ids:
        raise ValueError("Claims reference missing evidence records")

    treatments = validate_status_matrix(strict_json_load(status_path), state)
    source = source_path.read_text(encoding="utf-8")
    units = validate_source(source, claim_ids)
    rendered = render_preview(source, treatments, state, evidence_records, evidence_boundary)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")

    metadata: dict[str, object] = {
        "document_code": state["document_code"],
        "state": state["state"],
        "publication_authority": state["publication_authority"],
        "clinical_unit_count": len(units),
        "treatment_count": len(treatments),
        "source_sha256": sha256(source_path),
        "status_matrix_sha256": sha256(status_path),
        "release_state_sha256": sha256(state_path),
        "evidence_ledger_sha256": sha256(evidence_path),
        "claims_matrix_sha256": sha256(claims_path),
        "access_evidence_ledger_sha256": sha256(access_evidence_path),
        "preview_sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
    }
    metadata_path = output_path.parent / "preview-metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    metadata = build_preview(output_path=args.output)
    print(
        "MCL v2.0 working preview generated: "
        f"units={metadata['clinical_unit_count']} treatments={metadata['treatment_count']} "
        f"sha256={metadata['preview_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
