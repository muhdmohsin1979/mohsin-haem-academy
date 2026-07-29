#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence.json"
TEXT_ROOT = ROOT / "extracted-text"
SOURCE_TEXT = {
    "bortezomib-velcade": "bortezomib.txt",
    "ibrutinib-imbruvica": "ibrutinib.txt",
    "zanubrutinib-brukinsa": "zanubrutinib.txt",
    "brexucabtagene-autoleucel-tecartus": "brexucabtagene-autoleucel.txt",
    "acalabrutinib-calquence": "acalabrutinib.txt",
    "pirtobrutinib-jaypirca": "pirtobrutinib.txt",
    "lisocabtagene-maraleucel-breyanzi": "lisocabtagene-maraleucel.txt",
    "lenalidomide-revlimid": "lenalidomide.txt",
}

def norm(s: str) -> str:
    # Accommodate extraction-only line wrapping and typographic glyph variants while
    # preserving wording, numbers, punctuation and semantic order.
    s = s.replace("\r\n", "\n").replace("\u00ad", "")
    s = re.sub(r"===== PDF PAGE \d+ =====", " ", s)
    s = re.sub(r"(?<=[A-Za-z])-[\s\n]+(?=[a-z])", "", s)
    s = s.replace("\u2010", "-").replace("\u2011", "-")
    s = s.replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2212", "-").replace("µ", "μ").replace("²", "2")
    s = s.replace("×", "x").replace("≥", ">=").replace("≤", "<=")
    s = s.replace("-", "").replace("•", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def iter_quotes(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if k == "quote" and isinstance(v, str):
                yield p, v
            elif k == "quotes" and isinstance(v, list):
                for i, q in enumerate(v):
                    if isinstance(q, str):
                        yield f"{p}[{i}]", q
            elif k == "combination_agent_boundary_quote" and isinstance(v, str):
                yield p, v
            else:
                yield from iter_quotes(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_quotes(v, f"{path}[{i}]")

def main():
    data = json.loads(EVIDENCE.read_text())
    texts = {sid: norm((TEXT_ROOT / name).read_text()) for sid, name in SOURCE_TEXT.items()}
    failed = []
    checked = 0
    for i, rec in enumerate(data["licensed_mcl_treatments"]):
        source = texts[rec["source_id"]]
        for path, quote in iter_quotes(rec):
            checked += 1
            if norm(quote) not in source:
                failed.append((i, rec["treatment"], path, quote))
    print(f"checked={checked} failed={len(failed)}")
    for i, treatment, path, quote in failed:
        print(f"FAIL record={i} treatment={treatment} field={path}\n  {quote}")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
