# MCL v2.0 controlled work package

## Identity

- Work package: `MHA-MCL-V2-2026-01`
- Product: Mantle Cell Lymphoma guideline v2.0
- Branch: `feat/mcl-v2-20260728`
- Production base: `d4a306846c53a4b790162e1e4127bb87b16250e3`
- Accountable owner: Dr Muhammad Mohsin, Consultant Haematologist
- Started: 28 July 2026
- Current state: evidence and architecture development only

## Purpose

Create a coherent, reproducible and independently reviewed MCL v2.0 release family. It will replace the withdrawn MCL v1.x family only after separate clinical, pharmacy, publication, exact-hash and production approvals.

The current withdrawal page, direct-asset blocks, hub exclusions and sitemap exclusion remain authoritative until the complete v2.0 release is approved and deployed.

## Clinical scope

The controlled source must cover:

1. diagnosis and minimum pathology dataset;
2. staging, MIPI/MIPI-c, morphology, Ki-67 and TP53 risk;
3. observation of appropriate indolent/non-nodal disease;
4. first-line pathways for transplant-suitable and transplant-ineligible adults;
5. maintenance and response assessment;
6. relapsed/refractory sequencing, including covalent-BTKi exposure and progression;
7. CAR-T referral and bridging considerations;
8. high-risk and TP53-mutated disease;
9. supportive care, infection prevention, treatment-specific monitoring and consent;
10. surveillance, MDT documentation and audit standards;
11. emerging evidence, explicitly separated from routine practice;
12. jurisdiction-specific regulatory and access status.

## Mandatory evidence distinctions

Every regimen or technology must record these claims separately:

- clinical evidence and maturity;
- exact GB/UK marketing-authorisation wording;
- final, draft, in-development, paused, suspended or terminated NICE/HTA state;
- NHS England baseline commissioning, CDF managed access or absence of a demonstrated national route;
- Scotland, Wales and Northern Ireland status when stated;
- trial, manufacturer, early-access or local exceptional routes;
- clinical interpretation and applicability limits.

Marketing authorisation must never be presented as NICE recommendation or NHS funding. Draft NICE recommendations must remain explicitly draft. England access must not be generalised to the devolved nations.

## Controlled release family

The intended public artefacts are:

- `guidelines/mcl/index.html`
- `guidelines/mcl/guideline-v2.0.docx`
- `guidelines/mcl/guideline-v2.0.pdf`
- `guidelines/mcl/quickref-v2.0.docx`
- `guidelines/mcl/quickref-v2.0.pdf`
- `guidelines/mcl/algorithm-v2.0.excalidraw`
- `guidelines/mcl/algorithm-v2.0.svg`

The intended control and generation files are:

- `docs/mcl-v2/evidence-ledger.json`
- `docs/mcl-v2/claims-matrix.json`
- `docs/mcl-v2/access-evidence-ledger.json`
- `sources/mcl/source-v2.0.html`
- `sources/mcl/status-matrix-v2.0.json`
- `sources/mcl/release-state-v2.0.json`
- `scripts/generate_mcl_v2_release.py`
- `scripts/validate_mcl_v2_release.py`
- `scripts/validate_mcl_excalidraw.cjs`
- `scripts/validate_mcl_release_state.py`
- `guidelines/mcl/release-manifest-v2.0.json`
- `guidelines/mcl/release-record-v2.0.json`

Internal evidence records remain under `/docs/`; canonical generation inputs remain under `/sources/`. Both prefixes are blocked from public serving.

## Source-of-truth model

- One canonical content source controls clinical wording and section hierarchy.
- One access-status matrix controls licence, HTA, commissioning, jurisdiction and colour/status labels.
- One evidence ledger controls bibliographic identity, evidence extraction and claim support.
- HTML, DOCX, PDF, quick reference and algorithm text are generated or validated against those sources.
- Editable diagrams carry the document code, version, status and governance footer and must reproduce their public SVG derivatives through the pinned renderer.
- Versioned v2.0 download paths are used so the withdrawn v1.x paths remain permanently blocked.

No public format may be edited independently to change clinical or access wording.

## Required fail-closed invariants

