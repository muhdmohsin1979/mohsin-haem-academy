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
