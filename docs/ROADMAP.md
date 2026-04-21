# Mohsin Haematology Academy — Roadmap 2026–2027

**Maintainer:** Dr Muhammad Mohsin, Consultant Haematologist
**Live site:** https://mohsinhaemacademy.com
**Repo:** https://github.com/muhdmohsin1979/mohsin-haem-academy
**Current production tag:** see `git tag -l | tail -1`
**This file is versioned.** Every PR that finishes a roadmap item ticks the relevant box here.

---

## Vision

Take the Academy from a live static site to a citable UK clinical education resource that doctors open on a ward round and find useful within thirty seconds.

---

## If you focus on only four things

These four actions drive 80% of the platform's long-term impact.

1. **Build 3–5 high-quality clinical tools**, each anchored to NICE / BSH / EHA / ELN. Standardised structure on every tool.
2. **Make credentials visible immediately.** Name and role in the homepage hero — not buried.
3. **Build an audience before it is needed.** Email capture from day one. The journal club is already the product.
4. **Target real clinical search queries.** Clinicians search during decision-making. Own those queries before anyone else does.

---

## Cadence and success metric

- **One new clinical tool every 6 weeks.** Sustainable for a full-time consultant with a family.
- **Success metric by 1 April 2027: 10 clinical tools live at v1.0 or higher.** One number, fully under Dr Mohsin's control. Email subscribers and search traffic follow from shipped content and are tracked but not a gate.

Topic schedule (locked; can be reordered on request):

| Month | Topic | Primary guideline |
|---|---|---|
| May 2026 | Neutropenic sepsis | NICE NG51 |
| Jun 2026 | Iron deficiency anaemia (adults) | BSH 2021, NICE NG8 |
| Aug 2026 | DOAC emergency reversal | BSH 2016 reversal update |
| Sep 2026 | Thrombocytopenia differential | BSH 2021, ASH 2019 |
| Nov 2026 | Myeloma workup & risk stratification | IMWG 2024, NICE NG35 |
| Dec 2026 | AML induction fitness assessment | ELN 2022, BSH 2024 |

Existing live tools (4): Anaemia in pregnancy, CLL, ITP, VTE-cancer.
Target state by 1 April 2027: 4 + 6 = **10 tools live at v1.0+.**

---

## Phase 0 — Infrastructure ✅ complete (April 2026)

Recorded here so future readers know what is already in place.

