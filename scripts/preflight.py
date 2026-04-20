#!/usr/bin/env python3
"""
preflight.py — PII sweep and external link check on new or changed content.

Runs inside GitHub Actions after tone_guard.py passes. Exits:
    0  all checks passed
    1  PII pattern found OR one or more external links returned non-2xx/3xx
    2  usage / IO error

Checks performed on each markdown/HTML file:
  1. PII regex sweep — NHS numbers (10 digits, optionally spaced as
     3-3-4), hospital numbers (common NHS trust patterns), dates of
     birth, patient name markers.
  2. Link check — HEAD request (fallback to GET) on every http/https
     URL; allow 200/301/302/308; fail on 4xx/5xx/timeout.

Usage:
    python scripts/preflight.py --files-from changed.txt
    python scripts/preflight.py path/to/file.html
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("preflight: 'requests' not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(2)

try:
    from bs4 import BeautifulSoup
    HAVE_BS4 = True
except ImportError:
    HAVE_BS4 = False

# --- PII patterns ----------------------------------------------------------

NHS_NUMBER_RE = re.compile(
    r"\b\d{3}[ -]?\d{3}[ -]?\d{4}\b"
)
# Common hospital / MRN patterns (letter prefix + 6-8 digits, or 8-10 digits)
HOSPITAL_NUMBER_RE = re.compile(
    r"\b(?:MRN|Hospital No\.?|Hosp No\.?|NHS No\.?)[:\s]*([A-Z]{0,3}\d{6,10})\b",
    re.IGNORECASE,
)
DOB_RE = re.compile(
    r"\b(?:DOB|D\.O\.B|Date of birth)[:\s]*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b",
    re.IGNORECASE,
)
PATIENT_MARKER_RE = re.compile(
    r"\b(?:Patient|Pt)\s+Name[:\s]+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b",
)

PII_PATTERNS = [
    ("NHS number", NHS_NUMBER_RE),
    ("Hospital number", HOSPITAL_NUMBER_RE),
    ("Date of birth", DOB_RE),
    ("Patient name marker", PATIENT_MARKER_RE),
]

# --- Link extraction -------------------------------------------------------

URL_RE = re.compile(r"https?://[^\s'\"<>\)\]]+", re.IGNORECASE)
HTML_HREF_RE = re.compile(r'(?:href|src)\s*=\s*["\'](https?://[^"\']+)["\']', re.IGNORECASE)

# Domains to skip (rate-limit themselves or block HEAD)
SKIP_DOMAINS = {
    "doi.org",           # always 301s reliably; no need to hammer
    "dx.doi.org",
    "scholar.google.com",
}

ALLOW_STATUS = {200, 201, 202, 203, 204, 301, 302, 303, 307, 308}


def tag_strip(raw: str) -> str:
    if HAVE_BS4:
        return BeautifulSoup(raw, "html.parser").get_text(" ")
    return re.sub(r"<[^>]+>", " ", raw)


def extract_links(raw: str, suffix: str) -> list[str]:
    links: set[str] = set()
    if suffix in {".html", ".htm"}:
        for m in HTML_HREF_RE.finditer(raw):
            links.add(m.group(1))
    # plus any bare URL in visible text
    visible = tag_strip(raw) if suffix in {".html", ".htm"} else raw
    for m in URL_RE.finditer(visible):
        links.add(m.group(0).rstrip(".,;)"))
    return sorted(links)


def scan_pii(path: Path, raw: str, suffix: str) -> list[str]:
    visible = tag_strip(raw) if suffix in {".html", ".htm"} else raw
    hits = []
    for label, pattern in PII_PATTERNS:
        for m in pattern.finditer(visible):
            snippet = m.group(0)
            hits.append(f"{path}: possible {label} — '{snippet}'")
    return hits


def check_link(url: str, timeout: float = 10.0) -> tuple[bool, str]:
    # Skip rate-limited or reliable-301 domains
    for dom in SKIP_DOMAINS:
        if dom in url:
            return True, "skipped"
    headers = {"User-Agent": "mohsin-haem-academy-preflight/1.0"}
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout, headers=headers)
        if r.status_code in ALLOW_STATUS:
            return True, str(r.status_code)
        # HEAD not supported by some servers — retry as GET
        r = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers, stream=True)
        r.close()
        if r.status_code in ALLOW_STATUS:
            return True, str(r.status_code)
        return False, str(r.status_code)
    except requests.RequestException as exc:
        return False, f"error: {exc.__class__.__name__}"


def read_file_list(path: Path) -> list[Path]:
    out = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("#"):
            out.append(Path(raw))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="PII + link check for new content.")
    parser.add_argument("--files-from", type=Path)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--skip-links", action="store_true",
                        help="Do not hit the network; PII check only.")
    args = parser.parse_args()

    files: list[Path] = list(args.paths)
    if args.files_from and args.files_from.exists():
        files.extend(read_file_list(args.files_from))

    files = [p for p in files if p.suffix.lower() in {".md", ".markdown", ".html", ".htm"}]
    files = [p for p in files if p.exists() and p.is_file()]

    if not files:
        print("preflight: no markdown or HTML files to scan — pass.")
        return 0

    pii_hits: list[str] = []
    link_failures: list[str] = []

    for f in files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        suffix = f.suffix.lower()
        pii_hits.extend(scan_pii(f, raw, suffix))

        if args.skip_links:
            continue

        for url in extract_links(raw, suffix):
            ok, detail = check_link(url)
            if not ok:
                link_failures.append(f"{f}: {url} -> {detail}")

    print(f"preflight: scanned {len(files)} file(s).")

    if pii_hits:
        print("\nPII hits:")
        for h in pii_hits:
            print(f"  {h}")

    if link_failures:
        print("\nLink failures:")
        for f in link_failures:
            print(f"  {f}")

    if pii_hits or link_failures:
        print(f"\npreflight: FAIL — {len(pii_hits)} PII hit(s), "
              f"{len(link_failures)} broken link(s).")
        return 1

    print("preflight: PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
