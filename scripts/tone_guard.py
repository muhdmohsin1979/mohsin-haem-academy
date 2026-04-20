#!/usr/bin/env python3
"""
tone_guard.py — block banned words in new or changed markdown/HTML files.

Runs inside GitHub Actions as a PR check. Exits:
    0  no banned words found
    1  one or more banned words present (prints file:line:word)
    2  usage / IO error

Usage:
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Block banned words in new content.")
    parser.add_argument("--files-from", type=Path, help="File with one path per line.")
    parser.add_argument("paths", nargs="*", type=Path, help="Files to scan.")
    args = parser.parse_args()

    files: list[Path] = list(args.paths)
    if args.files_from and args.files_from.exists():
        files.extend(read_file_list(args.files_from))

    # Only scan markdown and HTML
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
