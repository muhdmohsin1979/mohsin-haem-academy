#!/usr/bin/env python3
"""
migrate_content_folders.py — one-shot legacy migration into /guidelines/<topic>/.

Moves each guideline's root-level files into a topic folder, renames them to
the standard pattern (index.html, guideline.pdf, quickref.pdf, algorithm.svg,
etc.), rewrites every internal link across the site, and writes the
_redirects file so every old URL continues to resolve with a 301.

Runs exactly once on the feat-restructure-content-folders-v1 branch. Safe to
re-run (it is idempotent — already-moved files are skipped).
"""

from __future__ import annotations
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# old_basename → new_relative_path (under the repo root)
MIGRATIONS: dict[str, str] = {
    # anaemia in pregnancy
    "anaemia-in-pregnancy.html":                   "guidelines/anaemia-in-pregnancy/index.html",
    "anaemia-in-pregnancy-audit.xlsx":             "guidelines/anaemia-in-pregnancy/audit.xlsx",
    "anaemia-in-pregnancy-diagnostic-pathway.svg": "guidelines/anaemia-in-pregnancy/diagnostic-pathway.svg",
    "anaemia-in-pregnancy-guideline.pdf":          "guidelines/anaemia-in-pregnancy/guideline.pdf",
    "anaemia-in-pregnancy-iv-iron-pathway.svg":    "guidelines/anaemia-in-pregnancy/iv-iron-pathway.svg",
    "anaemia-in-pregnancy-logic.json":             "guidelines/anaemia-in-pregnancy/logic.json",
    "anaemia-in-pregnancy-patient-leaflet.docx":   "guidelines/anaemia-in-pregnancy/patient-leaflet.docx",
    "anaemia-in-pregnancy-postpartum-pathway.svg": "guidelines/anaemia-in-pregnancy/postpartum-pathway.svg",
    "anaemia-in-pregnancy-quickref.pdf":           "guidelines/anaemia-in-pregnancy/quickref.pdf",
    "anaemia-in-pregnancy-teaching-deck.pdf":      "guidelines/anaemia-in-pregnancy/teaching-deck.pdf",
    "anaemia-in-pregnancy-teaching-deck.pptx":     "guidelines/anaemia-in-pregnancy/teaching-deck.pptx",
    "anaemia-in-pregnancy-treatment-pathway.svg":  "guidelines/anaemia-in-pregnancy/treatment-pathway.svg",

    # CLL
    "cll.html":                  "guidelines/cll/index.html",
    "cll-algorithm.excalidraw":  "guidelines/cll/algorithm.excalidraw",
    "cll-algorithm.svg":         "guidelines/cll/algorithm.svg",
    "cll-guideline.pdf":         "guidelines/cll/guideline.pdf",
    "cll-quickref.pdf":          "guidelines/cll/quickref.pdf",

    # ITP
    "itp.html":                  "guidelines/itp/index.html",
    "itp-algorithm.excalidraw":  "guidelines/itp/algorithm.excalidraw",
    "itp-algorithm.svg":         "guidelines/itp/algorithm.svg",
    "itp-guideline.pdf":         "guidelines/itp/guideline.pdf",
    "itp-quickref.pdf":          "guidelines/itp/quickref.pdf",

    # VTE-cancer (the cat-* assets belong here — CAT = Cancer-Associated Thrombosis)
    "vte-cancer.html":           "guidelines/vte-cancer/index.html",
    "cat-algorithm.excalidraw":  "guidelines/vte-cancer/algorithm.excalidraw",
    "cat-algorithm.svg":         "guidelines/vte-cancer/algorithm.svg",
    "cat-guideline.pdf":         "guidelines/vte-cancer/guideline.pdf",
    "cat-quickref.pdf":          "guidelines/vte-cancer/quickref.pdf",
}

