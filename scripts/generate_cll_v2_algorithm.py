#!/usr/bin/env python3
"""Generate the editable and rendered CLL v2.0 treatment algorithm."""

from __future__ import annotations

import hashlib
import html
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "guidelines" / "cll"
SVG_PATH = OUT / "algorithm.svg"
EXCALIDRAW_PATH = OUT / "algorithm.excalidraw"

W, H = 1000, 1930
NAVY = "#1B2A4A"
RED = "#C41E3A"
TEXT = "#1F2937"
MUTED = "#5B6472"
BLUE = "#EAF0F7"
GREEN = "#EAF4ED"
PINK = "#FBECEF"
AMBER = "#FFF7E6"
WHITE = "#FFFFFF"
BORDER = "#B8C1CC"


def eid(label: str) -> str:
    return hashlib.sha1(label.encode()).hexdigest()[:20]


def svg_text(x: int, y: int, lines: list[str], size: int = 18, bold_first: bool = False, colour: str = TEXT, line_height: int | None = None, anchor: str = "start") -> str:
    lh = line_height or int(size * 1.35)
    spans = []
    for i, line in enumerate(lines):
        weight = "700" if bold_first and i == 0 else "400"
        dy = 0 if i == 0 else lh
        spans.append(f'<tspan x="{x}" dy="{dy}" font-weight="{weight}">{html.escape(line)}</tspan>')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Georgia, Times New Roman, serif" font-size="{size}" fill="{colour}">' + "".join(spans) + "</text>"


def svg_box(x: int, y: int, w: int, h: int, title: str, lines: list[str], fill: str, stroke: str = NAVY, dashed: bool = False, title_colour: str = NAVY, body_size: int = 15, body_line_height: int = 22) -> str:
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    body_y = y + 62
    title_size = 14 if w < 400 else 17
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="42" rx="14" fill="{stroke}"/>',
        f'<rect x="{x}" y="{y+28}" width="{w}" height="14" fill="{stroke}"/>',
        svg_text(x + 16, y + 28, [title], size=title_size, bold_first=True, colour=WHITE),
        svg_text(x + 16, body_y, lines, size=body_size, colour=TEXT, line_height=body_line_height),
    ])


def arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{NAVY}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>'


