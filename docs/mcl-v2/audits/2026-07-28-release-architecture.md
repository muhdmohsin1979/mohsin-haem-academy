<!--
Independent report provenance: deleg_74e3562e/task-2
Cut-off: 28 July 2026
Status: working evidence input; not publication wording or release approval
Original source: Hermes independent delegation report retained outside the repository
-->

## Outcome

Designed a minimal, fail-closed MCL v2.0 release architecture based on the repository’s CLL v2 pattern, while preserving the current MCL withdrawal containment until an exact production family is reviewed, authorised and deployed.

### Repository findings

- Baseline confirmed:
  - Branch: `feat/mcl-v2-20260728`
  - HEAD: `d4a306846c53a4b790162e1e4127bb87b16250e3`
  - MCL v1.x remains withdrawn under `scripts/validate_mcl_containment.py`.
- The CLL v2 pattern provides:
  - Seven controlled public artefacts.
  - Deterministic diagram generation.
  - DOCX generation from controlled content and isolated LibreOffice PDF conversion.
  - Approval-bound SHA-256 manifest.
  - Closed-schema release record.
  - Cross-format validator and official Excalidraw render check.
  - Dedicated macOS CI gate.
- Historical MCL at `c2ed57a` had concrete reproducibility and governance defects:
  - Public HTML was labelled `v1.6.0` and “Published” while JSON-LD said `reviewedBy: Pending external review`.
  - HTML still said the next access check was due “before publication”.
  - Numerous unresolved `[VERIFY]` and `[VERIFY current NICE…]` markers remained on public clinical surfaces.
  - DOCX remained `v1.5.3-DRAFT`, including filename-internal metadata, header and document code, while HTML and SVGs claimed published `v1.6.0`.
  - DOCX core properties still described “UK MCL Guideline (Draft v1.0)”.
  - Mermaid source remained `v1.5.4-DRAFT`.
  - HTML comments/CSS referred to several other versions, including `v1.5.2`, `v1.5.5` and `v1.6.2`.
  - HTML, DOCX, SVG, Excalidraw, PNG and PDF assets had no common generator, canonical status matrix, manifest, release record or semantic parity gate.
  - Diagram history shows repeated manual overlap and canvas-width repairs, confirming absent deterministic layout validation.
  - The three editable Excalidraw scenes were independent reduced-content recreations rather than generated companions to the SVGs.

## Proposed MCL v2.0 file architecture

### Controlled, non-public inputs

Use the already blocked `/sources` prefix:

- `sources/mcl/source-v2.0.html`
  - Canonical clinical prose and stable section IDs.
  - Mark complete clinical units with stable IDs and explicit full-guideline, quick-reference and algorithm inclusion attributes.
- `sources/mcl/status-matrix-v2.0.json`
  - Canonical treatment, regulatory and access assertions.
  - Closed schema and duplicate-key rejection.
  - Each treatment record should separate:
    - evidence position;
    - marketing authorisation;
    - NICE recommendation/appraisal;
    - NHS England funding and implementation;
    - devolved-nation status;
    - population and line;
    - regimen, dose, schedule and duration;
    - access-check date and primary URL;
    - exact approved public wording.
- `sources/mcl/release-state-v2.0.json`
  - Closed enum: `PREVIEW` or `PUBLISHED`.
  - Contains document code, version, evidence/access cut-off and publication date where applicable.

### Public release family

Use versioned filenames so every withdrawn v1 path can remain permanently blocked:

- `guidelines/mcl/index.html`
- `guidelines/mcl/guideline-v2.0.docx`
- `guidelines/mcl/guideline-v2.0.pdf`
- `guidelines/mcl/quickref-v2.0.docx`
- `guidelines/mcl/quickref-v2.0.pdf`
- `guidelines/mcl/algorithm-v2.0.svg`
- `guidelines/mcl/algorithm-v2.0.excalidraw`
- `guidelines/mcl/release-manifest-v2.0.json`
- `guidelines/mcl/release-record-v2.0.json`

Do not restore the old unversioned DOCX/PDF, three legacy diagram families, PNGs, diagram PDFs or Mermaid file.

### Build and validation code

- `scripts/generate_mcl_v2_release.py`
  - Reads only the canonical source, status matrix and release state.
  - Generates all seven public artefacts in one invocation.
  - Builds SVG and Excalidraw from one diagram model.
  - Sets fixed DOCX core-property dates and canonicalises OOXML ZIP member order, timestamps and permissions.
  - Converts DOCX to PDF with an isolated LibreOffice profile.
- `scripts/validate_mcl_v2_release.py`
  - Manifest enforcement, cross-format semantics, reproducibility, metadata and release-record validation.
- `scripts/validate_mcl_excalidraw.cjs`
  - Official pinned Excalidraw restore/export and browser geometry checks.
- `scripts/validate_mcl_release_state.py`
  - State-aware CI entry point.
  - Runs existing containment validation when no authorised v2 state exists.
  - Runs the v2 gate for preview/published candidates.
  - Always verifies that every v1 direct path remains absent and actively blocked.
- `.github/workflows/preflight.yml`
  - Replace the containment-only MCL job with a named `MCL controlled publication state gate`.
  - Use `macos-15`, Python 3.11, pinned Excalidraw/Playwright dependencies, pinned LibreOffice family and recorded fonts/tool versions.

## Generation and reproducibility contract

1. Validate canonical inputs before writing:
   - required and unique section/unit IDs;
   - closed status-matrix schema;
   - no `[VERIFY]`, draft markers, stale version strings or incomplete references;
   - every quick-reference and algorithm ID resolves to one complete source unit.
