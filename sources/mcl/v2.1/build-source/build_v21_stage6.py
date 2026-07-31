#!/usr/bin/env python3
"""Stage 6: inline the four pathway SVGs and add the one-page quick reference."""
import sys, io
sys.path.insert(0, '/home/claude')
from diagrams_v21 import DIAGRAMS

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:170])
    return html.replace(needle, repl, n)


def figure(key, caption):
    svg = DIAGRAMS[key]()
    return ('<figure class="fig">\n  <div class="fig-scroll">\n%s\n  </div>\n'
            '  <figcaption>%s Scroll horizontally on a small screen. '
            'Access labels follow the key in section 16 and are separate determinations from the evidence.</figcaption>\n'
            '</figure>' % (svg, caption))


# ------------------------------------------------------------------- styling
h = must(h, '    .status-card.alert { border-top-color:var(--red); }',
"""    .status-card.alert { border-top-color:var(--red); }
    figure.fig { margin:1.3rem 0 1.1rem; }
    .fig-scroll { overflow-x:auto; -webkit-overflow-scrolling:touch; border:1px solid var(--line); border-radius:10px; background:var(--paper); }
    svg.pathway { display:block; width:100%; min-width:880px; height:auto; }
    figure.fig figcaption { margin-top:.55rem; color:#5B6472; font:400 .86rem/1.5 Arial,sans-serif; }
    .qr-table td:first-child { font-weight:700; }
    .qr-table td, .qr-table th { font-size:.86rem; padding:.45rem .5rem; }""")

# ------------------------------------------------- A. first-line into section 5
h = must(h,
  '<p>Select treatment according to biological risk, treatment requirement, physiological fitness and suitability for dose-intensive treatment or ASCT—not chronological age alone.</p>',
  '<p>Select treatment according to biological risk, treatment requirement, physiological fitness and suitability for dose-intensive treatment or ASCT—not chronological age alone.</p>\n    '
  + figure('first-line', 'First-line treatment algorithm. The split at transplant suitability governs both the clinical pathway and, because the two first-line marketing authorisations divide on exactly that line, which company scheme a patient can enter.'))

# -------------------------------------------------- C. high-risk into section 7
h = must(h,
  '<p>TP53-mutated disease should prompt early specialist discussion, explicit communication of uncertainty and consideration of an appropriate clinical trial. BOVen and other response-adapted novel combinations show activity and feasibility, but available single-arm studies do not prove comparative superiority or elimination of TP53-associated risk.</p>',
  '<p>TP53-mutated disease should prompt early specialist discussion, explicit communication of uncertainty and consideration of an appropriate clinical trial. BOVen and other response-adapted novel combinations show activity and feasibility, but available single-arm studies do not prove comparative superiority or elimination of TP53-associated risk.</p>\n    '
  + figure('high-risk', 'High-risk and TP53-mutated pathway, with the evidence limits stated alongside each branch.'))

# --------------------------------------------------- B. relapsed into section 8
h = must(h,
  '<p>At each relapse, record prior regimens and classes, depth and duration of response, reason for stopping, current disease tempo, performance status, organ function, infection history and access constraints. Distinguish covalent-BTKi intolerance from progression.</p>',
  '<p>At each relapse, record prior regimens and classes, depth and duration of response, reason for stopping, current disease tempo, performance status, organ function, infection history and access constraints. Distinguish covalent-BTKi intolerance from progression.</p>\n    '
  + figure('relapsed', 'Relapsed or refractory algorithm. The branch point is prior covalent BTK-inhibitor exposure, and the cellular-therapy route carries an unresolved access position that must be confirmed before referral.'))

# ------------------------------------------------- D. access flow into section 15
h = must(h,
  '<h3>Working through the options for a patient</h3>',
  '<h3>Working through the options for a patient</h3>\n    '
  + figure('access', 'Access-route decision flow. Steps run in order; most questions resolve before step four. The individual and cohort branches diverge sharply, and the funding-request test differs in each of the four nations.'))

