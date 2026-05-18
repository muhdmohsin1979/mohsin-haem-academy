# MHA-MYELOMA Guideline — Diff Note v0.4 → v0.4.1 GOVERNANCE POLISH

**Document code:** MHA-MYELOMA-2026-v0.4.1-GOVERNANCE-POLISH
**Date:** May 2026
**Author:** Dr Muhammad Mohsin, Consultant Haematologist
**Assist:** Claude
**Review input:** ChatGPT governance brief (May 2026)
**Status:** DRAFT — proposal only, no deployment

---

## Summary

v0.4.1 is a **minimal safety-polish revision** of v0.4-GOVERNANCE-REVIEW. The clinical structure, SOP scaffolding v2 framework, BSH/UKMS/IMWG content, MHA visual style, references and Section 1A NICE Horizon Scanning are all preserved. Only the six amendments listed in the governance brief have been applied. **No new clinical recommendations have been added.** No clinical statements have been removed. Wording around pathway placement and indication has been tightened where v0.4 was either over-stated or imprecise.

## The six amendments applied

### 1. Belantamab + Pd placement (TA1133)

**v0.4 said** that TA1133 (belantamab + pomalidomide + dexamethasone, DREAMM-8) was a "recently appraised relapse option" and listed it in the R/R algorithm and Quick-Ref under "Penta-refractory or beyond — late-line options". This risked the false implication that it was a generic penta-refractory option.

**v0.4.1 says** that belantamab + Pd is an **option after one prior lenalidomide-containing line if lenalidomide is not tolerated or disease is lenalidomide-refractory**; it is not a generic penta-refractory option; verify ocular monitoring service, commercial arrangement, Blueteq form and local pathway before prescribing.

Applied to:
- `myeloma.html` Section 11 — belantamab regimen block now leads with an "Indication" definition list row using the new wording, with the dose row reordered after it; mandatory pre-dose ophthalmology assessment retained with explicit "visual acuity and keratopathy grading per protocol" wording.
- `myeloma.html` Section 1 NICE TA listing — TA1133 bullet now reads "Option after one prior lenalidomide-containing line if lenalidomide is not tolerated or disease is lenalidomide-refractory; not a generic penta-refractory option."
- `myeloma.html` Section 1A horizon table — belantamab row Setting changed to "Previously treated myeloma after 1 prior lenalidomide-containing line if Len-intolerant or Len-refractory"; guideline wording rewritten accordingly.
- Full guideline DOCX — same changes applied in build script (Section 1 bullet, Section 1A table row, Section 11 belantamab block with new Indication field, Section 14 NICE TA references list).
- Quick-Ref DOCX — belantamab moved out of the "Penta-refractory or beyond" row; new row "1st relapse (post-Len) — Len-intolerant / Len-refractory" added with belantamab + Pd named first and the cautious wording; horizon-scanning prose block reworded to use the safer indication.
- R/R algorithm SVG and JPEG — belantamab moved out of the "Penta-refractory or beyond" box and placed in a renamed "Late-line and specialist-route options" box, with explicit post-Len indication line and TA1133 chip; selinexor and venetoclax retained in the same box. Ocular monitoring warning preserved.

### 2. D-VRd placement in NDMM algorithm

**v0.4 said** that D-VRd (PERSEUS-based, GID-TA10726 / ID3843) was an in-development NICE option for **transplant-eligible** NDMM, and placed it under "Newly diagnosed, transplant-eligible" in Section 1, with a regimen block in the TE-NDMM section of Section 8, and in the TE-NDMM area of the sidebar NICE Commissioning panel. The NDMM algorithm placed D-VRd as "TA11254 in development" in the TE pathway.

**This was incorrect.** The cited NICE in-development entry GID-TA10726 / ID3843 relates to **untreated myeloma when stem cell transplant is unsuitable** (transplant-ineligible NDMM), not transplant-eligible disease.

**v0.4.1 says** that D-VRd is **horizon/evidence only**; the cited NICE GID-TA10726 / ID3843 currently relates to transplant-unsuitable NDMM; verify live NICE indication before pathway placement; do not present D-VRd as a transplant-eligible NICE in-development option.

