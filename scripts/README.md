# /scripts — publishing guardrails

Two Python scripts run on every pull request before anything is allowed to
merge into `main`. Together they form the preflight check referenced in
`.github/workflows/preflight.yml`.

## `tone_guard.py`
Blocks banned words in new or changed markdown and HTML files. The word list
is defined inside the script and mirrors Dr Mohsin's personal writing
preferences. HTML tags, `<script>` blocks, and `<style>` blocks are stripped
before scanning so CSS class names and tag attributes do not produce false
hits.

Exit 0 on pass, exit 1 on any hit (CI fails, merge blocked).

```bash
python scripts/tone_guard.py --files-from changed.txt
python scripts/tone_guard.py content/guidelines/vte/index.html
```

## `preflight.py`
Runs two checks on new or changed markdown and HTML files:

1. PII sweep — NHS numbers, hospital numbers, dates of birth, and common
   patient-name markers. Any hit fails CI.
2. External link check — HEAD request (fallback to GET) on every http/https
   URL. Allows 200, 301, 302, 303, 307, 308. Fails on 4xx, 5xx, timeouts.

Exit 0 on pass, exit 1 on any PII hit or broken link.

```bash
python scripts/preflight.py --files-from changed.txt
python scripts/preflight.py --skip-links path/to/file.html   # PII only, no network
```

## Local use before pushing
```bash
# from the repo root
git diff --name-only --diff-filter=AM origin/main | grep -Ei '\.(md|html)$' > changed.txt
python scripts/tone_guard.py --files-from changed.txt
python scripts/preflight.py --files-from changed.txt
```

## Updating the banned-words list
Edit `BANNED_WORDS` at the top of `tone_guard.py`. Keep entries
lowercase — matching is case-insensitive. Open a PR; do not edit on `main`.
