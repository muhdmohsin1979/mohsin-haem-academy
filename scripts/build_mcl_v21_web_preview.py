#!/usr/bin/env python3
"""Build the deterministic MCL v2.1 reviewed web preview from exact C5 bytes."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "mcl" / "v2.1"
SOURCE = SOURCE_DIR / "accessibility-corrected-c5.html"
ATTESTATION = SOURCE_DIR / "review-attestation.json"
OUTPUT = ROOT / "docs" / "mcl-v2.1" / "web-preview"
EXPECTED_C4_SHA256 = "f16545565f7cb0c3619aa2ccff87f1fecd2ecc5718d4dae4d0960a09e9f77957"
EXPECTED_C5_SHA256 = "3b073bcaa8887018702cb2af53d4e655c59b82e7c7e2333548feb14d3bb4fba2"
DIAGRAMS = ("first-line.svg", "high-risk.svg", "relapsed.svg", "access-route.svg")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"Expected exactly one reviewed-C5 release label, found {count}: {old[:90]!r}")
    return text.replace(old, new)


def build() -> dict[str, Path]:
    if sha256(SOURCE) != EXPECTED_C5_SHA256:
        raise AssertionError("Accessibility-corrected C5 bytes changed")

    text = SOURCE.read_text(encoding="utf-8")
    replacements = (
        ('<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="noindex, nofollow, noarchive">'),
        ('<title>Mantle Cell Lymphoma guideline v2.1 — unratified draft</title>', '<title>Mantle Cell Lymphoma guideline v2.1 — controlled reviewed preview</title>'),
        ('<span class="preview">DRAFT — NOT FOR CLINICAL USE</span>', '<span class="preview">CONTROLLED REVIEWED PREVIEW — NOT FOR CLINICAL USE</span>'),
        ('MHA-MCL-2026-v2.1-DRAFT · evidence and access cut-off 2026-07-30 · supersedes nothing until ratified', 'MHA-MCL-2026-v2.1-PREVIEW-RC1 · evidence and access cut-off 2026-07-30 · supersedes nothing until exact production hashes are ratified'),
        ('<strong id="draft-warning-heading">Unratified working draft. Not for clinical use.</strong>', '<strong id="draft-warning-heading">Controlled reviewed preview. Not for clinical use.</strong>'),
        ('<p>This is a revision candidate prepared for the accountable owner. Independent clinical review is <strong>PENDING</strong> and pharmacy verification is <strong>PENDING</strong> for all material added since v2.0. It carries no publication authority and must not be used to make a treatment or funding decision. The published guideline remains v2.0.</p>', '<p>This exact substantive candidate passed independent clinical review and pharmacy verification; reviewer identities are retained privately. It remains a controlled preview with no publication authority until the complete release family is generated, verified and its exact production hashes are ratified. The published guideline remains v2.0.</p>'),
        ('Those corrections do <strong>not</strong> change the release state: this remains unratified, clinical review and pharmacy verification remain pending, and publication authority remains false.', 'Those corrections were included in the exact candidate that passed independent clinical review and pharmacy verification. Publication authority remains false for this preview pending complete release-family verification and exact production-hash ratification.'),
        ('<tr><th scope="row">Document code</th><td>MHA-MCL-2026-v2.1-DRAFT</td></tr>', '<tr><th scope="row">Document code</th><td>MHA-MCL-2026-v2.1-PREVIEW-RC1</td></tr>'),
        ('<tr><th scope="row">State</th><td>DRAFT — NOT FOR CLINICAL USE</td></tr>', '<tr><th scope="row">State</th><td>CONTROLLED REVIEWED PREVIEW — NOT FOR CLINICAL USE</td></tr>'),
        ('<tr><th scope="row">Owner scope approval</th><td>PENDING — owner scope approval for v2.1 not yet given</td></tr>', '<tr><th scope="row">Owner scope approval</th><td>APPROVED — owner directed controlled production replacement on 31 July 2026</td></tr>'),
        ('<tr><th scope="row">Independent clinical review</th><td>PENDING — not yet performed for v2.1 content</td></tr>', '<tr><th scope="row">Independent clinical review</th><td>PASS — reviewer identity retained privately</td></tr>'),
        ('<tr><th scope="row">Pharmacy verification</th><td>PENDING — v2.0 verification does not extend to v2.1 additions</td></tr>', '<tr><th scope="row">Pharmacy verification</th><td>COMPLETE — verifier identity retained privately</td></tr>'),
        ('<tr><th scope="row">Publication authority</th><td>FALSE — no publication authority</td></tr>', '<tr><th scope="row">Publication authority</th><td>FALSE — complete release family and exact production-hash ratification pending</td></tr>\n<tr><th scope="row">Reviewed substantive candidate</th><td>SHA-256 <code style="word-break:break-all;">f16545565f7cb0c3619aa2ccff87f1fecd2ecc5718d4dae4d0960a09e9f77957</code></td></tr>\n<tr><th scope="row">Accessibility correction</th><td>SHA-256 <code style="word-break:break-all;">3b073bcaa8887018702cb2af53d4e655c59b82e7c7e2333548feb14d3bb4fba2</code> — generated diagram colour token only; no clinical-content change</td></tr>\n<tr><th scope="row">Change from reviewed candidate</th><td>One generated diagram colour token plus release-control presentation; no clinical-content change</td></tr>'),
        ('MHA-MCL-2026-v2.1-DRAFT · unratified working draft, not for clinical use', 'MHA-MCL-2026-v2.1-PREVIEW-RC1 · controlled reviewed preview, not for clinical use'),
    )
    for old, new in replacements:
        text = replace_once(text, old, new)

    pharmacy_replacements = (
        (
            "REPORT_ONLY_NOT_PHARMACY_VERIFIED — exact MHRA SmPC quotations validated; human pharmacy verification pending.",
            "PHARMACY_VERIFIED — exact MHRA SmPC quotations validated; human pharmacy verification recorded 31 July 2026 on owner attestation, verifier identity retained privately.",
            10,
        ),
        (
            "REPORT_ONLY_TRIAL_AND_GUIDELINE_SCHEDULE_NOT_PHARMACY_VERIFIED",
            "PHARMACY_VERIFIED_TRIAL_AND_GUIDELINE_SCHEDULE — recorded 31 July 2026 on owner attestation",
            1,
        ),
        (
            "REPORT_ONLY_TRIAL_SCHEDULE_NOT_PHARMACY_VERIFIED",
            "PHARMACY_VERIFIED_TRIAL_SCHEDULE — recorded 31 July 2026 on owner attestation",
            1,
        ),
    )
    for old, new, expected_count in pharmacy_replacements:
        count = text.count(old)
        if count != expected_count:
            raise AssertionError(f"Unexpected pharmacy status count for {old!r}: {count}")
        text = text.replace(old, new)

    attestation_anchor = "      </tbody>\n    </table>\n  </section>\n    </main>"
    attestation_text = (
        "      </tbody>\n    </table>\n"
        "    <h3>Attestation record</h3>\n"
        "    <p>The clinical-review and pharmacy gates were cleared by the accountable owner on 31 July 2026. "
        "Verifier identities are retained privately at the owner&rsquo;s instruction and appear in no public file, manifest or commit.</p>\n"
        "    <ul>\n"
        "      <li>The build records the owner&rsquo;s attestation; it did not witness either review.</li>\n"
        "      <li>The attestation binds to substantive candidate <code style=\"word-break:break-all;\">"
        + EXPECTED_C4_SHA256
        + "</code>. The C5 accessibility correction changes one generated diagram colour token only.</li>\n"
        "      <li>These cleared gates do not grant publication authority to this preview. Exact production-hash ratification remains pending.</li>\n"
        "    </ul>\n"
        "  </section>\n    </main>"
    )
    text = replace_once(text, attestation_anchor, attestation_text)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    html = OUTPUT / "index.html"
    html.write_text(text, encoding="utf-8")
    outputs: dict[str, Path] = {"html": html}
    for name in DIAGRAMS:
        target = OUTPUT / name
        shutil.copyfile(SOURCE_DIR / "diagrams-c5" / name, target)
        outputs[name] = target

    axe_report = OUTPUT / "axe-report.json"
    axe_status: dict[str, object] = {"status": "NOT_RUN"}
    known_release_blocks = [
        "OFFICIAL_EXCALIDRAW_RENDER_NOT_VERIFIED",
        "EXACT_PRODUCTION_HASH_RATIFICATION_PENDING",
    ]
    excalidraw_paths = [OUTPUT / f"{Path(name).stem}.excalidraw" for name in DIAGRAMS]
    if all(path.is_file() for path in excalidraw_paths):
        for path in excalidraw_paths:
            outputs[path.name] = path
    else:
        known_release_blocks.insert(0, "EXCALIDRAW_PARITY_NOT_COMPLETE")

    document_paths = [
        OUTPUT / "guideline-v2.1-reviewed.docx",
        OUTPUT / "guideline-v2.1-reviewed.pdf",
        OUTPUT / "quickref-v2.1-reviewed.docx",
        OUTPUT / "quickref-v2.1-reviewed.pdf",
        OUTPUT / "manifest-reviewed-documents.json",
    ]
    if all(path.is_file() for path in document_paths):
        for path in document_paths:
            outputs[path.name] = path
    else:
        known_release_blocks.insert(0, "DOCX_PDF_QUICKREF_NOT_GENERATED")
    if axe_report.is_file():
        report = json.loads(axe_report.read_text(encoding="utf-8"))
        violations = [
            violation
            for viewport in report.get("viewports", {}).values()
            for violation in viewport.get("violations", [])
        ]
        if violations:
            raise AssertionError("Existing Axe report contains violations")
        axe_status = {
            "status": "PASS",
            "axe_version": report.get("axeVersion"),
            "viewports": sorted(report.get("viewports", {})),
            "report_sha256": sha256(axe_report),
        }
        outputs["axe_report"] = axe_report
    else:
        known_release_blocks.insert(0, "OFFLINE_AXE_NOT_RUN")

    manifest = {
        "schema_version": 1,
        "document_code": "MHA-MCL-2026-v2.1-PREVIEW-RC1",
        "status": "REVIEWED_WEB_PREVIEW_INCOMPLETE_RELEASE_FAMILY",
        "publication_authority": False,
        "reviewed_substantive_candidate": {
            "file": (SOURCE_DIR / "reviewed-candidate-c4.html").relative_to(ROOT).as_posix(),
            "sha256": EXPECTED_C4_SHA256,
            "bytes": (SOURCE_DIR / "reviewed-candidate-c4.html").stat().st_size,
        },
        "accessibility_corrected_candidate": {
            "file": SOURCE.relative_to(ROOT).as_posix(),
            "sha256": EXPECTED_C5_SHA256,
            "bytes": SOURCE.stat().st_size,
            "change_from_reviewed_candidate": "One generated diagram colour token; no clinical-content change",
        },
        "review_attestation": {
            "file": ATTESTATION.relative_to(ROOT).as_posix(),
            "sha256": sha256(ATTESTATION),
        },
        "accessibility_assurance": axe_status,
        "clinical_change_from_reviewed_candidate": "NONE; one generated diagram colour token plus release-control presentation",
        "known_release_blocks": known_release_blocks,
        "artefacts": {
            path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs.values()
        },
    }
    manifest_path = OUTPUT / "manifest-reviewed-web-preview.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    outputs["manifest"] = manifest_path
    return outputs


if __name__ == "__main__":
    for label, path in build().items():
        print(f"{label}: {path.relative_to(ROOT)} sha256={sha256(path)}")
