# /docs — project documentation

Longer-form documentation that lives in-repo so it ships with the site.

## Contents

| File | Purpose |
|---|---|
| `ROADMAP.md` | Living 2026–2027 roadmap. Ticked off as items land. |
| `templates/tool-page-template.html` | Skeleton for every new `/guidelines/<topic>/index.html` — enforces the Input → Output → Interpretation → Suggested Action → Guideline Basis → Last Updated structure. |

## How to update the roadmap

1. If you are finishing a listed item, tick the box in `ROADMAP.md` as part of the same PR that delivers the work.
2. If you are changing dates, priorities, or phase definitions, open a standalone PR titled `docs(roadmap): ...` so the timeline change is reviewable in isolation.
3. When a phase completes, add a short `docs/roadmap-retro-phase-N.md` note — one page — recording what shipped, what slipped, what surprised you. Future-you will thank you.

## How to start a new tool page

```bash
# replace <slug> with kebab-case topic name
mkdir -p guidelines/<slug>
cp docs/templates/tool-page-template.html guidelines/<slug>/index.html
# edit every <!-- FILL IN --> block, then open a draft PR
```

The preflight CI check + the pre-commit hook enforce tone-guard, PII, and
internal-link rules on the new file automatically.

## Template v2 fields (April 2026)

Every new tool page must fill in the following before it is considered v1.0:

- **Title** — the clinical topic.
- **Lede** — one sentence stating the decision the tool supports.
- **Tags** — any that apply: Emergency, MDT, NICE, BSH, Audit, Prescribing,
  Interpretation. Used by the Tools hub for filtering.
- **Scope** — what is in and out of scope for this tool.
- **Intended users** — e.g. UK consultant haematologists, SHOs on call,
  CNS teams. State explicitly that the tool is not patient-facing when
  that is the case.
- **Evidence base** — named primary sources (NICE, BSH, ELN, ASH, iwCLL,
  IMWG, RCPath, etc.) with year.
- **Version + last reviewed** — `v1.0 · YYYY-MM-DD`.
- **Disclaimer block** — top-of-page, visible without scrolling. Prescribing
  tools must state: local policy, renal function, weight, bleeding risk,
  interactions, pregnancy status, SmPC must be checked before
  administration.
- **Six required sections**: Input → Output → Interpretation → Suggested
  Action (with red-flag list) → Guideline Basis → How to cite.
- **Safety language** — use "suggests", "is compatible with", "consider",
  "requires clinical correlation". Do not write definitive diagnoses.

## Safety language rules

The template enforces (and the tone guard independently checks) that
clinical tools read as decision support, not directive. Prefer:

| Avoid | Use instead |
|---|---|
| "indicates", "proves", "confirms" | "suggests" |
| "diagnoses" | "is compatible with" |
| "start", "give", "prescribe" | "consider" |
| absolute statements | "requires clinical correlation" or "requires senior review" |

Emergency tools must carry a visible *"escalate to senior haematology
immediately"* line in the red-flags block, not buried in prose.
