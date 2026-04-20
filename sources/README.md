# /sources — reference library

Bibliographic exports and source lists used across guideline and journal-club
posts. Keep one file per topic or one consolidated Zotero export.

## Expected files
- `zotero-library.bib` — monthly export from Dr Mohsin's Zotero library.
- `<topic>.bib` — per-topic exports where useful (e.g. `vte-cancer.bib`).
- `guideline-links.md` — curated list of BSH, EHA, ASH, NICE, and ISTH
  guideline URLs with access dates.

## How to update the Zotero export
1. Open Zotero on desktop.
2. File → Export Library → Format: BibTeX → Character encoding: UTF-8.
3. Save as `zotero-library.bib` in this folder.
4. Commit on a `chore(sources)/zotero-refresh-<yyyymmdd>` branch via PR.

## Do not store
- Full-text PDFs of paywalled papers (copyright).
- Patient data of any kind.
- API keys or tokens.