def build_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        '<title id="title">CLL v2.0 treatment decision algorithm</title>',
        '<desc id="desc">First-line orientation and relapsed refractory sequencing, with NICE TA1173 pirtobrutinib and separate intolerance, progression, double-exposed and double-refractory pathways.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#1B2A4A"/></marker></defs>',
        f'<rect width="{W}" height="{H}" fill="#F8FAFC"/>',
        f'<rect x="0" y="0" width="{W}" height="96" fill="{NAVY}"/>',
        f'<rect x="720" y="0" width="280" height="96" fill="{RED}"/>',
        svg_text(40, 43, ["CHRONIC LYMPHOCYTIC LEUKAEMIA"], size=24, bold_first=True, colour=WHITE),
        svg_text(40, 75, ["Treatment decision algorithm · MHA-CLL-2026-v2.0"], size=15, colour=WHITE),
        svg_text(860, 55, ["PUBLISHED", "v2.0"], size=18, bold_first=True, colour=WHITE, line_height=23, anchor="middle"),
        svg_box(40, 125, 920, 108, "1 · CONFIRM TREATMENT IS REQUIRED", [
            "Treat only when iwCLL active-disease criteria are met.",
            "If criteria are not met: active monitoring; do not treat by stage or lymphocyte count alone.",
        ], BLUE),
        arrow(500, 233, 500, 268),
        svg_box(40, 268, 650, 180, "2 · BEFORE EACH TREATMENT LINE", [
            "Record prior class, regimen, response, duration, reason for stopping and treatment-free interval.",
            "Repeat del(17p) FISH and TP53 sequencing; review fitness, renal function, TLS, infection,",
            "cardiac/bleeding risk, interactions, preference and access.",
        ], BLUE),
        svg_box(710, 268, 250, 180, "RICHTER SUSPECTED?", [
            "Sudden decline, high LDH",
            "or asymmetric growth:",
            "PET-CT + biopsy the most",
            "FDG-avid lesion.",
            "Use separate RT pathway;",
            "not ordinary R/R sequence.",
        ], PINK, stroke=RED, body_size=14, body_line_height=18),
        arrow(690, 358, 708, 358),
        arrow(500, 448, 500, 471),
        svg_box(40, 471, 920, 146, "3 · FIRST-LINE OR RELAPSED/REFRACTORY?", [
            "FIRST-LINE: TP53-abnormal disease requires targeted therapy. BSH 2025 favours zanubrutinib or",
            "acalabrutinib; fixed-duration venetoclax–obinutuzumab is an alternative where eligible.",
            "R/R: classify intolerance, progression, retained class sensitivity, double exposure and double",
            "refractoriness before choosing the next treatment.",
        ], GREEN),
        arrow(500, 617, 500, 645),
        f'<rect x="25" y="645" width="950" height="570" rx="16" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>',
        svg_text(45, 678, ["SIX INDEPENDENT R/R STATES · CLASSIFY BY EXPOSURE AND REASON FOR STOPPING"], size=16, bold_first=True, colour=NAVY),
        svg_box(40, 700, 286, 225, "BTKi NAIVE", [
            "After previous non-BTKi therapy:",
            "• acalabrutinib TA689; or",
            "• zanubrutinib TA931.",
            "Select by exact TA criteria,",
            "comorbidity, interactions and",
            "toxicity profile.",
        ], GREEN),
        svg_box(357, 700, 286, 225, "COVALENT-BTKi INTOLERANCE", [
            "No progression:",
            "consider a better-tolerated",
            "covalent BTKi or switch class",
            "according to eligibility and",
            "preference.",
            "Do not call this resistant disease.",
        ], GREEN),
        svg_box(674, 700, 286, 225, "COVALENT-BTKi PROGRESSION", [
            "If venetoclax naive: use a",
            "venetoclax-based NICE pathway",
            "when eligible.",
            "Pirtobrutinib TA1173 when its",
            "specific restriction is met.",
        ], PINK, stroke=RED),
        svg_box(40, 955, 286, 235, "RELAPSE OFF FIXED-DURATION", [
            "Previous response; relapse off therapy:",
            "consider BTKi or selected venetoclax",
            "retreatment after reviewing response",
            "and treatment-free interval.",
            "Do not retreat primary or active-",
            "treatment resistant disease routinely.",
        ], BLUE),
        svg_box(357, 955, 286, 235, "DOUBLE EXPOSED", [
            "Both covalent BTKi and venetoclax",
            "used, but not refractory to both:",
            "individualise by retained sensitivity,",
            "prior response and NICE eligibility.",
            "Do not automatically label double",
            "refractory.",
        ], BLUE),
        svg_box(674, 955, 286, 235, "DOUBLE REFRACTORY", [
            "Progression during both classes:",
            "early tertiary and trial referral.",
            "Use pirtobrutinib when TA1173 met.",
            "Cellular therapy/alloHCT only in",
            "highly selected specialist pathways.",
            "No proven comparative hierarchy.",
        ], PINK, stroke=RED),
        svg_box(40, 1230, 920, 372, "NICE RECOMMENDATIONS AND NHS ENGLAND ACCESS · 26 JULY 2026", [
            "Evidence, marketing authorisation, NICE recommendation and NHS funding are separate determinations.",
            "TA429  Ibrutinib · previously treated CLL and restricted untreated TP53-abnormal disease.",
            "TA689  Acalabrutinib · previously treated CLL and specified untreated populations.",
            "TA931  Zanubrutinib · R/R CLL and specified untreated populations.",
            "TA561  Venetoclax–rituximab · after at least one previous therapy.",
            "TA796  Venetoclax monotherapy: (a) del(17p)/TP53 when a B-cell receptor pathway inhibitor",
            "        is unsuitable, or after progression on one; or (b) no del(17p)/TP53 after progression",
            "        following both chemoimmunotherapy and a B-cell receptor pathway inhibitor.",
            "TA1173 Pirtobrutinib for adults with R/R CLL after a BTKi, ONLY when covalent-BTKi retreatment,",
            "        including after a fixed-duration regimen, is not clinically appropriate.",
            "At the cut-off, NHS England access remained through interim Blueteq funding; routine-budget",
            "implementation was due by 29 September 2026. The broader MHRA licence does not widen funding.",
            "England access is not a single UK-wide entitlement. Check SmPC, Blueteq and local policy.",
        ], GREEN),
        svg_box(40, 1637, 920, 190, "EMERGING / SPECIALIST · NOT ROUTINE NHS CLL TREATMENT", [
            "• Pirtobrutinib–venetoclax–rituximab: phase III evidence; NICE ID6566 awaiting development.",
            "• Lisocabtagene maraleucel: efficacy evidence, but no demonstrated CLL marketing authorisation,",
            "  NICE recommendation or routine NHS England commissioning; devolved-nation access not established.",
            "• CD20×CD3 bispecifics: no qualifying prospective therapeutic trial in untransformed CLL",
            "  identified through 26 July 2026; do not extrapolate Richter/other-lymphoma evidence.",
        ], AMBER, stroke=RED, dashed=True),
        svg_text(40, 1862, ["Clinical decision-support only · verify current NICE, NHS, MHRA, SmPC and local policy before prescribing."], size=14, colour=MUTED),
        svg_text(40, 1890, ["Published 27 July 2026 · evidence cut-off 26 July 2026 · review, pharmacy verification and owner authorisation complete."], size=14, colour=RED),
        '</svg>',
    ]
    return "\n".join(parts) + "\n"


