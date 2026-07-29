#!/usr/bin/env python3
"""Generate editable and rendered MCL v2.0 preview algorithms."""

from __future__ import annotations

import hashlib
import html
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "mcl-v2" / "preview"

W, H = 1000, 2050
NAVY = "#1B2A4A"
RED = "#C41E3A"
TEXT = "#1F2937"
MUTED = "#5B6472"
BLUE = "#EAF0F7"
GREEN = "#EAF4ED"
PINK = "#FBECEF"
AMBER = "#FFF7E6"
WHITE = "#FFFFFF"
BACKGROUND = "#F8FAFC"

CANONICAL_HEADER = {
    "header.title": "MANTLE CELL LYMPHOMA",
    "header.code": "MCL v2.0 treatment decision algorithm · MHA-MCL-2026-v2.0",
    "header.preview": "WORKING PREVIEW\nNOT FOR CLINICAL USE",
    "group.first-line": "FIRST-LINE ORIENTATION · EVIDENCE DOES NOT CREATE ACCESS",
    "group.relapsed": "RELAPSED / REFRACTORY · CLASSIFY PRIOR BTKi EXPOSURE AND REASON FOR STOPPING",
    "footer.cut-off": "Evidence/access cut-off 28 July 2026 · England access framework with separate devolved-nation notes.",
    "footer.warning": "CONTROLLED WORKING PREVIEW — do not use for treatment, prescribing, consent, referral or commissioning.",
}

CANONICAL_NODES = {
    "diagnosis": {
        "title": "1 · CONFIRM DIAGNOSIS AND DEFINE RISK",
        "body": "Integrated morphology, immunophenotype and cyclin D1 / CCND-family confirmation.\nRecord blastoid or pleomorphic morphology, Ki-67 and TP53 status where feasible.\nDefine symptoms, tempo, organ compromise, cytopenias, fitness, frailty and goals.",
    },
    "treat": {
        "title": "2 · IS TREATMENT REQUIRED NOW?",
        "body": "No: selected asymptomatic low-volume, indolent or non-nodal disease may be observed after MDT review.\nYes: document objective indication, patient priorities and the clinical and access pathway below.",
    },
    "branch": {
        "title": "3 · FIRST-LINE OR RELAPSED / REFRACTORY?",
        "body": "First line: separate treatment fitness, biological risk and access.\nRelapse: record prior classes, response, duration and reason for stopping; distinguish intolerance from progression.",
    },
    "fit": {
        "title": "YOUNGER / TREATMENT-FIT",
        "body": "TRIANGLE changes the evidence architecture for the studied 18–65-year protocol.\nAdding ASCT did not improve FFS.\nLicensed ibrutinib regimen; current negative NICE advice is draft.\nNo final national entitlement.",
    },
    "older": {
        "title": "OLDER / TRANSPLANT-INELIGIBLE",
        "body": "Integrate frailty, renal, infection, cardiac, bleeding and interaction risk.\nENRICH and ECHO inform evidence.\nVR-CAP has TA370 only in its exact transplant-unsuitable scope.\nConfirm every other access route.",
    },
    "highrisk": {
        "title": "TP53-MUTATED / HIGH RISK",
        "body": "Early specialist and trial discussion.\nNovel combinations show activity but do not prove comparative superiority or elimination of risk.\nDo not omit effective maintenance from MRD negativity alone.",
    },
    "oneline": {
        "title": "EXACTLY ONE PREVIOUS LINE",
        "body": "England only, when exact live criteria are met:\n• ibrutinib TA502\n• zanubrutinib TA1081\nThe broader licences do not replace the NICE one-line scope.",
    },
    "intolerance": {
        "title": "COVALENT-BTKi INTOLERANCE",
        "body": "Stopped for toxicity without progression.\nSelect another clinically appropriate route by retained sensitivity, comorbidity, toxicity and access.\nDo not call intolerance resistance.",
    },
    "progression": {
        "title": "COVALENT-BTKi PROGRESSION",
        "body": "Refer early for cellular-therapy and trial assessment.\nPirtobrutinib has post-BTKi activity and a GB licence but no demonstrated national England MCL route at cut-off.\nDo not transpose CLL funding.",
    },
    "ta677": {
        "title": "TA677 CDF MANAGED ACCESS",
        "body": "Brexucabtagene autoleucel after at least two systemic lines including a BTKi.\nEngland route remains Cancer Drugs Fund managed access with live national and panel criteria.\nDo not describe as unrestricted baseline commissioning.",
    },
    "nonroutine": {
        "title": "TRIAL / EARLY / EXCEPTIONAL ROUTES",
        "body": "Licensed, no demonstrated national route: pirtobrutinib and liso-cel, each within its exact indication.\nNo current MCL licence: bispecific options.\nEvery option requires exact live route confirmation.\nNo national route does not prove absolute unavailability, but non-routine access must never be implied.",
    },
    "safety": {
        "title": "PHARMACY AND SUPPORTIVE-CARE HOLD POINT",
        "body": "Use current SmPC and local SACT protocol for formulation, dose, schedule, modifications and administration.\nAssess infection, vaccination, viral screening, interactions, bleeding, cardiac, renal and tumour-lysis risk.\nUse dedicated CAR-T and bispecific toxicity pathways. Human pharmacy verification remains mandatory.\nClinical and pharmacy review pending — no publication authority.",
    },
}


