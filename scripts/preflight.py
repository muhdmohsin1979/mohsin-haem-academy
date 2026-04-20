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

# A reference-identifier marker, followed only by word characters, whitespace,
# or the separators typically found inside a DOI / PMID / PMCID string
# (colon, equals, dot, slash, hyphen, brackets, square brackets). If such a
# run reaches the end of the lead (i.e. directly adjoins the matched digits),
# the matched digits are part of a reference identifier — not patient PII.
_REF_MARKER_AT_END_RE = re.compile(
    r"(?:DOI|doi\.org|dx\.doi\.org|PMID|PMCID|PMC|10\.\d{3,6})"
    r"[\w\s:=./\-\[\]()]*$",
    re.IGNORECASE,
)


def _is_reference_identifier(text: str, match_start: int) -> bool:
    """True if an NHS-number match is actually a DOI / PMID / PMCID fragment.

    Looks at up to 80 chars of the lead immediately before the match. Returns
    True if a reference-identifier marker (DOI, PMID, PMCID, PMC, doi.org,
    10.NNNN) appears and is connected to the match by a run of word chars,
    whitespace, or common identifier separators (`:` `=` `.` `/` `-` `[` `]`).
    """
    window_start = max(0, match_start - 80)
    lead = text[window_start:match_start]
    return bool(_REF_MARKER_AT_END_RE.search(lead))

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
            # Suppress NHS-number false positives on reference identifiers
            # (DOI suffixes, PMIDs, PMCIDs).
            if label == "NHS number" and _is_reference_identifier(visible, m.start()):
                continue
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


def _self_test() -> int:
    """Run the internal regression tests for PII detection.

    Verifies that the NHS-number regex suppresses DOI / PMID / PMCID
    false positives but still catches genuine 10-digit identifiers.
    """
    cases_no_hit = [
        ("DOI:10.1182/blood.2024024631",          "See reference [DOI:10.1182/blood.2024024631]"),
        ("doi.org URL",                            "https://doi.org/10.1056/NEJMoa2024024631"),
        ("10.1182 DOI prefix",                     "Published Blood 2024 (10.1182/blood.2024024631)"),
        ("PMID:1234567890",                        "PMID:1234567890 — Al-Sawaf et al"),
        ("PMID 1234567890 (space)",                "[PMID 1234567890]"),
        ("PMID: 1234567890 (colon+space)",         "Reference PMID: 1234567890 confirms this."),
        ("PMCID:PMC1234567890",                    "PMCID:PMC1234567890"),
        ("PMCID: PMC1234567890",                   "PMCID: PMC1234567890."),
        ("DOI= (equals form)",                     "DOI=10.1182/blood.2024024631"),
        ("DOI in bracket then slash",              "[DOI:10.1182/blood.2024024631] A2"),
    ]
    cases_one_hit = [
        ("bare 10-digit NHS-style",   "Patient NHS 123 456 7890 presented with..."),
        ("10-digit trust ref",        "Trust reference 9876543210 from casenote system."),
        ("prose clinical note",       "Seen today: patient 2345678901 on DOAC therapy."),
        ("no marker in lead",         "The number 1234567890 was reported."),
    ]

    failures = 0
    for label, text in cases_no_hit:
        hits = [h for h in scan_pii(Path("<self-test>"), text, ".md") if "NHS number" in h]
        if hits:
            failures += 1
            print(f"FAIL  expected 0 NHS hits — {label}")
            for h in hits:
                print(f"      -> {h}")
        else:
            print(f"PASS  {label}")
    for label, text in cases_one_hit:
        hits = [h for h in scan_pii(Path("<self-test>"), text, ".md") if "NHS number" in h]
        if len(hits) != 1:
            failures += 1
            print(f"FAIL  expected 1 NHS hit, got {len(hits)} — {label}")
            for h in hits:
                print(f"      -> {h}")
        else:
            print(f"PASS  {label}")

    total = len(cases_no_hit) + len(cases_one_hit)
    passed = total - failures
    print(f"\nself-test: {passed}/{total} passed.")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="PII + link check for new content.")
    parser.add_argument("--files-from", type=Path)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--skip-links", action="store_true",
                        help="Do not hit the network; PII check only.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the internal PII-regex regression tests.")
    args = parser.parse_args()

    if args.self_test:
        return _self_test()

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
