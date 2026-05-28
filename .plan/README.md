# MHA and HaemCalc Maintenance

Companion README for the 12-month website improvement plan (Track A maintenance and Track B content). This is the maintenance-project README, separate from the repo-root READMEs of mohsin-haem-academy and HaemCalc.

The locked plan lives in `MHA_HaemCalc_12-Month_Plan.docx`. That document is not edited mid-year. These companion files hold the live working state.

## Current Month

Month 1: Audit and tidy (observation only, fix nothing). 17 May to 16 Jun 2026.

## Last Session

Date: 2026-05-28
Month: 1
Track A focus: Audit and tidy (observation only)
What was done:
- Created the six companion files under /.plan/ via PR #56 (scaffold/plan-files).
- Logged seven Year 2 candidate entries in Year2-Ideas.md.
- Added two pending decisions to Decisions.md (testing framework, analytics platform).
- Rejected the _routes.json approach after checking Cloudflare docs; used a dot-prefixed /.plan/ folder, which Cloudflare Pages does not serve.
- Cleared two tone-guard banned-word hits in Year2-Ideas.md before all checks passed (reworded, meaning unchanged).
Outstanding items:
- PR #56 awaiting human review and merge. No approve/merge by automated agents.
- Note: tone guard scans all added lines, including /.plan/ companion files, so the avoid-list applies there too.
Next step:
- Merge PR #56 after review, then begin Week 2 of Month 1 (HaemCalc Pro calculator inventory plus reversal page list).