Applied to:
- `myeloma.html` Section 1 — D-VRd removed from the "Newly diagnosed, transplant-eligible" bullet list; added to the "Newly diagnosed, transplant-ineligible" bullet list with the explicit "horizon / evidence only" wording and pathway-placement warning.
- `myeloma.html` Section 8 prose — rewritten to clarify D-VRd is for transplant-unsuitable; PERSEUS trial population (transplant-eligible) noted separately from the appraisal indication.
- `myeloma.html` Section 8 regimen block — D-VRd block removed from the TE-NDMM area entirely; new D-VRd block placed after Isa-VRd in the TI-NDMM area, with a "Pathway placement" field as the first definition-list row stating "Horizon/evidence only. Cited NICE GID-TA10726 / ID3843 currently relates to untreated myeloma when stem cell transplant is unsuitable. Verify live NICE indication before pathway placement. Not commissioned for the transplant-eligible setting."
- `myeloma.html` sidebar — NICE Commissioning panel moved D-VRd from "NDMM transplant-eligible" to "In development / awaiting" with the wording "GID-TA10726 / ID3843 — D-VRd (transplant-unsuitable, in dev)".
- `myeloma.html` quick decision summary — TE-NDMM line clarified that D-VRd is in development for transplant-unsuitable NDMM and is not a commissioned TE-NDMM option.
- Full guideline DOCX — all Section 1, Section 1A, Section 8 changes applied in build script. D-VRd regimen block reordered to TI-NDMM area in Section 8 with Pathway placement field.
- Quick-Ref DOCX — NDMM table "Horizon scanning" row renamed to "Horizon scanning (transplant-unsuitable)"; wording updated to "D-VRd (PERSEUS): horizon/evidence only; NICE GID-TA10726 / ID3843 currently relates to transplant-unsuitable NDMM. Verify live NICE indication before pathway placement." Horizon-scanning prose block reworded with explicit "horizon / evidence only" framing and "do not place as a transplant-eligible NICE in-development option" statement.
- NDMM algorithm SVG and JPEG — D-VRd in the TE pathway box relabelled from "TA11254 in development" to "horizon/evidence only; NICE GID-TA10726/ID3843 (transplant-unsuitable)".

### 3. Star symbol wording

**v0.4 said** "★ Currently preferred where eligible." This phrasing implied a stronger MHA preferential recommendation than is justified by an educational decision-support document.

**v0.4.1 says** "★ = recently appraised / commonly pathway-relevant where NICE criteria and local access are met."

Applied to:
- `myeloma.html` sidebar NICE Commissioning panel footnote.
- Quick-Ref DOCX NICE TA list caption (and full guideline DOCX where the same convention appears).

### 4. TA763 wording

**v0.4 said** "TA763 — Daratumumab + bortezomib + thalidomide + dexamethasone (D-VTd) for induction and consolidation (Feb 2022)."

**v0.4.1 says** "TA763 — D-VTd induction/consolidation for newly diagnosed transplant-eligible myeloma, within NICE criteria (February 2022)."

Applied to:
- `myeloma.html` Section 1 TE-NDMM bullet list.
- `myeloma.html` sidebar NICE Commissioning panel.
- Full guideline DOCX Section 1 bullet list, Section 14 NICE TA references list.
- Quick-Ref DOCX NDMM table and NICE TA list.

### 5. Algorithm safety footer

Both algorithm SVG files have a new educational footer stripe added: **"Educational pathway summary only. NICE/Blueteq/local formulary and SmPC verification required before treatment."** The SVG viewBox height was extended (1500 → 1520) and the background rect height extended to match. JPEGs were regenerated from the updated SVGs at 1600 × 1900 px.

The R/R algorithm SVG title bar string was also bumped to v0.4.1; an additional in-pathway footer line in the existing footer box was updated from "MHA-MYELOMA-2026-v0.3 (draft)" to "MHA-MYELOMA-2026-v0.4.1-GOVERNANCE-POLISH (draft)". The Quick-Ref already carried a per-page safety footer; that wording is consistent with the new algorithm footer and was not changed in v0.4.1.

### 6. Governance status preserved

The banner, title page, document identity table, footer band, sidebar footnotes and Quick-Ref title bar still display **PROPOSAL ONLY — DRAFT — GOVERNANCE REVIEW** alongside the v0.4.1-GOVERNANCE-POLISH version string, with explicit wording: "Not for publication, deployment or clinical use without consultant and pharmacy sign-off." The draft label was not removed.

## Files in this v0.4.1 package

| File | Status vs v0.4 |
|---|---|
| `myeloma.html` | Revised. All six amendments applied. SOP scaffolding v2 preserved. Section 1A horizon scanning preserved. 16-item publication checklist preserved. |
| `MHA-MYELOMA-2026-v0.4.1-GOVERNANCE-POLISH-guideline.docx` / `.pdf` | New (44 pages A4, was 43 in v0.4). |
| `MHA-MYELOMA-2026-v0.4.1-GOVERNANCE-POLISH-quickref.docx` / `.pdf` | New (4 pages A4). Per-page safety footer retained. |
| `myeloma-ndmm-algorithm.svg` / `.jpeg` | Updated: educational footer stripe added; D-VRd label corrected; viewBox extended to 1520. JPEG re-rendered at 1600×1900 px. |
| `myeloma-rr-algorithm.svg` / `.jpeg` | Updated: educational footer stripe added; belantamab moved out of penta-refractory box into renamed late-line box with post-Len indication line; viewBox extended to 1520. JPEG re-rendered. |
| `diff-note-v0.4-to-v0.4.1.md` | This document. |

