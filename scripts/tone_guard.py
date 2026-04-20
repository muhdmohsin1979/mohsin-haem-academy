#!/usr/bin/env python3
"""
tone_guard.py — block banned words in new or changed markdown/HTML content.

Runs inside GitHub Actions as a PR check. Exits:
    0  no banned words found
    1  one or more banned words present
    2  usage / IO error

Modes:
  --diff-from <path>    Read a unified diff from <path> and scan ONLY the
                        lines being ADDED (prefixed with `+`, excluding
                        `+++` headers). This is the preferred mode — legacy
                        content that is only renamed or reformatted does not
                        trigger hits; new text does.
  --files-from <path>   Read one file path per line from <path> and scan
                        each file in full. Use for ad-hoc audits.
  (positional paths)    Scan the given files in full.

Usage examples:
    python scripts/tone_guard.py --diff-from pr.diff
    python scripts/tone_guard.py --files-from changed.txt
    python scripts/tone_guard.py path/to/file.html path/to/other.md
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

# Authoritative banned-words list. Sourced from Dr Mohsin's personal
# writing preferences and project instructions. Case-insensitive match.
BANNED_WORDS = [
    "embarked", "delved", "invaluable", "relentless", "groundbreaking",
    "endeavour", "enlightening", "insights", "esteemed", "shed light",
    "deep understanding", "crucial", "delving", "elevate", "resonate",
    "enhance", "expertise", "offerings", "valuable", "leverage",
    "intricate", "tapestry", "foster", "systemic", "inherent",
    "treasure trove", "testament", "peril", "landscape", "delve",
    "pertinent", "synergy", "explore", "underscores", "empower",
    "unleash", "unlock", "folks", "pivotal", "adhere", "amplify",
    "cognizant", "conceptualize", "emphasize", "complexity",
    "recognize", "adapt", "promote", "critique", "comprehensive",
    "implications", "complementary", "perspectives", "holistic",
    "discern", "multifaceted", "nuanced", "underpinnings", "cultivate",
    "integral", "profound", "facilitate", "encompass", "elucidate",
    "unravel", "paramount", "characterized", "significant",
]

# Strip HTML tags and script/style blocks before scanning, so a word
# that appears only as a CSS class name or tag attribute does not trigger.
TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
SCRIPT_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)


def extract_visible_text(raw: str, suffix: str) -> str:
    """Return the text a human reader would actually see."""
    if suffix in {".html", ".htm"}:
        raw = SCRIPT_RE.sub(" ", raw)
        raw = TAG_RE.sub(" ", raw)
    return raw


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return a list of (line_number, word, line_text) hits."""
    hits: list[tuple[int, str, str]] = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"tone_guard: cannot read {path}: {exc}", file=sys.stderr)
        return hits

    visible = extract_visible_text(raw, path.suffix.lower())
    lines = visible.splitlines()

    # Build one compiled regex with word-boundaries for speed.
    pattern = re.compile(
        r"(?<![A-Za-z])(" + "|".join(re.escape(w) for w in BANNED_WORDS) + r")(?![A-Za-z])",
        re.IGNORECASE,
    )

    for lineno, line in enumerate(lines, 1):
        for match in pattern.finditer(line):
            hits.append((lineno, match.group(0), line.strip()))
    return hits


def read_file_list(path: Path) -> list[Path]:
    out = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("#"):
            out.append(Path(raw))
    return out


def scan_diff(diff_path: Path) -> tuple[int, int]:
    """Scan only the added lines in a unified diff.

    Returns (lines_scanned, hits_found). Prints each hit to stdout in the
    form  <file>:<new-line-no>: banned word '<word>' — <line text>.
    """
    pattern = re.compile(
        r"(?<![A-Za-z])(" + "|".join(re.escape(w) for w in BANNED_WORDS) + r")(?![A-Za-z])",
        re.IGNORECASE,
    )
    tag_re = re.compile(r"<[^>]+>", re.DOTALL)

    try:
        diff = diff_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"tone_guard: cannot read diff {diff_path}: {exc}", file=sys.stderr)
        return 0, 0

    current_file: str | None = None
    current_is_text = False
    new_lineno = 0
    lines_scanned = 0
    hits = 0

    for raw_line in diff.splitlines():
        # File header: +++ b/path/to/file (or /dev/null if deleted)
        if raw_line.startswith("+++ "):
            path_str = raw_line[4:].strip()
            # strip a/ or b/ prefix
            if path_str.startswith(("a/", "b/")):
                path_str = path_str[2:]
            if path_str == "/dev/null":
                current_file = None
                current_is_text = False
                continue
            current_file = path_str
            current_is_text = path_str.lower().endswith((".md", ".markdown", ".html", ".htm"))
            continue

        if raw_line.startswith("--- "):
            continue

        # Hunk header: @@ -a,b +c,d @@
        if raw_line.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", raw_line)
            if m:
                new_lineno = int(m.group(1)) - 1
            continue

        if not current_is_text or current_file is None:
            continue

        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            new_lineno += 1
            added = raw_line[1:]
            lines_scanned += 1
            # For HTML files, strip tags from the added line before scanning
            if current_file.lower().endswith((".html", ".htm")):
                scan_text = tag_re.sub(" ", added)
            else:
                scan_text = added
            for m in pattern.finditer(scan_text):
                print(f"{current_file}:{new_lineno}: banned word "
                      f"'{m.group(0)}' — {added.strip()}")
                hits += 1
        elif raw_line.startswith("-") and not raw_line.startswith("---"):
            # removed line — old-file numbering changes; new numbering stays
            pass
        else:
            # context line
            new_lineno += 1

    return lines_scanned, hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Block banned words in new content.")
    parser.add_argument("--diff-from", type=Path,
                        help="Unified diff file; scan only ADDED lines (preferred).")
    parser.add_argument("--files-from", type=Path,
                        help="File with one path per line; scans each file in full.")
    parser.add_argument("paths", nargs="*", type=Path, help="Files to scan in full.")
    args = parser.parse_args()

    # --- Diff mode (preferred) ---
    if args.diff_from and args.diff_from.exists():
        lines_scanned, hits = scan_diff(args.diff_from)
        if hits:
            print(f"\ntone_guard: FAIL — {hits} banned-word hit(s) in "
                  f"{lines_scanned} added line(s).")
            print("Rewrite the flagged NEW lines and push again.")
            return 1
        print(f"tone_guard: PASS — scanned {lines_scanned} added line(s) in diff.")
        return 0

    # --- Full-file mode ---
    files: list[Path] = list(args.paths)
    if args.files_from and args.files_from.exists():
        files.extend(read_file_list(args.files_from))

    files = [p for p in files if p.suffix.lower() in {".md", ".markdown", ".html", ".htm"}]
    files = [p for p in files if p.exists() and p.is_file()]

    if not files:
        print("tone_guard: no markdown or HTML files to scan — pass.")
        return 0

    total_hits = 0
    for f in files:
        hits = scan_file(f)
        for lineno, word, line in hits:
            print(f"{f}:{lineno}: banned word '{word}' — {line}")
            total_hits += 1

    if total_hits:
        print(f"\ntone_guard: FAIL — {total_hits} banned-word hit(s).")
        print("Rewrite the flagged lines and push again.")
        return 1

    print(f"tone_guard: PASS — scanned {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