# For each HTML file that will be RELOCATED inside guidelines/<topic>/, this
# gives the in-file link rewrites. Keys are old url values, values are new
# url values expressed relative to the new location of the HTML file.
INNER_REWRITES: dict[str, dict[str, str]] = {
    "anaemia-in-pregnancy.html": {
        "anaemia-in-pregnancy-audit.xlsx":             "audit.xlsx",
        "anaemia-in-pregnancy-diagnostic-pathway.svg": "diagnostic-pathway.svg",
        "anaemia-in-pregnancy-guideline.pdf":          "guideline.pdf",
        "anaemia-in-pregnancy-iv-iron-pathway.svg":    "iv-iron-pathway.svg",
        "anaemia-in-pregnancy-logic.json":             "logic.json",
        "anaemia-in-pregnancy-patient-leaflet.docx":   "patient-leaflet.docx",
        "anaemia-in-pregnancy-postpartum-pathway.svg": "postpartum-pathway.svg",
        "anaemia-in-pregnancy-quickref.pdf":           "quickref.pdf",
        "anaemia-in-pregnancy-teaching-deck.pdf":      "teaching-deck.pdf",
        "anaemia-in-pregnancy-teaching-deck.pptx":     "teaching-deck.pptx",
        "anaemia-in-pregnancy-treatment-pathway.svg":  "treatment-pathway.svg",
        "itp.html":                                    "../itp/",
        # Links back to hub pages at root need one level up
        "index.html":        "../../index.html",
        "about.html":        "../../about.html",
        "contact.html":      "../../contact.html",
        "guidelines.html":   "../../guidelines.html",
        "governance.html":   "../../governance.html",
        "education.html":    "../../education.html",
        "journal-club.html": "../../journal-club.html",
        "tools.html":        "../../tools.html",
        "haemcalc.html":     "../../haemcalc.html",
        "calculator.html":   "../../calculator.html",
    },
    "cll.html": {
        "cll-guideline.pdf": "guideline.pdf",
        "cll-quickref.pdf":  "quickref.pdf",
        "cll.html":          "./",
        "itp.html":          "../itp/",
        "vte-cancer.html":   "../vte-cancer/",
        "index.html":        "../../index.html",
        "about.html":        "../../about.html",
        "contact.html":      "../../contact.html",
        "guidelines.html":   "../../guidelines.html",
        "governance.html":   "../../governance.html",
        "education.html":    "../../education.html",
        "journal-club.html": "../../journal-club.html",
        "tools.html":        "../../tools.html",
        "haemcalc.html":     "../../haemcalc.html",
        "calculator.html":   "../../calculator.html",
    },
    "itp.html": {
        "itp-algorithm.svg":  "algorithm.svg",
        "itp-guideline.pdf":  "guideline.pdf",
        "itp-quickref.pdf":   "quickref.pdf",
        "itp.html":           "./",
        "vte-cancer.html":    "../vte-cancer/",
        "index.html":         "../../index.html",
        "about.html":         "../../about.html",
        "contact.html":       "../../contact.html",
        "guidelines.html":    "../../guidelines.html",
        "governance.html":    "../../governance.html",
        "education.html":     "../../education.html",
        "journal-club.html":  "../../journal-club.html",
        "tools.html":         "../../tools.html",
        "haemcalc.html":      "../../haemcalc.html",
        "calculator.html":    "../../calculator.html",
    },
    "vte-cancer.html": {
        "cat-algorithm.svg":  "algorithm.svg",
        "cat-guideline.pdf":  "guideline.pdf",
        "cat-quickref.pdf":   "quickref.pdf",
        "vte-cancer.html":    "./",
        "index.html":         "../../index.html",
        "about.html":         "../../about.html",
        "contact.html":       "../../contact.html",
        "guidelines.html":    "../../guidelines.html",
        "governance.html":    "../../governance.html",
        "education.html":     "../../education.html",
        "journal-club.html":  "../../journal-club.html",
        "tools.html":         "../../tools.html",
        "haemcalc.html":      "../../haemcalc.html",
        "calculator.html":    "../../calculator.html",
    },
}

# For HTML files that STAY at the repo root (hub pages), old urls rewrite to
# the new /guidelines/<topic>/... paths.
ROOT_REWRITES: dict[str, str] = {
    # page rewrites (single-topic pages → topic folder)
    "anaemia-in-pregnancy.html": "guidelines/anaemia-in-pregnancy/",
    "cll.html":                  "guidelines/cll/",
    "itp.html":                  "guidelines/itp/",
    "vte-cancer.html":           "guidelines/vte-cancer/",
}
# asset rewrites at root — preserve extension/filename
for old, new in MIGRATIONS.items():
    if old.endswith(".html"):
        continue
    ROOT_REWRITES[old] = new