## Confirmation: no new clinical recommendations introduced

v0.4.1 changes are scope-limited to:
- Indication-precision wording (belantamab + Pd post-Len placement, D-VRd transplant-unsuitable indication).
- Pathway-placement corrections (D-VRd moved out of TE area; belantamab moved out of penta-refractory area).
- Editorial wording (star symbol explanation; TA763 reworded; algorithm safety footer).

No drug, regimen, dosing schedule, trial-evidence statement, NICE TA number, NICE identifier or recommendation strength has been added or removed in v0.4.1.

## Items still requiring consultant / pharmacy verification

The v0.4 verification list remains current in v0.4.1. In particular:

1. **GID-TA10726 / ID3843 (D-VRd)** — live NICE status check; the cited NICE expected publication date of 13 May 2026 has passed.
2. **TA1098 (Isa-VRd, September 2025)** — confirm final recommendation wording, restrictions and commercial arrangement; confirm Blueteq form and local formulary access.
3. **TA1023 (elranatamab, December 2024, managed access)** — confirm current managed-access evidence collection criteria and Blueteq form.
4. **TA1114 (talquetamab, December 2025)** — confirm restriction wording, approved-centre pathway and Blueteq form.
5. **TA1133 (belantamab + Pd, February 2026)** — confirm restriction wording, exact line-of-therapy criteria, ocular monitoring requirements, and ophthalmology service pathway.
6. **GID-TA10905 / ID4012 (cilta-cel earlier line)** — confirm in-development status and scheduled appraisal start date.
7. **GID-TA11846 / ID6639 (isatuximab maintenance)** — confirm "awaiting development" status.
8. **GID-TA10843 / ID1517 (ixazomib maintenance)** — confirm "discontinued February 2026" status.
9. Older TAs that have not been re-checked: TA129, TA228, TA311, TA380, TA427, TA510, TA586, TA587, TA657, TA680, TA695, TA763, TA869 (terminated), TA889 (terminated), TA970.
10. Pharmacy review of every dose block — current SmPC, renal/hepatic dose adjustment, frailty modification, local e-prescribing protocol, antiviral/antibacterial/antifungal prophylaxis, IVIg policy, VTE thromboprophylaxis policy with IMiDs.
11. Approved-centre pathway confirmation for bispecifics and CAR-T.
12. Ophthalmology service pathway confirmed for belantamab + Pd (TA1133).

## Broken links report

No broken links found. The HTML sidebar download links now point to v0.4.1 PDF filenames. The HTML sidebar visual-diagram links point to the JPEG and SVG assets in the same directory, both regenerated for v0.4.1. The Section 1A anchor (`#horizon`) and the anchor nav and sidebar On-This-Page list are unchanged. No other anchor changes.

## Suggested PR title

```
Finalise myeloma guideline v0.4.1 governance-polish draft
```

## Suggested PR description

```
Applies final safety refinements to the MHA myeloma guideline before
deployment preparation. Tightens belantamab + Pd pathway placement,
corrects D-VRd horizon-scanning placement, softens NICE TA star wording,
clarifies TA763 wording, and adds algorithm safety footers. Retains
proposal-only governance-review status pending consultant and pharmacy
sign-off.

Key changes from v0.4:
- Belantamab + Pd (TA1133): now explicitly an option after 1 prior
  lenalidomide-containing line if Len-intolerant or Len-refractory.
  Removed from penta-refractory positioning; mandatory pre-dose
  ophthalmology assessment retained.
- D-VRd (GID-TA10726 / ID3843): moved out of TE-NDMM area; labelled
  horizon/evidence only; cited NICE in-development entry currently
  relates to transplant-unsuitable NDMM. Verify live NICE indication
  before pathway placement.
- Star symbol wording softened: "★ = recently appraised / commonly
  pathway-relevant where NICE criteria and local access are met."
- TA763 reworded: "D-VTd induction/consolidation for newly diagnosed
  transplant-eligible myeloma, within NICE criteria."
- Algorithm safety footer added to both NDMM and R/R SVGs and JPEGs:
  "Educational pathway summary only. NICE/Blueteq/local formulary
  and SmPC verification required before treatment."
- Banner retains PROPOSAL ONLY — DRAFT — GOVERNANCE REVIEW.

No new clinical recommendations added. Not for publication until
consultant and pharmacy verification are complete.
```

---

*v0.4.1 is a draft governance-polish revision only. No deployment, no preview branch, no PR raised by Claude. Awaiting your sign-off.*