The release gate must reject:

- cross-format version, document-code, status or date differences;
- unresolved `[VERIFY]`, draft placeholders or expired publication-date wording;
- a licence claim presented as funding;
- a draft NICE recommendation presented as final;
- England access presented as UK-wide;
- inconsistent therapy status, colour, wording or sequencing across formats;
- missing doses, schedules, durations, eligibility limits or monitoring attached to a recommendation;
- unsupported clinical claims or citations absent from the evidence ledger;
- stale or contradictory DOCX headers, footers, properties or PDF metadata;
- split controlled rows, clipped diagrams, blank TOC pages or orphaned table fragments;
- Excalidraw/SVG text or structural divergence;
- altered artefacts paired with a re-written manifest;
- incomplete clinical, pharmacy, owner or production state transitions;
- restoration of MCL hub, sitemap or download exposure before publication authority is complete.

## Governance sequence

1. Freeze review question, jurisdictions, cut-off and inclusion rules.
2. Complete live official-source regulatory and access audit.
3. Complete verified PubMed/Crossref literature ledger and claims matrix.
4. Obtain owner agreement on clinical scope and proposed pathways.
5. Draft canonical content and status matrix.
6. Generate all public formats from the controlled sources.
7. Run clinical-unit, cross-format, layout, accessibility and negative-fixture validation.
8. Obtain independent clinical review.
9. Obtain human pharmacy verification, with verifier identity retained privately.
10. Freeze the exact staged tree, manifest and artefact hashes for independent publication review.
11. Deploy an immutable preview and verify exact bytes, desktop, mobile, print, downloads and console output.
12. Obtain owner approval of the exact preview hashes.
13. Obtain a separate owner decision for merge and production deployment.
14. Verify production commit, provider build, canonical bytes, blocked private paths and live behaviour.
15. Complete the release record without overclaiming any pending state.

## Current evidence baseline

The earlier 27 July 2026 audits are leads, not final v2.0 evidence. They identified high-priority areas requiring live re-verification, including:

- mature TRIANGLE evidence and its exact licensed regimen;
- ENRICH and the BR comparator interaction;
- peer-reviewed ECHO evidence and current appraisal state;
- TP53/high-risk and MRD-directed strategies;
- first-relapse covalent BTKi commissioning and intolerance-transfer limits;
- post-covalent-BTKi sequencing without unsupported CAR-T-versus-pirtobrutinib precedence;
- brexucabtagene autoleucel evidence, TA677 review and live CDF criteria;
- lisocabtagene maraleucel, pirtobrutinib, glofitamab and other non-routine pathways;
- VR-CAP/TA370, lenalidomide and ibrutinib–venetoclax status;
- devolved-nation access, which was not completed in the prior England-focused audit.

No statement above is publication wording. Each item must be reconciled against the new live evidence and access ledgers.

## Owner direction recorded 28 July 2026

The accountable owner directed that v2.0 should provide an actionable, evidence-based specialist pathway and that no clinical, regimen, dose, access or source statement may be invented or fabricated. The controlled source may include a treatment or dosing statement only when it is supported by checked primary evidence or an exact current official source. Missing, unresolved or non-transferable detail must be qualified, delegated to the current SmPC/local SACT protocol, or omitted. This direction authorises further drafting; it is not approval of any candidate artefact or publication authority.

## Open owner decisions before clinical drafting is frozen

- Whether the public title should say “UK practice-oriented” or explicitly use an England access framework with separate devolved-nation notes.
- Whether the first-line algorithm should lead with evidence architecture or current commissioned access.
- Which local SACT pathways and exceptional-access processes may be stated beyond national sources.
- Whether v2.0 should include a short patient-facing section or remain specialist-only.
- Whether the quick reference should be two or three pages.

## Explicit exclusions

- No restoration of MCL as a published resource during evidence development.
- No reuse of the withdrawn v1.x DOCX, PDF or diagrams as v2.0 artefacts.
- No assumption that historical v1.x wording remains clinically valid.
- No substantive change to CLL, Myeloma or other guideline products in this work package.
- No merge, preview publication or deployment without the corresponding later gate.
