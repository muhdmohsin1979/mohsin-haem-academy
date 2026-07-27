#!/usr/bin/env python3
"""Validate the published CLL v2.0 artefact family."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CLL = ROOT / "guidelines" / "cll"
RELEASE_MANIFEST = CLL / "release-manifest.json"
ARTEFACTS = [
    CLL / "index.html",
    CLL / "guideline.docx",
    CLL / "guideline.pdf",
    CLL / "quickref.docx",
    CLL / "quickref.pdf",
    CLL / "algorithm.svg",
    CLL / "algorithm.excalidraw",
]


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    return " ".join((node.text or "") for node in root.iter() if node.tag.endswith("}t"))


def pdf_text(path: Path) -> tuple[str, int]:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required to validate PDF text") from exc
    document = fitz.open(path)
    pages = [page.get_text() for page in document]
    if any(len(text.strip()) < 80 for text in pages):
        raise AssertionError(f"Blank or near-blank PDF page detected: {path}")
    return "\n".join(pages), len(pages)


def readable_text(path: Path) -> tuple[str, int | None]:
    if path.suffix == ".docx":
        return docx_text(path), None
    if path.suffix == ".pdf":
        return pdf_text(path)
    if path.suffix == ".svg":
        root = ET.parse(path).getroot()
        return " ".join(root.itertext()), None
    if path.suffix == ".excalidraw":
        data = json.loads(path.read_text(encoding="utf-8"))
        return " ".join(str(element.get("text", "")) for element in data.get("elements", [])), None
    return path.read_text(encoding="utf-8"), None


def normalise(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def assert_pdf_card_integrity(path: Path) -> None:
    import fitz

    pages = [normalise(page.get_text()) for page in fitz.open(path)]
    cards = {
        "Ibrutinib TA429 (de-prioritised — see note)": "Dose: 420 mg once daily continuously",
        "Venetoclax monotherapy (post-BTKi R/R) TA796": "TA796 recommends venetoclax monotherapy",
        "Pirtobrutinib (non-covalent BTKi) TA1173": "routine-budget implementation was due by 29 September 2026",
        "BTK Inhibitor Resistance — Key Molecular Mechanisms": "BTK C481S mutation",
    }
    for title, body in cards.items():
        title_pages = {idx for idx, text in enumerate(pages) if title in text}
        body_pages = {idx for idx, text in enumerate(pages) if body in text}
        if len(title_pages) != 1 or title_pages != body_pages:
            raise AssertionError(
                f"PDF card is split, duplicated or detached: {title!r}; "
                f"title pages={sorted(title_pages)}, body pages={sorted(body_pages)}"
            )


def assert_algorithm_structure(scene_path: Path) -> None:
    scene = json.loads(scene_path.read_text(encoding="utf-8"))
    elements = [element for element in scene.get("elements", []) if not element.get("isDeleted")]
    texts = [element for element in elements if element.get("type") == "text"]
    rectangles = {element.get("id"): element for element in elements if element.get("type") == "rectangle"}
    expected_states = {
        "BTKi NAIVE",
        "COVALENT-BTKi INTOLERANCE",
        "COVALENT-BTKi PROGRESSION",
        "RELAPSE OFF FIXED-DURATION",
        "DOUBLE EXPOSED",
        "DOUBLE REFRACTORY",
    }
    present = {normalise(str(element.get("text", ""))) for element in texts}
    missing = sorted(expected_states.difference(present))
    if missing:
        raise AssertionError(f"Excalidraw is missing independent R/R state titles: {missing}")

    for arrow in (element for element in elements if element.get("type") == "arrow"):
        points = arrow.get("points") or []
        absolute = [
            (float(arrow["x"]) if axis == 0 else float(arrow["y"])) + float(point[axis])
            for point in points
            for axis in (0, 1)
        ]
        ys = absolute[1::2]
        if ys and min(ys) > 645:
            raise AssertionError("Excalidraw contains an arrow between R/R classification states")

    for text in texts:
        container_id = text.get("containerId")
        if not container_id:
            continue
        container = rectangles.get(container_id)
        if container is None:
            raise AssertionError(f"Bound text {text.get('id')} has no rectangle container")
        left = float(text["x"])
        top = float(text["y"])
        right = left + float(text["width"])
        bottom = top + float(text["height"])
        c_left = float(container["x"])
        c_top = float(container["y"])
        c_right = c_left + float(container["width"])
        c_bottom = c_top + float(container["height"])
        if left < c_left or top < c_top or right > c_right or bottom > c_bottom:
            raise AssertionError(f"Bound Excalidraw text exceeds its container: {text.get('id')}")

    stale = "nearly tertiary/trial referral"
    if stale in " ".join(str(element.get("text", "")) for element in texts).casefold():
        raise AssertionError("Excalidraw contains stale tertiary-referral wording")


def assert_reproducible() -> None:
    with tempfile.TemporaryDirectory(prefix="cll-v2-repro-") as tmp:
        target = Path(tmp)
        (target / "scripts").mkdir()
        (target / "guidelines" / "cll").mkdir(parents=True)
        for name in ["generate_cll_v2_algorithm.py", "generate_cll_v2_documents.py"]:
            shutil.copy2(ROOT / "scripts" / name, target / "scripts" / name)
        shutil.copy2(CLL / "index.html", target / "guidelines" / "cll" / "index.html")
        for name in ["generate_cll_v2_algorithm.py", "generate_cll_v2_documents.py"]:
            subprocess.run([sys.executable, str(target / "scripts" / name)], check=True, capture_output=True, text=True)

        for name in ["algorithm.svg", "algorithm.excalidraw"]:
            generated = target / "guidelines" / "cll" / name
            if generated.read_bytes() != (CLL / name).read_bytes():
                raise AssertionError(f"Generator did not reproduce {name} byte-for-byte")

        for name in ["guideline.docx", "quickref.docx"]:
            generated_text = normalise(docx_text(target / "guidelines" / "cll" / name))
            committed_text = normalise(docx_text(CLL / name))
            if generated_text != committed_text:
                raise AssertionError(f"Generator did not reproduce {name} semantically")

        soffice = shutil.which("soffice")
        if not soffice:
            raise AssertionError("LibreOffice soffice is required for PDF reproducibility validation")
        pdf_out = target / "pdf"
        pdf_out.mkdir()
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf_out),
             str(target / "guidelines" / "cll" / "guideline.docx"),
             str(target / "guidelines" / "cll" / "quickref.docx")],
            check=True,
            capture_output=True,
            text=True,
        )
        for name in ["guideline.pdf", "quickref.pdf"]:
            generated_text, generated_pages = pdf_text(pdf_out / name)
            committed_text, committed_pages = pdf_text(CLL / name)
            if generated_pages != committed_pages or normalise(generated_text) != normalise(committed_text):
                raise AssertionError(f"Generator did not reproduce {name} text and pagination")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--manifest", type=Path, default=RELEASE_MANIFEST)
    args = parser.parse_args()

    missing = [str(path) for path in ARTEFACTS if not path.exists()]
    if missing:
        raise AssertionError(f"Missing artefacts: {missing}")

    results: dict[str, dict[str, object]] = {}
    texts: dict[str, str] = {}
    for path in ARTEFACTS:
        text, pages = readable_text(path)
        texts[path.name] = text
        record: dict[str, object] = {
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        if pages is not None:
            record["pages"] = pages
        results[path.name] = record

    required_all = ["TA1173", "Pirtobrutinib", "26 July 2026"]
    for name, text in texts.items():
        for phrase in required_all:
            if phrase.casefold() not in text.casefold():
                raise AssertionError(f"{name}: missing required phrase {phrase!r}")

    clinical_surfaces = ["index.html", "guideline.docx", "guideline.pdf", "quickref.docx", "quickref.pdf", "algorithm.svg", "algorithm.excalidraw"]
    for name in clinical_surfaces:
        folded = re.sub(r"\s+", " ", texts[name].casefold())
        for phrase in ["double exposed", "double refractory"]:
            if phrase not in folded:
                raise AssertionError(f"{name}: missing controlled phrase {phrase!r}")

    for name in ["index.html", "guideline.pdf", "quickref.pdf", "algorithm.svg", "algorithm.excalidraw"]:
        if "published" not in re.sub(r"\s+", " ", texts[name].casefold()):
            raise AssertionError(f"{name}: missing publication-status phrase 'published'")

    stale_pharmacy_status = "pharmacy verification and exact-artefact approval pending"
    for name, text in texts.items():
        if stale_pharmacy_status in normalise(text).casefold():
            raise AssertionError(f"{name}: stale pharmacy-pending release banner detected")

    prohibited_release_statuses = [
        "protected preview",
        "not yet published",
        "exact-artefact approval pending",
        "not authorised for publication",
    ]
    for name, text in texts.items():
        folded = normalise(text).casefold()
        for phrase in prohibited_release_statuses:
            if phrase in folded:
                raise AssertionError(f"{name}: prohibited pre-publication status remains: {phrase!r}")

    combined = "\n".join(texts.values())
    html = texts["index.html"]
    if html.casefold().count("</html>") != 1:
        raise AssertionError("HTML must contain exactly one closing </html> tag")
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)
    duplicate_ids = sorted({value for value in ids if ids.count(value) > 1})
    if duplicate_ids:
        raise AssertionError(f"HTML contains duplicate IDs: {duplicate_ids}")
    required_sections = {"scope", "overview", "methodology", "diagnosis", "prognostics", "indications", "firstline", "rr", "response", "special", "audit", "limits", "refs", "cite"}
    missing_sections = sorted(required_sections.difference(ids))
    if missing_sections:
        raise AssertionError(f"HTML is missing required sections: {missing_sections}")
    if "[VERIFY]" in combined:
        raise AssertionError("Unresolved [VERIFY] marker detected")
    exact_ta1173 = "only if retreatment with a covalent BTK inhibitor, including retreatment after a fixed-duration regimen, is not clinically appropriate"
    if exact_ta1173.casefold() not in html.casefold():
        raise AssertionError("HTML: exact TA1173 restriction is absent")
    if 'name="robots" content="index, follow"' not in html.casefold():
        raise AssertionError("Published HTML must carry an explicit index/follow directive")

    full_surfaces = ["index.html", "guideline.docx", "guideline.pdf"]
    for name in full_surfaces:
        folded = re.sub(r"\s+", " ", texts[name].casefold())
        for phrase in [
            "obinutuzumab cycle 1 day 1, 100 mg",
            "total treatment duration is 15 cycles",
            "bru in phase i/ii".replace(" ", ""),
        ]:
            candidate = folded.replace(" ", "") if phrase == "bruinphasei/ii" else folded
            if phrase not in candidate:
                raise AssertionError(f"{name}: missing full treatment-card content {phrase!r}")

    exact_references = [
        "Pirtobrutinib after a Covalent BTK Inhibitor in Chronic Lymphocytic Leukemia.",
        "Fixed-duration pirtobrutinib plus venetoclax-rituximab versus venetoclax-rituximab for patients with previously treated chronic lymphocytic leukaemia or small lymphocytic lymphoma (BRUIN CLL-322): an open-label, multicentre, randomised, controlled, phase 3 trial.",
    ]
    for name in full_surfaces:
        folded = normalise(texts[name]).casefold()
        for title in exact_references:
            if normalise(title).casefold() not in folded:
                raise AssertionError(f"{name}: exact PubMed title is absent: {title}")

    access_surfaces = ["index.html", "guideline.docx", "guideline.pdf", "quickref.docx", "quickref.pdf", "algorithm.svg", "algorithm.excalidraw"]
    for name in access_surfaces:
        folded = re.sub(r"\s+", " ", texts[name].casefold())
        for phrase in ["interim blueteq funding", "29 september 2026"]:
            if phrase not in folded:
                raise AssertionError(f"{name}: missing time-bounded TA1173 access wording {phrase!r}")
        for phrase in [
            "del(17p)/tp53",
            "chemoimmunotherapy",
            "b-cell receptor pathway inhibitor",
        ]:
            if phrase not in folded:
                raise AssertionError(f"{name}: missing explicit TA796 criterion {phrase!r}")

    for name in ["guideline.docx", "quickref.docx"]:
        path = CLL / name
        with zipfile.ZipFile(path) as archive:
            core = archive.read("docProps/core.xml").decode("utf-8")
        if "2026-07-26" not in core:
            raise AssertionError(f"{name}: controlled 2026 creation/modification metadata absent")

    stale_patterns = [
        r"pirtobrutinib[^<\n]{0,160}not NICE-commissioned",
        r"pirtobrutinib[^<\n]{0,160}check (?:current )?NICE",
        r"TA931[^<\n]{0,100}untreated CLL\. NICE, 2024",
        r"always re-test TP53/IGHV at relapse",
    ]
    for pattern in stale_patterns:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            raise AssertionError(f"Stale wording detected: {pattern}")

    if "PUBLISHED" not in texts["algorithm.svg"]:
        raise AssertionError("Algorithm SVG is not visibly marked as published")
    if "pharmacist" in combined.casefold() or "pharmacist name" in combined.casefold():
        raise AssertionError("Potential pharmacist identity surface detected")

    assert_pdf_card_integrity(CLL / "guideline.pdf")
    assert_algorithm_structure(CLL / "algorithm.excalidraw")
    assert_reproducible()

    manifest = {
        "document_code": "MHA-CLL-2026-v2.0",
        "status": "AUTHORISED FOR PUBLICATION 27 JULY 2026",
        "artefacts": results,
    }
    if args.write_manifest:
        args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    elif not args.manifest.exists():
        raise AssertionError(f"Approval-bound release manifest is missing: {args.manifest}")
    else:
        expected = json.loads(args.manifest.read_text(encoding="utf-8"))
        if expected != manifest:
            raise AssertionError("Current artefacts do not match the approval-bound release manifest")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        raise