- [x] GitHub-hosted repo at `muhdmohsin1979/mohsin-haem-academy`
- [x] Cloudflare Pages project `mohsin-haem-academy` serves `mohsinhaemacademy.com` via CNAME
- [x] Only one Worker in the account (`haemcalc`); no duplicate auto-build PRs
- [x] Draft-first publishing contract (`.github/PULL_REQUEST_TEMPLATE.md`)
- [x] Tone guard in diff mode (`scripts/tone_guard.py`) — blocks banned words on new lines only
- [x] Preflight PII sweep + DOI/PMID/PMCID suppression + 14/14 self-test in CI (`scripts/preflight.py`)
- [x] Internal link checker (file-based)
- [x] External link checker in diff mode (URLs in new lines only)
- [x] Pre-commit hook (`scripts/hooks/pre-commit`) runs the same checks locally
- [x] Cloudflare preview URL on every PR
- [x] Production auto-tagging on every merge to `main` — format `v<YYYY.MM.DD>-<short-sha>`
- [x] Long-term folder layout: `/guidelines/<topic>/`, `/journal-club/<slug>/`, `/blog/<slug>/`, `/education/<slug>/`
- [x] `_redirects` preserves 27 legacy URLs with 301s
- [x] `.env` holds Cloudflare, GitHub, Zotero, and NCBI keys (`.gitignore`'d)
- [x] Workspace cheatsheet (`WEBSITE_COMMANDS.md`) documents invocation phrases

---

## Phase 1 — Foundation & Quick Wins

**Objective:** Make the platform clinically credible and begin building an audience from day one.

- [ ] Credentials in the homepage hero — one sentence: *"Built by Dr Muhammad Mohsin, Consultant Haematologist."*
- [ ] Email capture on `index.html` and `contact.html` — free-tier provider (proposed: Buttondown or Mailchimp; user picks).
- [ ] Tighten the `guidelines.html` hub page into a clean tool index with category filters (Anaemia / Haemostasis / Malignancy / Transfusion).
- [ ] Trim the top-navigation to four sections: **Tools · Guidelines · Education · About**. Move Contact, Governance, HaemCalc, Calculator into the footer.
- [x] Governance page — `governance.html` exists; confirm scope, limitations, no patient data storage, medico-legal note.
- [ ] Tighten HaemCalc connection — embed a small preview on `index.html`, make the "Open HaemCalc" call-to-action prominent, two clicks or fewer from the homepage to a live calculator.

**Phase 1 done when:** homepage clearly identifies Dr Mohsin, email signup is live, nav is four items, governance page is linked from the footer.

---

## Phase 2 — High-Impact Clinical Tools

**Objective:** Drive adoption through real clinical utility.

**Non-negotiable structure for every tool page** (see `docs/templates/tool-page-template.html`):

> **Input → Output → Interpretation → Suggested Action → Guideline Basis → Last Updated (version + date)**

Each tool must include:

- Stepwise logic with clear thresholds
- Red flags visible, not buried
- References to NICE / BSH / EHA / ELN / RCOG as applicable
- Versioning block: `v1.0 | Updated YYYY-MM-DD`
- Disclaimer: *supports, not replaces, clinical judgement*

**Topic schedule:** see [Cadence](#cadence-and-success-metric). Checklist per topic, ticked as each ships:

- [ ] Neutropenic sepsis — `/guidelines/neutropenic-sepsis/`
- [ ] Iron deficiency anaemia, adults — `/guidelines/iron-deficiency-anaemia/`
- [ ] DOAC emergency reversal — `/guidelines/doac-reversal/`
- [ ] Thrombocytopenia differential — `/guidelines/thrombocytopenia-differential/`
- [ ] Myeloma workup — `/guidelines/myeloma-workup/`
- [ ] AML induction fitness — `/guidelines/aml-induction/`

**Phase 2 done when:** 10 tools live at v1.0+ (existing 4 + new 6). That is also the overall success metric.

---

## Phase 3 — SEO & Discoverability (runs in parallel with Phase 2)

**Objective:** Capture real clinical search traffic so the Academy becomes findable at the moment of decision.

- [ ] Each tool page targets one search intent. Draft target-query table inside each PR body.
- [ ] Unique keyword-led `<title>` on every page
- [ ] `<meta name="description">` on every page
- [ ] Internal linking between related tools (e.g. Neutropenic sepsis ↔ Neutropenia management)
- [ ] Submit `sitemap.xml` to Google Search Console (account: Dr Mohsin)
- [ ] Monitor indexing and search queries monthly; log observations in `/docs/analytics/YYYY-MM.md`
- [ ] Publish journal club posts at `/journal-club/<slug>/` — target: 4–6 posts by end of 2026

**Phase 3 done when:** Search Console shows ≥ 50 indexed pages and ≥ 10 organic clicks per week sustained for a month.

---

## Phase 4 — Authority & Professional Presence

**Objective:** Make the platform citable and professionally visible.

- [ ] Reference section at the bottom of every tool (NICE guideline number + date, BSH standard, ELN, ASCO as relevant)
- [ ] "How to cite this page" block on every tool (APA + Vancouver + BibTeX)
- [ ] LinkedIn professional track — post journal club and guideline updates, drive return traffic
- [ ] "Citable" landing page at `/about.html` showing ORCID, affiliations, teaching roles

**Phase 4 done when:** at least one external clinician cites a Academy page in presentation / audit / teaching and it can be tracked (via email, screenshot, or citation-audit PR).

---

## Phase 5 — Engagement & Repeat Users

**Objective:** Convert first-time visitors into a returning user base.

- [ ] Monthly or bi-monthly newsletter — pick cadence once Phase 1 email list is live
- [ ] Newsletter content mix: clinical pearls, guideline updates, journal club highlights, new tool announcements
- [ ] "Suggest an improvement" email link on every tool page (mailto: link is fine; no form backend needed)
- [ ] Optional per-tool rating widget (useful / not useful) — only if backend is trivial

**Phase 5 done when:** 200 email subscribers and one newsletter issue published per month for three consecutive months.

---

## Phase 6 — NHS Integration & Academic Output

**Objective:** Transition from a personal site to a recognised clinical resource.

- [ ] Share Academy with trainees, MDT colleagues, department
- [ ] Use tools in teaching and ward rounds; gather informal feedback
- [ ] Short service evaluation: measure point-of-care time savings, decision confidence, error reduction
- [ ] Document adoption as evidence for academic output
- [ ] Publish HaemCalc manuscript (already in progress)
- [ ] Submit poster/abstract to BSH Annual Meeting or SOHO
- [ ] Short paper in BMJ Open Quality or BMJ Health & Care Informatics
- [ ] Letter or correspondence in Clinical Medicine or The Haematologist

**Phase 6 done when:** one peer-reviewed publication accepts a paper, letter, or correspondence referencing the Academy.

---

## Phase 7 — Advanced Evolution (only if Phase 6 confirms demand)

Do not build ahead of evidence.

- [ ] Branching-logic calculators for complex decision trees
- [ ] Mobile-first optimisation and progressive web app
- [ ] Structured haematology curriculum / learning pathways
- [ ] NHS department or deanery collaboration
- [ ] App version — only if web adoption justifies it

---

## How this document evolves

1. Every PR that ships a roadmap item ticks the box here in the same PR.
2. Timeline updates (topic reordering, cadence change) land as a standalone `docs/ROADMAP.md` PR.
3. A new snapshot (`docs/ROADMAP-v2.md`) is created when a major replan happens (e.g. at the end of Phase 2).
4. The PDF that informed this document (`MHA strategic road map.pdf`) stays in the workspace as the historical source; contributor Muhammad Moaaz is credited below.

## Credits

- **Author:** Dr Muhammad Mohsin, Consultant Haematologist
- **Contributor (original strategic roadmap, April 2026):** Muhammad Moaaz
- **Publishing pipeline (April 2026):** drafted with Claude via Cowork mode

## Banned words in published content

This roadmap follows the same tone-guard rules as every other page in the repo. The authoritative list lives in `scripts/tone_guard.py`. Do not copy or paraphrase roadmap language that has been softened for that list into clinical tool content without checking against the guard first.