def excalidraw_rect(label: str, x: int, y: int, w: int, h: int, fill: str, stroke: str = NAVY, dashed: bool = False) -> dict:
    return {
        "id": eid("rect:" + label), "type": "rectangle", "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid",
        "strokeWidth": 2, "strokeStyle": "dashed" if dashed else "solid", "roughness": 1,
        "opacity": 100, "groupIds": [], "frameId": None, "index": None, "roundness": {"type": 3},
        "seed": int(eid(label)[:7], 16), "version": 1, "versionNonce": int(eid(label)[7:14], 16),
        "isDeleted": False, "boundElements": [], "updated": 0, "link": None, "locked": False,
    }


def wrap_excalidraw_text(text: str, width: int, size: int) -> str:
    """Wrap text conservatively for Excalidraw's Helvetica-compatible font."""
    max_chars = max(8, int(width / (size * 0.52)))
    wrapped: list[str] = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph:
            wrapped.append("")
            continue
        indent = "• " if paragraph.startswith("• ") else ""
        source = paragraph[2:] if indent else paragraph
        lines = textwrap.wrap(
            source,
            width=max_chars - len(indent),
            break_long_words=False,
            break_on_hyphens=False,
            subsequent_indent="  " if indent else "",
        ) or [""]
        lines[0] = indent + lines[0]
        wrapped.extend(lines)
    return "\n".join(wrapped)


def excalidraw_text(label: str, x: int, y: int, max_width: int, text: str, size: int = 18, colour: str = TEXT, bold: bool = False, align: str = "left", container_id: str | None = None) -> dict:
    wrapped = wrap_excalidraw_text(text, max_width, size)
    lines = wrapped.splitlines() or [""]
    measured_width = min(max_width, max(1, round(max(len(line) for line in lines) * size * 0.62)))
    measured_height = max(1, round(len(lines) * size * 1.25))
    if align == "center":
        x += round((max_width - measured_width) / 2)
    return {
        "id": eid("text:" + label), "type": "text", "x": x, "y": y, "width": measured_width, "height": measured_height,
        "angle": 0, "strokeColor": colour, "backgroundColor": "transparent", "fillStyle": "solid",
        "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100,
        "groupIds": [], "frameId": None, "index": None, "roundness": None,
        "seed": int(eid("t" + label)[:7], 16), "version": 1, "versionNonce": int(eid("t" + label)[7:14], 16),
        "isDeleted": False, "boundElements": [], "updated": 0, "link": None, "locked": False,
        "fontSize": size, "fontFamily": 2, "text": wrapped,
        "textAlign": align, "verticalAlign": "middle" if container_id else "top", "containerId": container_id,
        "originalText": wrapped, "lineHeight": 1.25, "baseline": size,
    }


