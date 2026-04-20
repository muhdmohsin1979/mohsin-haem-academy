<!--
  Mohsin Haematology Academy — standard PR body.
  Fill in every section. Tick boxes as you go. Do not merge until preview reviewed.
-->

## Summary
<!-- One or two sentences describing what this PR adds or changes and why. -->

## Type of change
- [ ] New guideline page (one topic, full 8-artefact bundle)
- [ ] Guideline revision (version bump)
- [ ] Journal club post
- [ ] Blog / reflection post
- [ ] Education case
- [ ] Site page edit (about, services, contact, home, etc.)
- [ ] Infrastructure / scripts / workflows
- [ ] Legacy migration / restructure

## What's new
<!-- Bulleted file-by-file summary of what was added or changed. -->

## Evidence (for clinical content)
<!-- List the societies, systematic reviews, RCTs, regulatory sources, and
     recent publications used. Include publication years and PMIDs or DOIs.
     Mark any claim you cannot fully verify as `[unverified — needs source]`.
     Do not delete unverified claims; surface them for review. -->

## Consistency check (for guideline PRs)
<!-- Confirm thresholds and clinical rules are identical across HTML, SVGs,
     PDFs, deck, leaflet, audit workbook, and logic JSON. List any mismatch. -->

## Preview / test plan
- [ ] Cloudflare Pages preview renders the page
- [ ] All figures (SVGs, images) load
- [ ] All download links return 200
- [ ] Mobile layout readable
- [ ] No banned words (Tone Guard passes)
- [ ] No PII or patient identifiers (Preflight passes)
- [ ] External links return 200 (Preflight link check passes)

## Deployment rule
Draft first. Do not merge until the Cloudflare preview has been reviewed and
the author has replied `deploy`, `publish`, `ship it`, `go live`, or `merge`.

## Rollback plan
If the live site breaks after merge, revert the merge commit on `main`.
Cloudflare Pages will auto-redeploy the previous production build.
