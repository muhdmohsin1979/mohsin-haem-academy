# MCL v2.1 build chain — source of record

Run order (each stage rewrites `/home/claude/mcl-v2.1-draft.html` in place; always run the
whole chain from `build_v21.py`, never a single stage twice — stage 11 is not idempotent):

    python3 build_v21.py
    for i in 2 3 4 5 6 7 8 9 10 11 12 13 14; do python3 build_v21_stage$i.py; done
    python3 diagrams_v21.py     # writes the four standalone dg-*.svg

`diagrams_v21.py` is the single node model for all four pathway diagrams. The inline SVGs in
the HTML and the standalone `dg-*.svg` files are emitted from the same functions, which is why
they are canonical-XML equal. Marker ids are namespaced per diagram inside `document()`.

Every stage uses a fail-closed `must()` helper: if an anchor string is not found the stage exits
non-zero rather than writing a partially patched file. `soft()` is used only where a needle is
allowed to be absent because an earlier stage may already have produced the final wording.

## Verification scripts

- `console.mjs`     — console/pageerror capture + focus-ring and tier-badge contrast maths
- `printcheck.mjs`  — layout at 1200/901/900/600/375px and print-media emulation
- `axeoffline.mjs`  — axe-core 4.10.2 from `node_modules`, WCAG 2.0/2.1 A+AA plus best-practice
- `contrast_svg.py` — resolves SVG text contrast, which axe reports as incomplete
- `contrast_dom.mjs`— resolves every distinct DOM colour pair, including axe's obscured/overlap cases
- `linkcheck.mjs`   — link-in-text-block distinguishability