def canonical_semantic_texts() -> dict[str, str]:
    values = dict(CANONICAL_HEADER)
    for key, node in CANONICAL_NODES.items():
        values[f"node.{key}.title"] = node["title"]
        values[f"node.{key}.body"] = node["body"]
    return values


def eid(label: str) -> str:
    return hashlib.sha1(label.encode("utf-8")).hexdigest()[:20]


def svg_text(x: int, y: int, lines: list[str], size: int = 17, colour: str = TEXT, bold_first: bool = False, line_height: int | None = None, anchor: str = "start", semantic_id: str | None = None) -> str:
    step = line_height or int(size * 1.35)
    spans: list[str] = []
    for index, line in enumerate(lines):
        weight = "700" if bold_first and index == 0 else "400"
        spans.append(f'<tspan x="{x}" dy="{0 if index == 0 else step}" font-weight="{weight}">{html.escape(line)}</tspan>')
    semantic = f' data-semantic-id="{html.escape(semantic_id, quote=True)}"' if semantic_id else ""
    return f'<text x="{x}" y="{y}"{semantic} text-anchor="{anchor}" font-family="Georgia, Times New Roman, serif" font-size="{size}" fill="{colour}">' + "".join(spans) + "</text>"


def svg_box(x: int, y: int, width: int, height: int, title: str, lines: list[str], fill: str, stroke: str = NAVY, dashed: bool = False, body_size: int = 15, body_step: int = 21, semantic_prefix: str | None = None) -> str:
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    title_size = 14 if width < 400 else 17
    return "\n".join((
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="42" rx="14" fill="{stroke}"/>',
        f'<rect x="{x}" y="{y + 28}" width="{width}" height="14" fill="{stroke}"/>',
        svg_text(x + 15, y + 28, [title], title_size, WHITE, True, semantic_id=f"node.{semantic_prefix}.title" if semantic_prefix else None),
        svg_text(x + 15, y + 63, lines, body_size, TEXT, False, body_step, semantic_id=f"node.{semantic_prefix}.body" if semantic_prefix else None),
    ))


def svg_model_box(key: str, x: int, y: int, width: int, height: int, fill: str, stroke: str = NAVY, dashed: bool = False, body_size: int = 15, body_step: int = 21, wrap_chars: int | None = None) -> str:
    node = CANONICAL_NODES[key]
    lines: list[str] = []
    for paragraph in node["body"].splitlines():
        lines.extend(textwrap.wrap(paragraph, width=wrap_chars, break_long_words=False, break_on_hyphens=False) if wrap_chars else [paragraph])
    return svg_box(
        x, y, width, height, node["title"], lines, fill,
        stroke, dashed, body_size, body_step, key,
    )


def arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{NAVY}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>'


