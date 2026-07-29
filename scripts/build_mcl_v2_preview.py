#!/usr/bin/env python3
"""Build the complete non-public MCL v2.0 review artefact family."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_mcl_v2_algorithm import build_algorithm
from scripts.generate_mcl_v2_documents import build_documents
from scripts.generate_mcl_v2_release import build_preview

DEFAULT_OUTPUT = ROOT / "docs" / "mcl-v2" / "preview"
CONTROLLED_INPUTS = (
    ROOT / "sources" / "mcl" / "source-v2.0.html",
    ROOT / "sources" / "mcl" / "status-matrix-v2.0.json",
    ROOT / "sources" / "mcl" / "release-state-v2.0.json",
    ROOT / "docs" / "mcl-v2" / "evidence-ledger.json",
    ROOT / "docs" / "mcl-v2" / "claims-matrix.json",
    ROOT / "docs" / "mcl-v2" / "access-evidence-ledger.json",
    ROOT / "docs" / "mcl-v2" / "source-register.json",
    ROOT / "scripts" / "generate_mcl_v2_release.py",
    ROOT / "scripts" / "generate_mcl_v2_documents.py",
    ROOT / "scripts" / "generate_mcl_v2_algorithm.py",
    ROOT / "scripts" / "build_mcl_v2_preview.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def convert_docx_pair(output_dir: Path, guideline: Path, quickref: Path) -> tuple[Path, Path]:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("LibreOffice soffice is required to generate MCL v2.0 preview PDFs")
    with tempfile.TemporaryDirectory(prefix="mcl-v2-libreoffice-") as profile:
        profile_uri = (Path(profile) / "profile").resolve().as_uri()
        result = subprocess.run(
            [
                soffice,
                "--headless",
                f"-env:UserInstallation={profile_uri}",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(guideline),
                str(quickref),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice PDF conversion failed: {result.stderr or result.stdout}")
    guideline_pdf = output_dir / f"{guideline.stem}.pdf"
    quickref_pdf = output_dir / f"{quickref.stem}.pdf"
    if not guideline_pdf.is_file() or not quickref_pdf.is_file():
        raise RuntimeError(f"LibreOffice did not produce both PDFs: {result.stdout} {result.stderr}")
    return guideline_pdf, quickref_pdf


def artefact_record(path: Path) -> dict[str, object]:
    record: dict[str, object] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    if path.suffix.lower() == ".pdf":
        with fitz.open(path) as document:
            record["pages"] = document.page_count
    return record


def build_multiformat_preview(output_dir: Path = DEFAULT_OUTPUT) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    html = output_dir / "index.html"
    build_preview(output_path=html)
    documents = build_documents(output_dir)
    algorithm = build_algorithm(output_dir)
    guideline_pdf, quickref_pdf = convert_docx_pair(output_dir, documents["guideline"], documents["quickref"])

    outputs = {
        "html": html,
        "guideline_docx": documents["guideline"],
        "guideline_pdf": guideline_pdf,
        "quickref_docx": documents["quickref"],
        "quickref_pdf": quickref_pdf,
        "algorithm_svg": algorithm["svg"],
        "algorithm_excalidraw": algorithm["excalidraw"],
    }
    manifest = {
        "schema_version": 1,
        "document_code": "MHA-MCL-2026-v2.0",
        "status": "WORKING_PREVIEW",
        "publication_authority": False,
        "evidence_access_cut_off": "2026-07-28",
        "controlled_inputs": {
            path.relative_to(ROOT).as_posix(): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in CONTROLLED_INPUTS
        },
        "artefacts": {path.name: artefact_record(path) for path in outputs.values()},
    }
    manifest_path = output_dir / "build-manifest-working.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    outputs["manifest"] = manifest_path
    return outputs


def main() -> int:
    outputs = build_multiformat_preview()
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