def excalidraw_arrow(label: str, x1: int, y1: int, x2: int, y2: int) -> dict:
    return {
        "id": eid("arrow:" + label), "type": "arrow", "x": x1, "y": y1,
        "width": x2 - x1, "height": y2 - y1, "angle": 0, "strokeColor": NAVY,
        "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2,
        "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
        "frameId": None, "index": None, "roundness": {"type": 2},
        "seed": int(eid("a" + label)[:7], 16), "version": 1, "versionNonce": int(eid("a" + label)[7:14], 16),
        "isDeleted": False, "boundElements": [], "updated": 0, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]], "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow",
        "elbowed": False,
    }


def add_excalidraw_box(elements: list[dict], key: str, x: int, y: int, w: int, h: int, title: str, body: str, fill: str, stroke: str = NAVY, dashed: bool = False) -> None:
    elements.append(excalidraw_rect(key, x, y, w, h, fill, stroke, dashed))
    elements.append(excalidraw_rect(key + ":head", x, y, w, 42, stroke, stroke))
    elements.append(excalidraw_text(key + ":title", x + 14, y + 10, w - 28, title, 14 if w < 400 else 17, WHITE, True))
    body_rect = excalidraw_rect(key + ":body-container", x + 4, y + 44, w - 8, h - 48, "transparent", "transparent")
    body_rect["roughness"] = 0
    body_text = excalidraw_text(
        key + ":body", x + 14, y + 54, w - 28, body, 15, TEXT,
        container_id=body_rect["id"],
    )
    body_text["y"] = body_rect["y"] + (body_rect["height"] - body_text["height"]) / 2
    body_rect["boundElements"] = [{"type": "text", "id": body_text["id"]}]
    elements.extend([body_rect, body_text])