2. Generate into an OS temporary directory.
3. Generate DOCX first and PDF only from those generated DOCX files.
4. Generate SVG and Excalidraw from the same in-memory model.
5. Run the complete validator against the temporary family.
6. Move generated bytes together, never by hand-editing a derivative.
7. Build the manifest from final bytes.
8. Validate again in manifest-enforcement mode.
9. Record separately:
   - exact artefact hashes;
   - DOCX byte reproducibility;
   - SVG/Excalidraw byte reproducibility;
   - PDF page-count, normalised-text and rendered-layout reproducibility;
   - final approved PDF hashes.

PDF byte determinism should not be claimed unless demonstrated on the pinned renderer. Final publication approval always binds the exact exported PDF bytes.

## Mandatory cross-format invariants

- Exact document code, version, status, evidence/access cut-off and territorial boundary.
- No v1.x, `DRAFT`, `[VERIFY]`, pending-review or contradictory publication wording anywhere.
- Scan:
  - HTML body and metadata;
  - DOCX body, tables, headers, footers, comments, footnotes, endnotes and properties;
  - PDF page text and metadata;
  - SVG title, description, metadata and visible text;
  - all Excalidraw text and scene metadata.
- Each treatment unit must retain title, population, indication, regimen, dose, schedule/duration, evidence status and access boundary.
- Quick-reference content must be a declared subset of canonical units, not hard-coded alternative prose.
- In PDF, each controlled card title and body anchor must occur on the same page.
- Every status-matrix therapy ID represented in a public format must have the same classification and exact access wording.
- Exact reference titles, identifiers and authority URLs must agree across full HTML/DOCX/PDF.
- SVG and Excalidraw must have the same nodes, labels and permitted edges.
- Independent classifications must not be joined by arrows that imply false treatment sequence.
- Manifest must bind byte count and SHA-256 for all seven public artefacts, plus hashes of canonical inputs and generator/toolchain identity.
- Release record must reconcile exactly to the current manifest and all artefact hashes.

## Accessibility and layout gates

- HTML:
  - one `h1`, logical heading order, landmarks, skip link and unique IDs;
  - labelled navigation and downloads;
  - table captions and header associations;
  - meaningful SVG title/description and non-duplicative accessible labelling;
  - keyboard focus visibility and acceptable colour contrast;
  - no horizontal overflow at 320, 375, 768 and 1440 px;
  - valid fragments/downloads, clean console and no requests for v1 assets;
  - screen and print checks.
- DOCX/PDF:
  - all pages rasterised and inspected;
  - no blank/near-blank pages, clipping, orphan headings, split clinical rows, detached restrictions, footer collisions or font substitution;
  - repeated table headers and correct reading order.
- Diagrams:
  - official Excalidraw restore/export of the exact saved scene;
  - text contained within boxes and SVG bounds;
  - no text overlap;
  - browser inspection at full size and narrow embedded width.

## Fail-closed negative fixtures

The normal CI command must reject each mutation for its intended reason, including:

- altered artefact with a rebound manifest;
- changed treatment classification with internally consistent hashes;
- stale v1 wording in DOCX header/footer/property;
- stale status in PDF metadata;
- modified SVG `<desc>` or Excalidraw text;
- duplicate keys or unknown fields in status matrix/release record;
- title-only or split PDF treatment card;
- overlapping or out-of-bounds diagram text;
- false arrow between independent states;
- weakened robots/status wording;
- restored legacy asset or removed worker denylist entry;
- commented-out CI invocation;
- fabricated pharmacy identity, approval timestamp, reviewed-preview identity or production verification.

## Controlled release sequence

1. **Containment remains authoritative**
   - Production continues serving the withdrawal notice.
   - Existing v1 files remain deleted and all historical paths remain denied with `404` and `no-store`.
2. **Protected preview**
   - Generate `PREVIEW`, with exactly one `noindex, nofollow, noarchive` robots tag and explicit non-publication wording.
   - Freeze commit, tree, binary diff hash, manifest hash and all artefact hashes.
3. **Clinical gate**
   - Owner-approved scope and evidence boundary.
   - Independent review of the exact frozen clinical source, matrix and rendered family.
   - All clinical blockers create a new candidate.
4. **Pharmacy gate**
   - Verify exact indications, doses, schedules, durations, interactions, SmPC boundaries and access wording across every format.
   - Keep verifier identity private.
5. **Technical/publication gate**
   - CI, reproducibility, accessibility, layout, diagram render, metadata and adversarial fixtures pass.
   - Preview downloads match manifest bytes.
6. **Owner decision**
   - Separate approval of reviewed clinical content from authority to produce a public candidate.
7. **Production conversion**
   - Regenerate the whole family as `PUBLISHED`.
   - Require exactly `index, follow`, remove all preview wording and keep the clinical payload digest identical to the reviewed preview.
   - New bytes require a new manifest and explicit owner ratification of that exact manifest.
8. **Merge and deployment**
   - Merge and deployment remain separate authorities.
   - Do not disable v1 path blocks.
9. **Production verification**
   - Verify canonical HTML and every versioned download byte-for-byte.
   - Confirm commit/tree, robots, hub links, sitemap, responsive layout, accessibility, console/network state and continued v1 path denial.
   - Close the release record only after live verification.

## Files changed

- None. Repository inspection was read-only.
- A pre-existing untracked `docs/mcl-v2/` directory was observed and left untouched.