# ----------------------------------------- one-page quick reference in section 13
QR = """<h3>One-page quick reference</h3>
    <p>The tables that follow this summary give the reasoning. This one is the compressed form, intended to be printed and taken to clinic or MDT. Certainty and access are recorded separately and deliberately: they answer different questions and they frequently disagree.</p>
    <div class="tbl-wrap">
      <table class="qr-table">
        <caption class="sidebar-note" style="text-align:left;caption-side:bottom;padding-top:.4rem;">Certainty A to E and access class R1 to R5 are defined immediately below. Priority P1 to P4 is the practical instruction. Draft, not for clinical use — confirm every access statement against the live source.</caption>
        <thead><tr><th scope="col">Setting</th><th scope="col">Option</th><th scope="col">Certainty</th><th scope="col">England access</th><th scope="col">Priority</th></tr></thead>
        <tbody>
          <tr><td rowspan="4">First line, transplant-suitable</td><td>Cytarabine induction, ASCT, rituximab maintenance 3 years</td><td><span class="tier a">A</span></td><td>R3 guideline-supported</td><td><span class="pri">P1</span></td></tr>
          <tr><td>TRIANGLE ibrutinib regimen</td><td><span class="tier a">A</span></td><td>R4 licensed, company scheme</td><td><span class="pri">P3</span></td></tr>
          <tr><td>Rituximab maintenance in a TRIANGLE pathway</td><td><span class="tier d">D</span></td><td>R3</td><td><span class="pri">P2</span></td></tr>
          <tr><td>Obinutuzumab substituted for rituximab</td><td><span class="tier d">D</span></td><td>R5 no licence</td><td><span class="pri">P4</span></td></tr>
          <tr><td rowspan="6">First line, older or transplant-ineligible</td><td>Bendamustine–rituximab, then maintenance ≥2 years</td><td><span class="tier b">B</span></td><td><strong>R1 routine — policy 17088P, off-label</strong></td><td><span class="pri">P1</span></td></tr>
          <tr><td>VR-CAP</td><td><span class="tier a">A</span></td><td>R1 routine — TA370</td><td><span class="pri">P2</span></td></tr>
          <tr><td>R-BAC</td><td><span class="tier c">C</span></td><td>R3 guideline-supported</td><td><span class="pri">P2</span></td></tr>
          <tr><td>Acalabrutinib with bendamustine–rituximab</td><td><span class="tier a">A</span></td><td>R4 licensed, company scheme</td><td><span class="pri">P3</span></td></tr>
          <tr><td>Adding bortezomib to BR, or lenalidomide to maintenance</td><td><span class="tier a">A</span></td><td>—</td><td><span class="pri">P4</span></td></tr>
          <tr><td>Ibrutinib with BR (SHINE), or ibrutinib–rituximab (ENRICH)</td><td><span class="tier a">A</span></td><td>R5 no route</td><td><span class="pri">P4</span></td></tr>
          <tr><td rowspan="3">TP53-mutated</td><td>Trial referral</td><td><span class="tier g">G</span></td><td>R3</td><td><span class="pri">P1</span></td></tr>
          <tr><td>Anti-CD20 with BTK and BCL2 inhibition, first line</td><td><span class="tier c">C</span></td><td>R5 no licence</td><td><span class="pri">P4</span></td></tr>
          <tr><td>MRD-guided cessation</td><td><span class="tier b">B</span></td><td>R5</td><td><span class="pri">P4</span></td></tr>
          <tr><td rowspan="8">Relapsed or refractory</td><td>Ibrutinib or zanubrutinib after exactly one line</td><td><span class="tier b">B</span></td><td>R1 routine — TA502, TA1081</td><td><span class="pri">P2</span></td></tr>
          <tr><td>Brexucabtagene autoleucel after ≥2 lines incl. BTKi</td><td><span class="tier c">C</span></td><td><strong>R2 CDF — review at appeal</strong></td><td><span class="pri">P2</span></td></tr>
          <tr><td>Pirtobrutinib after covalent BTKi</td><td><span class="tier c">C</span></td><td>R4 licensed, no route</td><td><span class="pri">P3</span></td></tr>
          <tr><td>Lisocabtagene maraleucel</td><td><span class="tier c">C</span></td><td>R4 licensed, no route</td><td><span class="pri">P3</span></td></tr>
          <tr><td>Lenalidomide monotherapy</td><td><span class="tier c">C</span></td><td>R4 licensed, no route</td><td><span class="pri">P3</span></td></tr>
          <tr><td>Ibrutinib with venetoclax</td><td><span class="tier a">A</span></td><td>R5 no MCL licence</td><td><span class="pri">P4</span></td></tr>
          <tr><td>Glofitamab — GLOBRYTE trial</td><td><span class="tier c">C</span></td><td>R5 trial only</td><td><span class="pri">P4</span></td></tr>
          <tr><td>Sonrotoclax — CELESTIAL-RRMCL trial</td><td><span class="tier c">C</span></td><td>R5 trial only</td><td><span class="pri">P4</span></td></tr>
        </tbody>
      </table>
    </div>
    <div class="changed"><strong>Three lines to carry in your head</strong>
      <p>Bendamustine–rituximab is routinely commissioned in first line and is <em>off-label</em> — NHS England policy 17088P says so itself. Commissioning and licensing are not the same thing and can point in opposite directions.</p>
      <p>The two first-line company schemes divide on transplant eligibility, in opposite directions: acalabrutinib–bendamustine–rituximab is licensed for patients <strong>not</strong> eligible for ASCT, the TRIANGLE regimen for those who <strong>are</strong>.</p>
      <p>Brexucabtagene autoleucel is the only cellular therapy with an England route, and that route is currently under challenge at appeal. Confirm before you promise.</p>
    </div>
    <h3>How the classifications are assigned</h3>"""

h = must(h, '<h3>How the classifications are assigned</h3>', QR)

# ------------------------------------- reword the algorithm-not-regenerated note
h = must(h,
  '<p>The published v2.0 diagram is deliberately not displayed here. It encodes the v2.0 statements on the NICE positions for the TRIANGLE regimen, pirtobrutinib and brexucabtagene autoleucel, three of which this draft has corrected or withdrawn. Displaying it beside the corrected text would put a contradiction in front of the reader.</p>\n      <p>Regeneration is a required step before ratification, through the single node model that generates the SVG and the Excalidraw scene together, followed by the parity test. Until then there is no v2.1 algorithm.</p>',
  '<p>The published v2.0 diagram is deliberately not displayed here. It encodes the v2.0 statements on the NICE positions for the TRIANGLE regimen, pirtobrutinib and brexucabtagene autoleucel, three of which this draft has corrected or withdrawn. Displaying it beside the corrected text would put a contradiction in front of the reader.</p>\n      <p><strong>Four new pathway diagrams are embedded in this draft</strong> — first line in section 5, high-risk in section 7, relapsed or refractory in section 8, and the access-route flow in section 15. They are inline SVG generated from a single node model, so the draft remains one self-contained file with no external artefact to fall out of step.</p>\n      <p>They do <strong>not</strong> replace the release artefacts. Before ratification the downloadable SVG and the editable Excalidraw scene must both be regenerated from that same node model and put through the parity test, so that the editable copy cannot drift from the published one — the defect the earlier comparison found in the CLL package. Until that is done there is no downloadable v2.1 algorithm.</p>')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
