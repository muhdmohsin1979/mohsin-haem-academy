#!/usr/bin/env python3
"""Build reviewed MCL v2.1 DOCX/PDF artefacts from the exact reviewed web preview."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "docs" / "mcl-v2.1" / "web-preview"
SOURCE = PREVIEW / "index.html"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match is None:
        raise AssertionError(f"Unable to extract {label}")
    return match.group(0)


def convert_html(html: str, stem: str) -> tuple[Path, Path]:
    html_path = PREVIEW / f"{stem}.html"
    docx_path = PREVIEW / f"{stem}.docx"
    pdf_path = PREVIEW / f"{stem}.pdf"
    html_path.write_text(html, encoding="utf-8")
    subprocess.run(["textutil", "-convert", "docx", "-output", str(docx_path), str(html_path)], check=True, timeout=180)
    with tempfile.TemporaryDirectory(prefix="mcl-v21-libreoffice-") as profile:
        result = subprocess.run(
            [
                shutil.which("soffice") or "soffice", "--headless",
                f"-env:UserInstallation={(Path(profile) / 'profile').resolve().as_uri()}",
                "--convert-to", "pdf", "--outdir", str(PREVIEW), str(docx_path),
            ],
            text=True, capture_output=True, timeout=240,
        )
    if result.returncode or not pdf_path.is_file():
        raise RuntimeError(result.stderr or result.stdout or f"No PDF produced for {docx_path}")
    html_path.unlink()
    return docx_path, pdf_path


def build() -> dict[str, Path]:
    source = SOURCE.read_text(encoding="utf-8")
    style = extract(r"<style>[\s\S]*?</style>", source, "stylesheet")
    hero = extract(r"<header class=\"page-hero\">[\s\S]*?</header>", source, "hero")
    main = extract(r"<main class=\"gl-main\" id=\"main-content\">[\s\S]*?</main>", source, "main content")
    footer = extract(r"<footer class=\"page-footer\">[\s\S]*?</footer>", source, "footer")
    common_head = (
        "<!doctype html><html lang=\"en-GB\"><head><meta charset=\"utf-8\">"
        "<title>MCL v2.1 controlled reviewed document</title>" + style +
        "<style>body{background:white}.gl-main{width:100%;margin:0}.fig-scroll,.tbl-wrap{overflow:visible}"
        "svg.pathway{min-width:0;width:100%}.draft-banner{display:block}.vh{position:static;width:auto;height:auto;clip:auto}"
        "</style></head><body>"
    )
    guideline_html = common_head + hero + main + footer + "</body></html>"
    guideline_docx, guideline_pdf = convert_html(guideline_html, "guideline-v2.1-reviewed")

    quick = extract(
        r"<h3>One-page quick reference</h3>[\s\S]*?(?=<h3>How the classifications are assigned</h3>)",
        source,
        "quick reference",
    )
    warning = extract(r"<aside class=\"draft-banner\"[\s\S]*?</aside>", source, "review warning")
    quick_html = (
        common_head + hero + warning +
        "<main class=\"gl-main\"><section><h2>MCL v2.1 quick reference</h2>" + quick +
        "</section></main>" + footer + "</body></html>"
    )
    quick_docx, quick_pdf = convert_html(quick_html, "quickref-v2.1-reviewed")

    outputs = {
        "guideline_docx": guideline_docx,
        "guideline_pdf": guideline_pdf,
        "quickref_docx": quick_docx,
        "quickref_pdf": quick_pdf,
    }
    manifest = {
        "schema_version": 1,
        "document_code": "MHA-MCL-2026-v2.1-PREVIEW-RC1",
        "status": "CONTROLLED_REVIEWED_PREVIEW",
        "publication_authority": False,
        "source_html_sha256": sha256(SOURCE),
        "artefacts": {
            path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs.values()
        },
    }
    manifest_path = PREVIEW / "manifest-reviewed-documents.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    outputs["manifest"] = manifest_path
    return outputs


if __name__ == "__main__":
    for label, path in build().items():
        print(f"{label}: {path.relative_to(ROOT)} sha256={sha256(path)}")
