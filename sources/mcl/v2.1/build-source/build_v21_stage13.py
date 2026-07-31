#!/usr/bin/env python3
"""Stage 13: accessibility residuals — named scroll regions, nav landmark,
sidebar completeness, focus-ring and badge contrast."""
import re, sys, io, html as H

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:180])
    return html.replace(needle, repl, n)


# ------------------------------------ 1. focus ring: two-colour, navy + amber
h = must(h, ':focus-visible { outline:3px solid #F6C344; outline-offset:3px; }',
            ':focus-visible { outline:3px solid #1B2A4A; outline-offset:3px; box-shadow:0 0 0 5px #F6C344; }')
h = must(h, '.tbl-wrap:focus-visible, .fig-scroll:focus-visible { outline:3px solid #F6C344; outline-offset:2px; }',
            '.tbl-wrap:focus-visible, .fig-scroll:focus-visible { outline:3px solid #1B2A4A; outline-offset:2px; box-shadow:0 0 0 5px #F6C344; }')

# ------------------------------------ 2. tier C badge contrast: dark text on amber
h = must(h, '.tier.c { background:#b08538; }', '.tier.c { background:#e0b externally; }')
h = h.replace('.tier.c { background:#e0b externally; }',
              '.tier.c { background:#d8a441; color:#241a05; }')

# ------------------------------------ 3. section strip becomes a nav landmark
h = must(h, '<div class="anchor-nav">', '<nav class="anchor-nav" aria-label="MCL guideline sections">')
h = must(h, '<div class="anchor-nav-inner" aria-label="MCL guideline sections">',
            '<div class="anchor-nav-inner">')
# close the right element: the anchor-nav block ends with two </div> then a blank line
h = re.sub(r'(<nav class="anchor-nav" aria-label="MCL guideline sections">.*?</div>\s*</div>\s*)</div>',
           r'\1</nav>', h, count=1, flags=re.S)

# ------------------------------------ 4. sidebar: restore missing section 19
h = must(h, '<li><a href="#access-status">18. Regulatory and access matrix</a></li>',
            '<li><a href="#access-status">18. Regulatory and access matrix</a></li>\n'
            '          <li><a href="#evidence-boundary">19. Evidence boundary</a></li>')

# ------------------------------------ 5. name every scrollable region
heads = [(m.start(), re.sub(r'<[^>]+>', '', m.group(1)).strip())
         for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', h, re.S)]


def nearest(pos):
    best = 'Guideline content'
    for p, t in heads:
        if p < pos:
            best = t
        else:
            break
    return H.unescape(re.sub(r'\s+', ' ', best))[:90]


def name_regions(html, cls, suffix):
    out, last, n = [], 0, 0
    for m in re.finditer(r'<div class="%s" tabindex="0">' % re.escape(cls), html):
        # prefer the table's own caption where one exists
        seg = html[m.end():m.end() + 400]
        cap = re.search(r'<caption class="vh">(.*?)</caption>', seg)
        label = H.unescape(cap.group(1)) if cap else nearest(m.start())
        label = label.replace('"', '').strip()
        out.append(html[last:m.start()])
        out.append('<div class="%s" tabindex="0" role="region" aria-label="%s%s">'
                   % (cls, H.escape(label, quote=True), suffix))
        last = m.end()
        n += 1
    out.append(html[last:])
    return ''.join(out), n


h, n1 = name_regions(h, 'tbl-wrap', '; scroll horizontally')
h, n2 = name_regions(h, 'fig-scroll', ' algorithm; scroll horizontally')

# ------------------------------------ 6. sidebar card titles become headings
h = h.replace('<div class="sidebar-card-header">', '<h2 class="sidebar-card-header">')
h = re.sub(r'(<h2 class="sidebar-card-header">[^<]*)</div>', r'\1</h2>', h)

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d named_tables=%d named_figures=%d' % (OUT, len(h), n1, n2))