def build_excalidraw() -> dict:
    e: list[dict] = []
    e.append(excalidraw_rect("page", 0, 0, W, H, "#F8FAFC", "#F8FAFC"))
    e.append(excalidraw_rect("header", 0, 0, W, 96, NAVY, NAVY))
    e.append(excalidraw_rect("status", 720, 0, 280, 96, RED, RED))
    e.append(excalidraw_text("header-title", 40, 24, 650, "CHRONIC LYMPHOCYTIC LEUKAEMIA", 24, WHITE, True))
    e.append(excalidraw_text("header-code", 40, 58, 650, "Treatment decision algorithm · MHA-CLL-2026-v2.0", 15, WHITE))
    e.append(excalidraw_text("status-text", 770, 26, 180, "PUBLISHED\nv2.0", 18, WHITE, True, "center"))
    e.append(excalidraw_rect("rr-states-panel", 25, 645, 950, 570, WHITE, NAVY))
    e.append(excalidraw_text("rr-states-title", 45, 658, 910, "SIX INDEPENDENT R/R STATES · CLASSIFY BY EXPOSURE AND REASON FOR STOPPING", 16, NAVY, True))

    boxes = [
        ("confirm", 40, 125, 920, 108, "1 · CONFIRM TREATMENT IS REQUIRED", "Treat only when iwCLL active-disease criteria are met.\nIf criteria are not met: active monitoring; do not treat by stage or lymphocyte count alone.", BLUE, NAVY, False),
        ("before", 40, 268, 650, 180, "2 · BEFORE EACH TREATMENT LINE", "Record prior class, regimen, response, duration and reason for stopping.\nRepeat del(17p) FISH and TP53 sequencing; review fitness, renal function, TLS, infection, cardiac/bleeding risk, interactions, preference and access.", BLUE, NAVY, False),
        ("richter", 710, 268, 250, 180, "RICHTER SUSPECTED?", "Sudden decline, high LDH\nor asymmetric growth:\nPET-CT + biopsy the most\nFDG-avid lesion.\nUse separate RT pathway;\nnot ordinary R/R sequence.", PINK, RED, False),
        ("route", 40, 471, 920, 146, "3 · FIRST-LINE OR RELAPSED/REFRACTORY?", "FIRST-LINE: targeted therapy for TP53-abnormal disease; BSH 2025 favours zanubrutinib/acalabrutinib.\nR/R: classify intolerance, progression, retained sensitivity, double exposure and double refractoriness.", GREEN, NAVY, False),
        ("naive", 40, 700, 286, 225, "BTKi NAIVE", "After non-BTKi therapy:\n• acalabrutinib TA689; or\n• zanubrutinib TA931.\nSelect by exact criteria, comorbidity, interactions and toxicity.", GREEN, NAVY, False),
        ("intolerance", 357, 700, 286, 225, "COVALENT-BTKi INTOLERANCE", "No progression:\nconsider a better-tolerated covalent BTKi or switch class.\nDo not call this resistant disease.", GREEN, NAVY, False),
        ("progression", 674, 700, 286, 225, "COVALENT-BTKi PROGRESSION", "If venetoclax naive: use a venetoclax-based NICE pathway when eligible.\nPirtobrutinib TA1173 when its restriction is met.", PINK, RED, False),
        ("postven", 40, 955, 286, 235, "RELAPSE OFF FIXED-DURATION", "Previous response; relapse off venetoclax:\nconsider BTKi or selected retreatment after reviewing response and interval.\nDo not retreat resistant disease routinely.", BLUE, NAVY, False),
        ("doubleexposed", 357, 955, 286, 235, "DOUBLE EXPOSED", "Both classes used but not refractory to both:\nindividualise by retained sensitivity, prior response and eligibility.\nDo not automatically label double refractory.", BLUE, NAVY, False),
        ("doubleref", 674, 955, 286, 235, "DOUBLE REFRACTORY", "Progression during both classes:\nearly tertiary/trial referral.\nPirtobrutinib if TA1173 met.\nHighly selected cellular therapy/alloHCT discussion.", PINK, RED, False),
        ("nice", 40, 1230, 920, 372, "NICE RECOMMENDATIONS AND NHS ENGLAND ACCESS · 26 JULY 2026", "Evidence, marketing authorisation, NICE recommendation and NHS funding are separate determinations.\nTA429 Ibrutinib · TA689 Acalabrutinib · TA931 Zanubrutinib · TA561 Venetoclax–rituximab\nTA796: (a) del(17p)/TP53 when a B-cell receptor pathway inhibitor is unsuitable, or after progression on one; or (b) no del(17p)/TP53 after progression following both chemoimmunotherapy and a B-cell receptor pathway inhibitor.\nTA1173: pirtobrutinib for adults with R/R CLL after a BTKi, only when covalent-BTKi retreatment, including after a fixed-duration regimen, is not clinically appropriate.\nAt the cut-off, NHS England access remained through interim Blueteq funding; routine-budget implementation was due by 29 September 2026. The broader MHRA licence does not widen funding.\nEngland access is not a single UK-wide entitlement. Check SmPC, Blueteq and local policy.", GREEN, NAVY, False),
        ("emerging", 40, 1637, 920, 190, "EMERGING / SPECIALIST · NOT ROUTINE NHS CLL TREATMENT", "• Pirtobrutinib–venetoclax–rituximab: phase III; NICE ID6566 awaiting development.\n• Liso-cel: no demonstrated CLL marketing authorisation, NICE recommendation or routine NHS England commissioning; devolved-nation access not established.\n• CD20×CD3 bispecifics: no qualifying prospective untransformed-CLL trial found by cut-off.", AMBER, RED, True),
    ]
    for args in boxes:
        add_excalidraw_box(e, *args)
    for idx, coords in enumerate([
        (500,233,500,268), (690,358,708,358), (500,448,500,471), (500,617,500,645),
    ]):
        e.append(excalidraw_arrow(str(idx), *coords))
    e.append(excalidraw_text("footer1", 40, 1852, 920, "Clinical decision-support only · verify current NICE, NHS, MHRA, SmPC and local policy before prescribing.", 14, MUTED))
    e.append(excalidraw_text("footer2", 40, 1880, 920, "Published 27 July 2026 · evidence cut-off 26 July 2026 · review, pharmacy verification and owner authorisation complete.", 14, RED))
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": e,
        "appState": {"gridSize": None, "viewBackgroundColor": "#F8FAFC"},
        "files": {},
    }


def main() -> None:
    SVG_PATH.write_text(build_svg(), encoding="utf-8")
    EXCALIDRAW_PATH.write_text(json.dumps(build_excalidraw(), indent=2) + "\n", encoding="utf-8")
    print(SVG_PATH)
    print(EXCALIDRAW_PATH)


if __name__ == "__main__":
    main()
