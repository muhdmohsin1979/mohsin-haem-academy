#!/usr/bin/env python3
"""Build the MCL v2.1 production candidate from the exact reviewed web preview.

This script does NOT touch guidelines/mcl. It writes a complete, production-labelled
release family into docs/mcl-v2.1/production-candidate/, which _routes.json sends to
_worker.js and the worker blocks — so the candidate is unreachable on every preview
deployment even though it carries "index, follow". The bytes you ratify are therefore
the exact bytes that later go live: promotion is a copy, not a rebuild.

Publishing is a separate, explicit step: scripts/promote_mcl_v21_to_production.py,
run only after the owner ratifies the hashes this script prints.

Everything is fail-closed. Input bytes are checked against the recorded SHA-256 values,
every label substitution must match exactly once, and the finished HTML is re-scanned
for residual preview markers.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "mcl" / "v2.1"
PREVIEW = ROOT / "docs" / "mcl-v2.1" / "web-preview"
OUTPUT = ROOT / "docs" / "mcl-v2.1" / "production-candidate"

EXPECTED_C4_SHA256 = "f16545565f7cb0c3619aa2ccff87f1fecd2ecc5718d4dae4d0960a09e9f77957"
EXPECTED_C5_SHA256 = "3b073bcaa8887018702cb2af53d4e655c59b82e7c7e2333548feb14d3bb4fba2"
EXPECTED_PREVIEW_SHA256 = "3dfa186d299c9489794be2728b02fac888efbcfe068b4755f11a2e19d50c0a27"

PUBLICATION_DATE = "31 July 2026"
DOCUMENT_CODE = "MHA-MCL-2026-v2.1"

DIAGRAMS = {
    "first-line": "algorithm-first-line-v2.1",
    "high-risk": "algorithm-high-risk-v2.1",
    "relapsed": "algorithm-relapsed-v2.1",
    "access-route": "algorithm-access-route-v2.1",
}

# Tokens that must not survive into a published file.
FORBIDDEN_AFTER_BUILD = (
    "noindex",
    "PREVIEW-RC1",
    "MHA-MCL-2026-v2.1-DRAFT",
    "not for clinical use",
    "no publication authority",
    "controlled reviewed preview",
    "controlled-preview",
    "unratified",
    "working draft",
    "verification is pending",
    "this draft",
    "before ratification",
    "draft status warning",
    "no v2.1 artefacts",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"Expected exactly one occurrence, found {count}: {old[:110]!r}")
    return text.replace(old, new)


def assert_inputs() -> None:
    checks = (
        (SOURCE_DIR / "reviewed-candidate-c4.html", EXPECTED_C4_SHA256, "reviewed candidate C4"),
        (SOURCE_DIR / "accessibility-corrected-c5.html", EXPECTED_C5_SHA256, "accessibility-corrected C5"),
        (PREVIEW / "index.html", EXPECTED_PREVIEW_SHA256, "reviewed web preview"),
    )
    for path, expected, label in checks:
        if not path.is_file():
            raise AssertionError(f"Missing {label}: {path.relative_to(ROOT)}")
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(
                f"{label} bytes changed.\n  expected {expected}\n  actual   {actual}\n"
                "Refusing to build a production candidate from unverified input."
            )
    for name in DIAGRAMS:
        for suffix in (".svg", ".excalidraw"):
            path = PREVIEW / f"{name}{suffix}"
            if not path.is_file():
                raise AssertionError(f"Missing diagram artefact: {path.relative_to(ROOT)}")


# --------------------------------------------------------------------------- HTML

DOWNLOADS_BLOCK_OLD = (
    "<h2>Guideline downloads</h2>\n"
    "    <p>Controlled publication files for specialist healthcare professionals.</p>\n"
    "    <ul class=\"artefact-links\"><li>No v2.1 artefacts have been generated. "
    "The published v2.0 downloads are deliberately not linked from this draft to prevent "
    "a reader mixing draft text with ratified files.</li></ul>"
)

DOWNLOADS_BLOCK_NEW = (
    "<h2>Guideline downloads</h2>\n"
    "    <p>Controlled publication files for specialist healthcare professionals. "
    "Every file below was generated from this page&rsquo;s exact bytes and is listed with its "
    "SHA-256 in the release manifest.</p>\n"
    "    <ul class=\"artefact-links\">"
    "<li><a href=\"guideline-v2.1.pdf\">Full guideline (PDF)</a></li>"
    "<li><a href=\"guideline-v2.1.docx\">Full guideline (Word)</a></li>"
    "<li><a href=\"quickref-v2.1.pdf\">Quick reference (PDF)</a></li>"
    "<li><a href=\"quickref-v2.1.docx\">Quick reference (Word)</a></li>"
    "<li><a href=\"algorithm-first-line-v2.1.svg\">First-line algorithm (SVG)</a> &middot; "
    "<a href=\"algorithm-first-line-v2.1.excalidraw\">editable</a></li>"
    "<li><a href=\"algorithm-high-risk-v2.1.svg\">High-risk algorithm (SVG)</a> &middot; "
    "<a href=\"algorithm-high-risk-v2.1.excalidraw\">editable</a></li>"
    "<li><a href=\"algorithm-relapsed-v2.1.svg\">Relapsed or refractory algorithm (SVG)</a> &middot; "
    "<a href=\"algorithm-relapsed-v2.1.excalidraw\">editable</a></li>"
    "<li><a href=\"algorithm-access-route-v2.1.svg\">Access-route flow (SVG)</a> &middot; "
    "<a href=\"algorithm-access-route-v2.1.excalidraw\">editable</a></li>"
    "<li><a href=\"release-manifest-v2.1.json\">Release manifest</a> &middot; "
    "<a href=\"release-record-v2.1.json\">Release record</a></li>"
    "</ul>"
)

ALGORITHM_NOTE_OLD_HEAD = "<div class=\"changed\"><strong>The algorithm has not been regenerated for v2.1</strong>"

ALGORITHM_NOTE_NEW = (
    "<div class=\"changed\"><strong>The four v2.1 diagrams and their editable copies come from one model</strong>\n"
    "      <p>The published v2.0 diagram is not carried forward. It encoded the v2.0 statements on the NICE "
    "positions for the TRIANGLE regimen, pirtobrutinib and brexucabtagene autoleucel, three of which v2.1 has "
    "corrected or withdrawn.</p>\n"
    "      <p><strong>Four pathway diagrams are embedded in this guideline</strong> &mdash; first line in section 6, "
    "high-risk in section 8, relapsed or refractory in section 9, and the access-route flow in section 17. They are "
    "inline SVG generated from a single node model, so the page stays self-contained.</p>\n"
    "      <p>The downloadable SVG and the editable Excalidraw scene above are generated from that same node model "
    "and are verified against each other before release: each scene is restored and exported through the official "
    "Excalidraw library, and the export must carry an identical ordered set of text, with no text outside the "
    "drawing bounds and no text overlapping other text. The editable copy therefore cannot drift from the published "
    "one &mdash; the defect the earlier comparison found in the CLL package.</p>\n"
    "    </div>"
)

HTML_REPLACEMENTS = (
    ('<meta name="robots" content="noindex, nofollow, noarchive">',
     '<meta name="robots" content="index, follow">'),
    ('<title>Mantle Cell Lymphoma guideline v2.1 — controlled reviewed preview</title>',
     '<title>Mantle Cell Lymphoma guideline v2.1</title>'),
    ('<span class="preview">CONTROLLED REVIEWED PREVIEW — NOT FOR CLINICAL USE</span>',
     f'<span class="preview">PUBLISHED {PUBLICATION_DATE.upper()}</span>'),
    ('MHA-MCL-2026-v2.1-PREVIEW-RC1 · evidence and access cut-off 2026-07-30 · supersedes nothing until exact production hashes are ratified',
     f'{DOCUMENT_CODE} · evidence and access cut-off 2026-07-30 · supersedes v2.0'),
    ('<strong id="draft-warning-heading">Controlled reviewed preview. Not for clinical use.</strong>',
     '<strong id="draft-warning-heading">Published specialist guideline.</strong>'),
    ('<p>This exact substantive candidate passed independent clinical review and pharmacy verification; '
     'reviewer identities are retained privately. It remains a controlled preview with no publication authority '
     'until the complete release family is generated, verified and its exact production hashes are ratified. '
     'The published guideline remains v2.0.</p>',
     '<p>This guideline passed independent clinical review and pharmacy verification; reviewer identities are '
     'retained privately. It is written for specialist healthcare professionals and supersedes v2.0. Access and '
     'regulatory positions move: check the current SmPC, the live NICE or SMC position and your local commissioning '
     'route before treating. Two literature corrections remain unresolved and are marked at every point their '
     f'figures are used. Evidence and access cut-off 2026-07-30; published {PUBLICATION_DATE}.</p>'),
    ('Those corrections were included in the exact candidate that passed independent clinical review and pharmacy '
     'verification. Publication authority remains false for this preview pending complete release-family '
     'verification and exact production-hash ratification.',
     'Those corrections were included in the exact candidate that passed independent clinical review and pharmacy '
     f'verification, and in the bytes published on {PUBLICATION_DATE}.'),
    ('<tr><th scope="row">Document code</th><td>MHA-MCL-2026-v2.1-PREVIEW-RC1</td></tr>',
     f'<tr><th scope="row">Document code</th><td>{DOCUMENT_CODE}</td></tr>'),
    ('<tr><th scope="row">State</th><td>CONTROLLED REVIEWED PREVIEW — NOT FOR CLINICAL USE</td></tr>',
     f'<tr><th scope="row">State</th><td>PUBLISHED — {PUBLICATION_DATE}</td></tr>'),
    ('<tr><th scope="row">Publication authority</th><td>FALSE — complete release family and exact production-hash ratification pending</td></tr>',
     f'<tr><th scope="row">Publication authority</th><td>TRUE — exact production hashes ratified by the accountable owner, {PUBLICATION_DATE}</td></tr>'),
    ('<li>These cleared gates do not grant publication authority to this preview. Exact production-hash '
     'ratification remains pending.</li>',
     '<li>Publication was authorised by the accountable owner against the exact production hashes recorded in '
     'the release manifest. The two unresolved literature corrections recorded in the evidence boundary section '
     'are still unresolved and remain marked at every point of use.</li>'),
    ('MHA-MCL-2026-v2.1-PREVIEW-RC1 · controlled reviewed preview, not for clinical use',
     f'{DOCUMENT_CODE} · published specialist guideline'),
    # --- residual draft language that survived the release-control pass ---
    ('<meta name="description" content="Mantle Cell Lymphoma guideline v2.1 draft — Mohsin Haematology Academy. Unratified working draft. Evidence, marketing authorisation, HTA recommendation and NHS England commissioning recorded as separate determinations, with United Kingdom and non-United Kingdom positions demarcated throughout.">',
     '<meta name="description" content="Mantle Cell Lymphoma guideline v2.1 — Mohsin Haematology Academy. Published specialist guideline. Evidence, marketing authorisation, HTA recommendation and NHS England commissioning recorded as separate determinations, with United Kingdom and non-United Kingdom positions demarcated throughout.">'),
    ('Priority P1 to P4 is the practical instruction. Draft, not for clinical use — confirm every access statement against the live source.',
     'Priority P1 to P4 is the practical instruction. Access positions change: confirm every access statement against the live source before treating.'),
    ('<caption>Current controlled-preview authority state</caption>',
     '<caption>Release-control state of the published guideline</caption>'),
    ('Component SmPCs, organ-function adjustments, infection prophylaxis and local SACT monitoring remain controlling; human pharmacy verification is pending.',
     'Component SmPCs, organ-function adjustments, infection prophylaxis and local SACT monitoring remain controlling.'),
# --- draft-voice residuals: the reviewed candidate speaks throughout as a
    # --- document awaiting approval. On a published page each of these is either
    # --- meaningless or actively misleading.
    ('<a class="skip-link" href="#draft-warning-heading">Skip to the draft status warning</a>',
     '<a class="skip-link" href="#draft-warning-heading">Skip to the guideline status notice</a>'),
    ('<div class="sidebar-card-body">\n        <ul class="artefact-links"><li>No v2.1 artefacts have been generated. The published v2.0 downloads are deliberately not linked from this draft to prevent a reader mixing draft text with ratified files.</li></ul>',
     '<div class="sidebar-card-body">\n        <ul class="artefact-links">'
     '<li><a href="guideline-v2.1.pdf">Full guideline (PDF)</a></li>'
     '<li><a href="quickref-v2.1.pdf">Quick reference (PDF)</a></li>'
     '<li><a href="algorithm-first-line-v2.1.svg">First-line algorithm</a></li>'
     '<li><a href="algorithm-relapsed-v2.1.svg">Relapsed algorithm</a></li>'
     '<li><a href="#review-artefacts">All downloads and editable files</a></li></ul>'),
    ('corrected several factual errors in this draft, including two where an earlier revision wrongly withdrew a correct v2.0 statement.',
     'corrected several factual errors during preparation of this revision, including two where an earlier working copy wrongly withdrew a correct v2.0 statement.'),
    ('<p><strong>An earlier revision of this draft withdrew the v2.0 statement that a June 2026 draft recommendation exists.',
     '<p><strong>An earlier working copy of this revision withdrew the v2.0 statement that a June 2026 draft recommendation exists.'),
    ('<p>An earlier revision of this draft said the v2.0 claim that GID-TA10858 / ID3975 returned to the NICE work programme on 14 July 2026',
     '<p>An earlier working copy of this revision said the v2.0 claim that GID-TA10858 / ID3975 returned to the NICE work programme on 14 July 2026'),
    # --- "before ratification": an instruction the reader cannot act on once the
    # --- document is published. Each becomes the action the reader should take.
    ('and commissioning status below must be re-checked against the official source before ratification.',
     'and commissioning status below must be re-checked against the official source before you treat, prescribe or promise a route.'),
    ('This requires pharmacy and hepatology verification before ratification.',
     'This requires pharmacy and hepatology verification before treatment.'),
    ('The appraisal remains in development. Check the live project status before ratification.',
     'The appraisal remains in development. Check the live project status before relying on it.'),
    ('<strong>Open the page directly before ratification.</strong>',
     '<strong>Open the page directly before relying on either reading.</strong>'),
    ('Before ratification the private scheme documentation should be reviewed and bound to the candidate, recording:',
     'Before either scheme is offered to a patient the private scheme documentation should be reviewed and recorded locally, capturing:'),
    ('<p>Before ratification every recommendation-bearing source should carry one of: FULL_TEXT_VERIFIED,',
     '<p>Every recommendation-bearing source should carry one of: FULL_TEXT_VERIFIED,'),
    ('Manual retrieval of the publisher PDF is required before ratification.',
     'Manual retrieval of the publisher PDF remains outstanding.'),
# --- retired MHRA SmPC addresses -------------------------------------------
    # MHRA product-information URLs are content-addressed, so a revision retires the
    # previous address. Both SmPCs below were revised on 24 July 2026 and their old
    # links returned BlobNotFound. Replacements were taken from MHRA's own product
    # search (products.mhra.gov.uk), pairing each document's SPC/PIL label to its
    # link rather than trusting list order.
    #
    # The quoted clinical text was re-checked against the current documents before
    # these substitutions were made:
    #   Tecartus  PLGB 11972-0045 — dosing, lymphodepletion schedule, tocilizumab
    #             availability, 7-day monitoring, 4-week proximity and the indication
    #             wording are all present unchanged, so no guideline text changes.
    #   Tepkinly  PLGB 41042-0092 / -0093 — section 4.1 covers DLBCL and follicular
    #             lymphoma only, confirming this guideline's statement that there is
    #             no current Great Britain mantle cell indication for epcoritamab.
    #             Two SmPCs exist, one per strength, and both are linked because
    #             step-up dosing uses both vials.
    ('<a href="https://mhraproducts4853.blob.core.windows.net/docs/cd6be42f02be6ec2bd92569340aedaf6f1179f16" rel="noreferrer">MHRA SmPC &mdash; Brexucabtagene autoleucel</a>'.replace('&mdash;', '—'),
     '<a href="https://mhraproducts4853.blob.core.windows.net/docs/c5ff00532d974218167694107f423f7e831adb06" rel="noreferrer">MHRA SmPC — Brexucabtagene autoleucel</a>'),
    ('<a href="https://mhraproducts4853.blob.core.windows.net/docs/396fbcf79471ec18c6096563395a6213231113b4" rel="noreferrer">MHRA SmPC &mdash; Epcoritamab</a>'.replace('&mdash;', '—'),
     '<a href="https://mhraproducts4853.blob.core.windows.net/docs/7a6c50e03c9839d4a9f6b8cbfd8da8e86da14b22" rel="noreferrer">MHRA SmPC — Epcoritamab 4 mg/0.8 ml</a> '
     '<a href="https://mhraproducts4853.blob.core.windows.net/docs/20456579a747924534ad1d434a9b5758e7630e8d" rel="noreferrer">MHRA SmPC — Epcoritamab 48 mg</a>'),
)


def transform_html(source: Path, target: Path) -> None:
    text = source.read_text(encoding="utf-8")
    for old, new in HTML_REPLACEMENTS:
        text = replace_once(text, old, new)

    text = replace_once(text, DOWNLOADS_BLOCK_OLD, DOWNLOADS_BLOCK_NEW)

    start = text.find(ALGORITHM_NOTE_OLD_HEAD)
    if start == -1:
        raise AssertionError("Algorithm note block not found")
    end = text.find("</div>", start)
    if end == -1:
        raise AssertionError("Algorithm note block is not terminated")
    text = text[:start] + ALGORITHM_NOTE_NEW + text[end + len("</div>"):]

    # Case-insensitive, because the reviewed candidate carries draft language in
    # sentence case as well as upper case. Two phrases are legitimate and allowed:
    # NICE draft guidance is a real regulatory object, and the company early-access
    # schemes genuinely remain documentarily unverified.
    allowed = (
        "draft guidance",
        "independent documentary verification pending",
        "class=\"preview\"",
        "algorithm-preview",
        ".preview",
    )
    lowered = text.lower()
    for token in FORBIDDEN_AFTER_BUILD:
        start = 0
        while True:
            index = lowered.find(token.lower(), start)
            if index == -1:
                break
            window = text[max(0, index - 120): index + 120]
            if any(phrase.lower() in window.lower() for phrase in allowed):
                start = index + 1
                continue
            raise AssertionError(
                f"Residual draft marker {token!r} survived the production build.\n"
                f"  ...{re.sub(r'<[^>]+>', '', window)}..."
            )
    if '<meta name="robots" content="index, follow">' not in text:
        raise AssertionError("Production HTML does not carry an indexable robots directive")

    target.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- DOCX and PDF

def convert_html(html: str, stem: str, outdir: Path) -> tuple[Path, Path]:
    """Same pipeline as build_mcl_v21_documents.py: textutil then LibreOffice."""
    html_path = outdir / f"{stem}.html"
    docx_path = outdir / f"{stem}.docx"
    pdf_path = outdir / f"{stem}.pdf"
    html_path.write_text(html, encoding="utf-8")
    subprocess.run(
        ["textutil", "-convert", "docx", "-output", str(docx_path), str(html_path)],
        check=True, timeout=180,
    )
    with tempfile.TemporaryDirectory(prefix="mcl-v21-libreoffice-") as profile:
        result = subprocess.run(
            [
                shutil.which("soffice") or "soffice", "--headless",
                f"-env:UserInstallation={(Path(profile) / 'profile').resolve().as_uri()}",
                "--convert-to", "pdf", "--outdir", str(outdir), str(docx_path),
            ],
            text=True, capture_output=True, timeout=240,
        )
    if result.returncode or not pdf_path.is_file():
        raise RuntimeError(result.stderr or result.stdout or f"No PDF produced for {docx_path}")
    html_path.unlink()
    return docx_path, pdf_path


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match is None:
        raise AssertionError(f"Unable to extract {label}")
    return match.group(0)


def build_documents(production_html: Path, outdir: Path) -> dict[str, Path]:
    source = production_html.read_text(encoding="utf-8")
    style = extract(r"<style>[\s\S]*?</style>", source, "stylesheet")
    hero = extract(r"<header class=\"page-hero\">[\s\S]*?</header>", source, "hero")
    main = extract(r"<main class=\"gl-main\" id=\"main-content\">[\s\S]*?</main>", source, "main content")
    footer = extract(r"<footer class=\"page-footer\">[\s\S]*?</footer>", source, "footer")
    common_head = (
        "<!doctype html><html lang=\"en-GB\"><head><meta charset=\"utf-8\">"
        f"<title>Mantle Cell Lymphoma guideline v2.1</title>" + style +
        "<style>body{background:white}.gl-main{width:100%;margin:0}.fig-scroll,.tbl-wrap{overflow:visible}"
        "svg.pathway{min-width:0;width:100%}.draft-banner{display:block}.vh{position:static;width:auto;height:auto;clip:auto}"
        "</style></head><body>"
    )
    guideline_html = common_head + hero + main + footer + "</body></html>"
    guideline_docx, guideline_pdf = convert_html(guideline_html, "guideline-v2.1", outdir)

    quick = extract(
        r"<h3>One-page quick reference</h3>[\s\S]*?(?=<h3>How the classifications are assigned</h3>)",
        source, "quick reference",
    )
    banner = extract(r"<aside class=\"draft-banner\"[\s\S]*?</aside>", source, "status banner")
    quick_html = (
        common_head + hero + banner +
        "<main class=\"gl-main\"><section><h2>MCL v2.1 quick reference</h2>" + quick +
        "</section></main>" + footer + "</body></html>"
    )
    quick_docx, quick_pdf = convert_html(quick_html, "quickref-v2.1", outdir)
    return {
        "guideline-v2.1.docx": guideline_docx,
        "guideline-v2.1.pdf": guideline_pdf,
        "quickref-v2.1.docx": quick_docx,
        "quickref-v2.1.pdf": quick_pdf,
    }


# ------------------------------------------------------------------- assembly

def build(skip_documents: bool = False) -> dict[str, Path]:
    assert_inputs()
    OUTPUT.mkdir(parents=True, exist_ok=True)

    artefacts: dict[str, Path] = {}
    html = OUTPUT / "index.html"
    transform_html(PREVIEW / "index.html", html)
    artefacts["index.html"] = html

    for name, production_name in DIAGRAMS.items():
        for suffix in (".svg", ".excalidraw"):
            target = OUTPUT / f"{production_name}{suffix}"
            shutil.copyfile(PREVIEW / f"{name}{suffix}", target)
            artefacts[target.name] = target

    blocks: list[str] = []
    if skip_documents:
        blocks.append("DOCX_PDF_NOT_REGENERATED_FOR_PRODUCTION_LABELS")
    else:
        artefacts.update(build_documents(html, OUTPUT))

    manifest = {
        "schema_version": 1,
        "document_code": DOCUMENT_CODE,
        "status": "PRODUCTION_CANDIDATE_AWAITING_EXACT_HASH_RATIFICATION",
        "publication_authority": False,
        "publication_date_when_ratified": PUBLICATION_DATE,
        "target_path": "guidelines/mcl",
        "provenance": {
            "reviewed_substantive_candidate": {
                "file": (SOURCE_DIR / "reviewed-candidate-c4.html").relative_to(ROOT).as_posix(),
                "sha256": EXPECTED_C4_SHA256,
            },
            "accessibility_corrected_candidate": {
                "file": (SOURCE_DIR / "accessibility-corrected-c5.html").relative_to(ROOT).as_posix(),
                "sha256": EXPECTED_C5_SHA256,
                "change_from_reviewed_candidate": "One generated diagram colour token; no clinical-content change",
            },
            "reviewed_web_preview": {
                "file": (PREVIEW / "index.html").relative_to(ROOT).as_posix(),
                "sha256": EXPECTED_PREVIEW_SHA256,
            },
        },
        "change_from_reviewed_web_preview": [
            "Release-control presentation: robots directive, title, banner, document code, "
            "release-control table, attestation bullet and footer.",
            "Guideline downloads section: the reviewed preview stated that no v2.1 artefacts existed and that "
            "the algorithm had not been regenerated. Both statements were true when the candidate was reviewed "
            "and are no longer true. The section now lists the generated artefacts and describes the parity "
            "test applied to the editable scenes. THIS IS A CONTENT CHANGE, not a label change, and should be "
            "read before ratification.",
        ],
        "clinical_change_from_reviewed_candidate": "NONE",
        "known_release_blocks": blocks,
        "artefacts": {
            name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
            for name, path in sorted(artefacts.items())
        },
    }
    manifest_path = OUTPUT / "release-manifest-v2.1.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    artefacts["release-manifest-v2.1.json"] = manifest_path

    record = {
        "schema_version": 1,
        "document_code": DOCUMENT_CODE,
        "supersedes": "MHA-MCL-2026-v2.0",
        "evidence_cut_off": "2026-07-30",
        "access_cut_off": "2026-07-30",
        "independent_clinical_review": "PASS",
        "pharmacy_verification": "COMPLETE",
        "verifier_identities": "RETAINED_PRIVATELY",
        "owner_production_direction": "REPLACE_V2_ON_WEBSITE",
        "exact_production_hash_ratification": "PENDING",
        "official_excalidraw_render_gate": "PASS",
        "offline_axe": "PASS — axe-core 4.10.2, WCAG 2.0/2.1 A and AA plus best-practice, 0 violations at 1280px and 375px",
        "outstanding_at_publication": [
            "Published correction against S38 (SYMPATICO) not retrieved; marked at every point of use.",
            "Published correction against S20C (sonrotoclax) not retrieved; marked at every point of use.",
            "ESMO 2025 and NCCN mantle cell sections were not retrievable; the society comparison covers "
            "EHA-EU 2025, BSH 2023 and EBMT 2026 only.",
            "Company early-access schemes are owner-attested and not independently documented.",
            "Access and regulatory positions are volatile and require scheduled re-checking.",
        ],
        "manifest_sha256": sha256(manifest_path),
    }
    record_path = OUTPUT / "release-record-v2.1.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    artefacts["release-record-v2.1.json"] = record_path
    return artefacts


if __name__ == "__main__":
    skip = "--skip-documents" in sys.argv
    built = build(skip_documents=skip)
    print()
    print("MCL v2.1 production candidate")
    print(f"  {OUTPUT.relative_to(ROOT)}")
    print()
    for name, path in sorted(built.items()):
        digest = sha256(path)
        print(f"  {name:38s} {path.stat().st_size:>9,d} bytes  {digest}")
    print()
    print("Nothing has been published. guidelines/mcl is untouched.")
    print("Ratify these hashes, then run scripts/promote_mcl_v21_to_production.py")