def build_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">MCL v2.0 treatment decision algorithm</title>',
        '<desc id="desc">Non-public working preview showing diagnostic, first-line, high-risk, relapsed, cellular-therapy and access pathways for mantle cell lymphoma.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#1B2A4A"/></marker></defs>',
        f'<rect width="{W}" height="{H}" fill="{BACKGROUND}"/>',
        f'<rect width="{W}" height="105" fill="{NAVY}"/>',
        f'<rect x="700" width="300" height="105" fill="{RED}"/>',
        svg_text(38, 44, [CANONICAL_HEADER["header.title"]], 25, WHITE, True, semantic_id="header.title"),
        svg_text(38, 77, [CANONICAL_HEADER["header.code"]], 15, WHITE, semantic_id="header.code"),
        svg_text(850, 43, CANONICAL_HEADER["header.preview"].splitlines(), 16, WHITE, True, 22, "middle", "header.preview"),
        svg_model_box("diagnosis", 40, 130, 920, 130, BLUE),
        arrow(500, 260, 500, 292),
        svg_model_box("treat", 40, 292, 920, 120, GREEN),
        arrow(500, 412, 500, 446),
        svg_model_box("branch", 40, 446, 920, 105, BLUE),
        arrow(500, 551, 500, 585),
        f'<rect x="25" y="585" width="950" height="390" rx="16" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>',
        svg_text(45, 619, [CANONICAL_HEADER["group.first-line"]], 17, NAVY, True, semantic_id="group.first-line"),
        svg_model_box("fit", 40, 650, 286, 275, GREEN, wrap_chars=34),
        svg_model_box("older", 357, 650, 286, 275, GREEN, wrap_chars=34),
        svg_model_box("highrisk", 674, 650, 286, 275, PINK, RED, wrap_chars=34),
        arrow(500, 975, 500, 1010),
        f'<rect x="25" y="1010" width="950" height="445" rx="16" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>',
        svg_text(45, 1044, [CANONICAL_HEADER["group.relapsed"]], 16, NAVY, True, semantic_id="group.relapsed"),
        svg_model_box("oneline", 40, 1075, 286, 320, GREEN, wrap_chars=34),
        svg_model_box("intolerance", 357, 1075, 286, 320, BLUE, wrap_chars=34),
        svg_model_box("progression", 674, 1075, 286, 320, PINK, RED, wrap_chars=34),
        f'<path d="M817 1395 L817 1440 L262 1440 L262 1485" stroke="{NAVY}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>',
        f'<path d="M817 1440 L738 1440 L738 1485" stroke="{NAVY}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>',
        svg_model_box("ta677", 40, 1485, 445, 220, GREEN, wrap_chars=55),
        svg_model_box("nonroutine", 515, 1485, 445, 220, AMBER, RED, True, wrap_chars=55),
        arrow(500, 1705, 500, 1735),
        svg_model_box("safety", 40, 1735, 920, 205, PINK, RED),
        svg_text(40, 1980, [CANONICAL_HEADER["footer.cut-off"]], 14, MUTED, semantic_id="footer.cut-off"),
        svg_text(40, 2012, [CANONICAL_HEADER["footer.warning"]], 14, RED, True, semantic_id="footer.warning"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def wrap_text(text: str, width: int, size: int) -> str:
    max_chars = max(8, int(width / (size * 0.54)))
    result: list[str] = []
    for paragraph in text.splitlines() or [""]:
        result.extend(textwrap.wrap(paragraph, width=max_chars, break_long_words=False, break_on_hyphens=False) or [""])
    return "\n".join(result)


def excalidraw_rect(label: str, x: int, y: int, width: int, height: int, fill: str, stroke: str = NAVY, dashed: bool = False) -> dict[str, object]:
    return {
        "id": eid("rect:" + label), "type": "rectangle", "x": x, "y": y, "width": width, "height": height,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "groupIds": [],
        "frameId": None, "index": None, "roundness": {"type": 3}, "seed": int(eid(label)[:7], 16),
        "version": 1, "versionNonce": int(eid(label)[7:14], 16), "isDeleted": False, "boundElements": [],
        "updated": 0, "link": None, "locked": False,
    }


def excalidraw_text(label: str, x: int, y: int, width: int, text: str, size: int = 16, colour: str = TEXT, align: str = "left", semantic_id: str | None = None) -> dict[str, object]:
    wrapped = wrap_text(text, width, size)
    lines = wrapped.splitlines() or [""]
    measured_width = min(width, max(1, round(max(len(line) for line in lines) * size * 0.62)))
    measured_height = max(1, round(len(lines) * size * 1.25))
    if align == "center":
        x += round((width - measured_width) / 2)
    return {
        "id": eid("text:" + label), "type": "text", "x": x, "y": y, "width": measured_width, "height": measured_height,
        "angle": 0, "strokeColor": colour, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
        "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None, "index": None,
        "roundness": None, "seed": int(eid("t:" + label)[:7], 16), "version": 1,
        "versionNonce": int(eid("t:" + label)[7:14], 16), "isDeleted": False, "boundElements": [], "updated": 0,
        "link": None, "locked": False, "fontSize": size, "fontFamily": 2, "text": wrapped, "textAlign": align,
        "verticalAlign": "top", "containerId": None, "originalText": wrapped, "lineHeight": 1.25, "baseline": size,
        "customData": {"semanticId": semantic_id} if semantic_id else {},
    }


def excalidraw_arrow(label: str, x1: int, y1: int, x2: int, y2: int, points: list[list[int]] | None = None) -> dict[str, object]:
    arrow_points = points or [[0, 0], [x2 - x1, y2 - y1]]
    return {
        "id": eid("arrow:" + label), "type": "arrow", "x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1,
        "angle": 0, "strokeColor": NAVY, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None, "index": None,
        "roundness": {"type": 2}, "seed": int(eid("a:" + label)[:7], 16), "version": 1,
        "versionNonce": int(eid("a:" + label)[7:14], 16), "isDeleted": False, "boundElements": [], "updated": 0,
        "link": None, "locked": False, "points": arrow_points, "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False,
    }


def add_excalidraw_box(elements: list[dict[str, object]], key: str, x: int, y: int, width: int, height: int, fill: str, stroke: str = NAVY, dashed: bool = False) -> None:
    node = CANONICAL_NODES[key]
    elements.append(excalidraw_rect(key, x, y, width, height, fill, stroke, dashed))
    elements.append(excalidraw_rect(key + ":head", x, y, width, 42, stroke, stroke))
    elements.append(excalidraw_text(key + ":title", x + 14, y + 11, width - 28, node["title"], 14, WHITE, semantic_id=f"node.{key}.title"))
    elements.append(excalidraw_text(key + ":body", x + 14, y + 55, width - 28, node["body"], 14, TEXT, semantic_id=f"node.{key}.body"))


def build_excalidraw() -> dict[str, object]:
    elements: list[dict[str, object]] = [
        excalidraw_rect("page", 0, 0, W, H, BACKGROUND, BACKGROUND),
        excalidraw_rect("header", 0, 0, W, 105, NAVY, NAVY),
        excalidraw_rect("preview", 700, 0, 300, 105, RED, RED),
        excalidraw_text("header-title", 38, 24, 620, CANONICAL_HEADER["header.title"], 25, WHITE, semantic_id="header.title"),
        excalidraw_text("header-code", 38, 63, 650, CANONICAL_HEADER["header.code"], 14, WHITE, semantic_id="header.code"),
        excalidraw_text("preview-text", 725, 26, 250, CANONICAL_HEADER["header.preview"], 16, WHITE, "center", "header.preview"),
        excalidraw_rect("first-line-group", 25, 585, 950, 390, WHITE, NAVY),
        excalidraw_text("first-line-group-title", 45, 596, 900, CANONICAL_HEADER["group.first-line"], 17, NAVY, semantic_id="group.first-line"),
        excalidraw_rect("relapsed-group", 25, 1010, 950, 445, WHITE, NAVY),
        excalidraw_text("relapsed-group-title", 45, 1021, 900, CANONICAL_HEADER["group.relapsed"], 16, NAVY, semantic_id="group.relapsed"),
    ]
    boxes = [
        ("diagnosis", 40, 130, 920, 130, BLUE, NAVY, False),
        ("treat", 40, 292, 920, 120, GREEN, NAVY, False),
        ("branch", 40, 446, 920, 105, BLUE, NAVY, False),
        ("fit", 40, 650, 286, 275, GREEN, NAVY, False),
        ("older", 357, 650, 286, 275, GREEN, NAVY, False),
        ("highrisk", 674, 650, 286, 275, PINK, RED, False),
        ("oneline", 40, 1075, 286, 320, GREEN, NAVY, False),
        ("intolerance", 357, 1075, 286, 320, BLUE, NAVY, False),
        ("progression", 674, 1075, 286, 320, PINK, RED, False),
        ("ta677", 40, 1485, 445, 220, GREEN, NAVY, False),
        ("nonroutine", 515, 1485, 445, 220, AMBER, RED, True),
        ("safety", 40, 1735, 920, 205, PINK, RED, False),
    ]
    for box in boxes:
        add_excalidraw_box(elements, *box)
    for index, coordinates in enumerate(((500, 260, 500, 292), (500, 412, 500, 446), (500, 551, 500, 585), (500, 975, 500, 1010))):
        elements.append(excalidraw_arrow(str(index), *coordinates))
    elements.append(excalidraw_arrow("progression-ta677", 817, 1395, 262, 1485, [[0, 0], [0, 45], [-555, 45], [-555, 90]]))
    elements.append(excalidraw_arrow("progression-other", 817, 1395, 738, 1485, [[0, 0], [0, 45], [-79, 45], [-79, 90]]))
    elements.append(excalidraw_arrow("to-safety", 500, 1705, 500, 1735))
    elements.append(excalidraw_text("footer-one", 40, 1980, 920, CANONICAL_HEADER["footer.cut-off"], 14, MUTED, semantic_id="footer.cut-off"))
    elements.append(excalidraw_text("footer-two", 40, 2012, 920, CANONICAL_HEADER["footer.warning"], 14, RED, semantic_id="footer.warning"))
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": BACKGROUND},
        "files": {},
    }


def build_algorithm(output_dir: Path = DEFAULT_OUTPUT) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_path = output_dir / "algorithm-working.svg"
    excalidraw_path = output_dir / "algorithm-working.excalidraw"
    svg_path.write_text(build_svg(), encoding="utf-8")
    excalidraw_path.write_text(json.dumps(build_excalidraw(), indent=2) + "\n", encoding="utf-8")
    return {"svg": svg_path, "excalidraw": excalidraw_path}


def main() -> int:
    for path in build_algorithm().values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
