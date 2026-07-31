#!/usr/bin/env python3
"""Convert the four canonical MCL v2.1 SVGs into editable Excalidraw scenes."""

from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "sources" / "mcl" / "v2.1" / "diagrams-c5"
OUTPUT = ROOT / "docs" / "mcl-v2.1" / "web-preview"
FILES = ("first-line", "high-risk", "relapsed", "access-route")
SVG_NS = "{http://www.w3.org/2000/svg}"


def eid(label: str) -> str:
    return hashlib.sha1(label.encode("utf-8")).hexdigest()[:20]


def number(value: str | None, default: float = 0) -> float:
    if value is None:
        return default
    return float(re.sub(r"[^0-9.+-]", "", value) or default)


def common(label: str, kind: str, x: float, y: float, width: float, height: float, stroke: str, fill: str, stroke_width: float, roughness: int = 0) -> dict[str, object]:
    return {
        "id": eid(label), "type": kind, "x": x, "y": y, "width": width, "height": height,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid",
        "strokeWidth": stroke_width, "strokeStyle": "solid", "roughness": roughness, "opacity": 100,
        "groupIds": [], "frameId": None, "index": None, "roundness": None,
        "seed": int(eid("seed:" + label)[:7], 16), "version": 1,
        "versionNonce": int(eid("nonce:" + label)[:7], 16), "isDeleted": False,
        "boundElements": [], "updated": 0, "link": None, "locked": False,
    }


def path_points(data: str) -> list[list[float]]:
    tokens = re.findall(r"[MLHV]|-?\d+(?:\.\d+)?", data)
    points: list[list[float]] = []
    x = y = 0.0
    index = 0
    command = ""
    while index < len(tokens):
        token = tokens[index]
        if token in {"M", "L", "H", "V"}:
            command = token
            index += 1
            continue
        if command in {"M", "L"}:
            x, y = float(tokens[index]), float(tokens[index + 1])
            index += 2
        elif command == "H":
            x = float(tokens[index])
            index += 1
        elif command == "V":
            y = float(tokens[index])
            index += 1
        else:
            raise ValueError(f"Unsupported SVG path: {data}")
        points.append([x, y])
    if len(points) < 2:
        raise ValueError(f"SVG path has fewer than two points: {data}")
    origin = points[0]
    return [[px - origin[0], py - origin[1]] for px, py in points]


def convert(name: str) -> Path:
    svg_path = SVG_DIR / f"{name}.svg"
    root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    viewbox = [float(value) for value in root.attrib["viewBox"].split()]
    elements: list[dict[str, object]] = []
    text_index = 0
    shape_index = 0
    for child in list(root):
        tag = child.tag.removeprefix(SVG_NS)
        if tag in {"title", "desc", "defs"}:
            continue
        label = f"{name}:{shape_index}:{tag}"
        shape_index += 1
        if tag == "rect":
            x, y = number(child.get("x")), number(child.get("y"))
            width, height = number(child.get("width")), number(child.get("height"))
            item = common(label, "rectangle", x, y, width, height, child.get("stroke", "transparent"), child.get("fill", "transparent"), number(child.get("stroke-width"), 1))
            if number(child.get("rx")):
                item["roundness"] = {"type": 3}
            elements.append(item)
        elif tag == "circle":
            radius = number(child.get("r"))
            elements.append(common(label, "ellipse", number(child.get("cx")) - radius, number(child.get("cy")) - radius, radius * 2, radius * 2, child.get("stroke", child.get("fill", "transparent")), child.get("fill", "transparent"), number(child.get("stroke-width"), 1)))
        elif tag == "text":
            text = "".join(child.itertext())
            size = number(child.get("font-size"), 12)
            width = max(1, len(text) * size * 0.58)
            height = size * 1.25
            x = number(child.get("x"))
            align = child.get("text-anchor", "start")
            if align == "middle":
                x -= width / 2
            item = common(label, "text", x, number(child.get("y")) - size, width, height, child.get("fill", "#172033"), "transparent", 1)
            item.update({
                "fontSize": size, "fontFamily": 2, "text": text, "textAlign": "center" if align == "middle" else "left",
                "verticalAlign": "top", "containerId": None, "originalText": text, "lineHeight": 1.25,
                "baseline": size, "customData": {"semanticId": f"{name}.text.{text_index}"},
            })
            text_index += 1
            elements.append(item)
        elif tag == "line":
            x1, y1, x2, y2 = (number(child.get(key)) for key in ("x1", "y1", "x2", "y2"))
            kind = "arrow" if child.get("marker-end") else "line"
            item = common(label, kind, x1, y1, x2 - x1, y2 - y1, child.get("stroke", "#1B2A4A"), "transparent", number(child.get("stroke-width"), 1))
            item.update({"points": [[0, 0], [x2 - x1, y2 - y1]], "lastCommittedPoint": None, "startBinding": None, "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow" if kind == "arrow" else None})
            elements.append(item)
        elif tag == "path":
            points = path_points(child.attrib["d"])
            first_x = re.search(r"M\s*(-?\d+(?:\.\d+)?)", child.attrib["d"])
            first_pair = re.search(r"M\s*-?\d+(?:\.\d+)?\s+(-?\d+(?:\.\d+)?)", child.attrib["d"])
            if first_x is None or first_pair is None:
                raise ValueError(f"SVG path has no absolute move origin: {child.attrib['d']}")
            absolute_x = number(first_x.group(1))
            absolute_y = number(first_pair.group(1))
            kind = "arrow" if child.get("marker-end") else "line"
            xs, ys = [point[0] for point in points], [point[1] for point in points]
            item = common(label, kind, absolute_x, absolute_y, max(xs) - min(xs), max(ys) - min(ys), child.get("stroke", "#1B2A4A"), "transparent", number(child.get("stroke-width"), 1))
            item.update({"points": points, "lastCommittedPoint": None, "startBinding": None, "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow" if kind == "arrow" else None})
            elements.append(item)
        else:
            raise ValueError(f"Unsupported visual SVG element {tag!r} in {svg_path}")

    scene = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#F7F8FA", "scrollX": 0, "scrollY": 0},
        "files": {},
        "customData": {
            "sourceSvg": svg_path.relative_to(ROOT).as_posix(),
            "viewBox": viewbox,
            "semanticTextCount": text_index,
        },
    }
    output = OUTPUT / f"{name}.excalidraw"
    output.write_text(json.dumps(scene, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for diagram in FILES:
        path = convert(diagram)
        print(path.relative_to(ROOT))