# Attribute rewrite regex — matches href="..." or src="..." (also handles
# spaces around =, single or double quotes, and ignores anchors/queries).
ATTR_PATTERN = re.compile(
    r'((?:href|src)\s*=\s*["\'])([^"\'#?]+)((?:[#?][^"\']*)?["\'])',
    re.IGNORECASE,
)


def rewrite_html(file_path: pathlib.Path, rules: dict[str, str]) -> bool:
    """Rewrite in place. Returns True if file was modified."""
    raw = file_path.read_text(encoding="utf-8", errors="replace")
    changed = False

    def _sub(m: re.Match) -> str:
        nonlocal changed
        prefix, url, suffix = m.group(1), m.group(2), m.group(3)
        # leave external and protocol-relative alone
        if url.startswith(("http://", "https://", "mailto:", "tel:", "//", "/")):
            return m.group(0)
        # leave same-dir anchors alone
        if url.startswith("#"):
            return m.group(0)
        if url in rules:
            changed = True
            return f"{prefix}{rules[url]}{suffix}"
        return m.group(0)

    new = ATTR_PATTERN.sub(_sub, raw)
    if changed:
        file_path.write_text(new, encoding="utf-8")
    return changed


def git_mv(old: pathlib.Path, new: pathlib.Path) -> None:
    new.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(old), str(new)], check=True, cwd=ROOT)


def run() -> int:
    # 1. Rewrite links INSIDE files that are about to be moved (rules
    #    expressed relative to their new location).
    for old_name, rules in INNER_REWRITES.items():
        p = ROOT / old_name
        if not p.exists():
            # already moved from a previous run — skip
            continue
        if rewrite_html(p, rules):
            print(f"rewrote internal links in {old_name}")

    # 2. Rewrite links in hub pages that STAY at the root.
    hub_pages = [
        "index.html", "guidelines.html", "about.html", "contact.html",
        "education.html", "governance.html", "journal-club.html",
        "tools.html", "haemcalc.html", "calculator.html",
    ]
    for name in hub_pages:
        p = ROOT / name
        if not p.exists():
            continue
        if rewrite_html(p, ROOT_REWRITES):
            print(f"rewrote root-hub links in {name}")

    # 3. Rewrite links in sitemap.xml (treat same as root hub for url rewriting)
    sitemap = ROOT / "sitemap.xml"
    if sitemap.exists():
        raw = sitemap.read_text(encoding="utf-8", errors="replace")
        changed = False
        for old, new in ROOT_REWRITES.items():
            # sitemap contains full URLs — match the path after the domain
            pattern = re.compile(r'(/)' + re.escape(old) + r'(?=["<])')
            new_raw, n = pattern.subn(r'\1' + new, raw)
            if n:
                raw = new_raw
                changed = True
        if changed:
            sitemap.write_text(raw, encoding="utf-8")
            print("rewrote sitemap.xml URLs")

    # 4. Move the files with git mv (preserves history).
    for old, new in MIGRATIONS.items():
        src = ROOT / old
        dst = ROOT / new
        if not src.exists() and dst.exists():
            continue  # already moved
        if not src.exists():
            print(f"warning: source missing: {old}")
            continue
        git_mv(src, dst)
        print(f"moved {old} -> {new}")

    # 5. Remove the guidelines/.gitkeep now that the folder has real content.
    gk = ROOT / "guidelines" / ".gitkeep"
    if gk.exists():
        subprocess.run(["git", "rm", str(gk.relative_to(ROOT))], check=True, cwd=ROOT)
        print("removed guidelines/.gitkeep (folder now has real content)")

    # 6. Write _redirects for Cloudflare Pages (301 every old URL to new).
    redirects_path = ROOT / "_redirects"
    lines = [
        "# Legacy URL redirects — preserve every old path after the "
        "content restructure.",
        "# Format: <old path>   <new path>   <status>",
        "# 301 = permanent; Cloudflare caches and search engines update.",
        "",
    ]
    for old, new in MIGRATIONS.items():
        old_path = "/" + old
        if new.endswith("/index.html"):
            new_path = "/" + new[:-len("index.html")]
        else:
            new_path = "/" + new
        lines.append(f"{old_path}   {new_path}   301")
    redirects_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {redirects_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(run())
