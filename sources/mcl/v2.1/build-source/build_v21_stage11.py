#!/usr/bin/env python3
"""Stage 11: accessibility and structural fixes from the audit.

Table captions from the nearest preceding heading, keyboard-focusable scroll
regions, print rules, complete section navigation, verification vocabulary.
"""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:180])
    return html.replace(needle, repl, n)


# ------------------------------------- visually-hidden + focus + print styling
h = must(h, '    .qr-table td:first-child { font-weight:700; }',
"""    .vh { position:absolute; width:1px; height:1px; margin:-1px; padding:0; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }
    .tbl-wrap:focus-visible, .fig-scroll:focus-visible { outline:3px solid #F6C344; outline-offset:2px; }
    @media print {
      .site-nav-shell, .anchor-nav, .gl-sidebar { display:none !important; }
      .gl-layout { display:block !important; padding:0 !important; }
      .gl-main { width:100% !important; }
      .tbl-wrap, .fig-scroll { overflow:visible !important; }
      svg.pathway { min-width:0 !important; width:100% !important; }
      section { break-inside:auto; border:none; padding-left:0; padding-right:0; }
      h2, h3 { break-after:avoid; }
      table, figure { break-inside:avoid; }
      .draft-banner, .page-footer, header.page-hero { display:block !important; }
      .page-footer { color:black !important; background:none !important; border-top:2px solid #000; }
      a[href^="http"]::after { content:" (" attr(href) ")"; font-size:.75em; word-break:break-all; }
    }
    .qr-table td:first-child { font-weight:700; }""")

# ------------------------------------------------ captions from nearest heading
heads = [(m.start(), re.sub(r'<[^>]+>', '', m.group(1)).strip())
         for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', h, re.S)]


def nearest(pos):
    best = 'Table'
    for p, t in heads:
        if p < pos:
            best = t
        else:
            break
    return re.sub(r'\s+', ' ', best)[:110]


out, last, added = [], 0, 0
for m in re.finditer(r'<table(?: class="[^"]*")?>', h):
    tail = h[m.end():m.end() + 240]
    if '<caption' in tail:
        continue
    label = nearest(m.start()).replace('&', '&amp;')
    out.append(h[last:m.end()])
    out.append('<caption class="vh">%s</caption>' % label)
    last = m.end()
    added += 1
out.append(h[last:])
h = ''.join(out)

# --------------------------------- keyboard-focusable horizontal scroll regions
h = h.replace('<div class="tbl-wrap">', '<div class="tbl-wrap" tabindex="0">')
h = h.replace('<div class="fig-scroll">', '<div class="fig-scroll" tabindex="0">')

# ------------------------------------------- complete the section strip
NAVFULL = """      <a href="#scope">1. Scope and use</a>
      <a href="#diagnosis">2. Diagnosis and minimum dataset</a>
      <a href="#staging-risk">3. Staging and risk</a>
      <a href="#observation">4. Observation where treatment is not required</a>
      <a href="#limited-stage">5. Limited-stage disease</a>
      <a href="#first-line-fit">6. First-line pathway for younger or treatment-fit adults</a>
      <a href="#first-line-older">7. First-line pathway for older or transplant-ineligible adults</a>
      <a href="#high-risk">8. TP53-mutated and other high-risk MCL</a>
      <a href="#relapsed">9. Relapsed or refractory pathway</a>
      <a href="#cns">10. Central nervous system involvement</a>
      <a href="#response-mrd">11. Response assessment, MRD and maintenance</a>
      <a href="#supportive-care">12. Supportive care and treatment safety</a>
      <a href="#follow-up">13. Follow-up and MDT documentation</a>
      <a href="#jurisdictions">14. Regulatory and access boundary</a>
      <a href="#evidence-model">15. Evidence-to-recommendation model</a>
      <a href="#trials">16. Clinical trials</a>
      <a href="#non-routine-access">17. Non-routine access routes</a>
      <a href="#access-status">18. Regulatory and access matrix</a>
      <a href="#evidence-boundary">19. Evidence boundary</a>
      <a href="#evidence-references">20. Evidence references</a>
      <a href="#release-control">21. Release control</a>"""
h = re.sub(r'(<div class="anchor-nav-inner" aria-label="MCL guideline sections">\n).*?(\n    </div>)',
           lambda m: m.group(1) + NAVFULL + m.group(2), h, count=1, flags=re.S)

# ----------------------------------------- verification vocabulary in §19
h = must(h,
  '<p>Scientific extraction is abstract-only except for the verified full text of S01',
  """<div class="changed"><strong>Verification status is not uniform, and the labels below say so</strong>
      <p>An independent audit on 30 July 2026 checked all 43 references carrying a PMID against PubMed and all 50 carrying a DOI against Crossref. No title, PMID or DOI mismatch was found, and no retraction or expression-of-concern signal was detected. Identifier integrity is therefore sound.</p>
      <p>That is not the same as verifying the science. Most extraction here is abstract-level, and the audit found the recurring weakness was not fabricated studies but <strong>broadening a conditional source recommendation into a categorical instruction</strong> — particularly in supportive care after cellular therapy, in causal language applied to observational evidence, and in subgroup findings stated as general conclusions. Several such statements have been narrowed in this revision.</p>
      <p>Before ratification every recommendation-bearing source should carry one of: FULL_TEXT_VERIFIED, ABSTRACT_ONLY, OFFICIAL_GUIDELINE_FULL_TEXT, OFFICIAL_REGULATORY_SOURCE, OFFICIAL_HTA_SOURCE, or CORRECTION_UNRESOLVED. Outcome figures taken only from an abstract must not be presented as though protocol, denominators, supplementary analyses and adverse-event methods had been checked in full.</p>
    </div>
    <p>Scientific extraction is abstract-only except for the verified full text of S01""")

# ------------------------------------- release control unchanged, stated plainly
h = must(h,
  '<p>Every statement of marketing authorisation, HTA recommendation and commissioning status below must be re-checked against the official source before ratification.',
  '<p>An independent three-track audit on 30 July 2026 corrected several factual errors in this draft, including two where an earlier revision wrongly withdrew a correct v2.0 statement. Those corrections do <strong>not</strong> change the release state: this remains unratified, clinical review and pharmacy verification remain pending, and publication authority remains false.</p>'
  '<p>Every statement of marketing authorisation, HTA recommendation and commissioning status below must be re-checked against the official source before ratification.')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d captions_added=%d' % (OUT, len(h), added))
