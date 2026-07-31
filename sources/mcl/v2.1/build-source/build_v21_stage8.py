#!/usr/bin/env python3
"""Stage 8: close the society gaps.

Adds two new sections (limited-stage disease, CNS involvement), expands the
diagnosis and staging sections, and renumbers everything downstream including
in-text cross-references. New content leads with the action.
"""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:170])
    return html.replace(needle, repl, n)


# ------------------------------------------------------------- styling: action box
h = must(h, '    .qr-table td:first-child { font-weight:700; }',
"""    .do { border-left:5px solid #2e6b3e; background:#f1f7f2; padding:.7rem .95rem; margin:.85rem 0; }
    .do > strong:first-child { display:block; color:#22592f; font:700 .74rem/1.3 Arial,sans-serif; text-transform:uppercase; letter-spacing:.07em; margin-bottom:.35rem; }
    .split { border-left:5px solid #6b4d8b; background:#f6f2fa; padding:.7rem .95rem; margin:.85rem 0; }
    .split > strong:first-child { display:block; color:#513a69; font:700 .74rem/1.3 Arial,sans-serif; text-transform:uppercase; letter-spacing:.07em; margin-bottom:.35rem; }
    .qr-table td:first-child { font-weight:700; }""")

# ================================================== 1. RENUMBER cross-references
# old -> new, before any new section is inserted
XMAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 6, 6: 7, 7: 8, 8: 9, 9: 11, 10: 12,
        11: 13, 12: 14, 13: 15, 14: 16, 15: 17, 16: 18, 17: 19, 18: 20, 19: 21}


def remap(m):
    word, a = m.group(1), int(m.group(2))
    b = m.group(3)
    if b is None:
        return '%s @@%d@@' % (word, XMAP[a])
    return '%s @@%d@@ and @@%d@@' % (word, XMAP[a], XMAP[int(b)])


# Only remap prose. The SVG diagrams already carry final section numbers from
# their own node model; remapping them again would shift them a second time.
_PAT = re.compile(r'\b(sections?|Sections?) (\d{1,2})(?: and (\d{1,2}))?\b')
_parts = re.split(r'(<svg\b.*?</svg>)', h, flags=re.S)
h = ''.join(seg if seg.startswith('<svg') else _PAT.sub(remap, seg) for seg in _parts)

# heading numbers, done from the highest down so nothing collides
for old in sorted(XMAP, reverse=True):
    new = XMAP[old]
    if old == new:
        continue
    h = h.replace('<h2>%d. ' % old, '<h2>@@H%d@@. ' % new)

# nav + sidebar entries
NAV = [(19, 21, 'Release control'), (18, 20, 'Evidence references'),
       (16, 18, 'Regulatory and access matrix'), (15, 17, 'Non-routine access routes'),
       (14, 16, 'Clinical trials'), (13, 15, 'Evidence-to-recommendation model'),
       (12, 14, 'Regulatory and access boundary'), (11, 13, 'Follow-up and MDT documentation'),
       (10, 12, 'Supportive care and treatment safety'), (9, 11, 'Response assessment, MRD and maintenance'),
       (8, 9, 'Relapsed or refractory pathway'), (7, 8, 'TP53-mutated and other high-risk MCL'),
       (6, 7, 'First-line pathway for older or transplant-ineligible adults'),
       (5, 6, 'First-line pathway for younger or treatment-fit adults')]
for old, new, label in NAV:
    h = h.replace('>%d. %s</a>' % (old, label), '>@@H%d@@. %s</a>' % (new, label))

h = re.sub(r'@@H?(\d+)@@', lambda m: m.group(1), h)

# ============================================ 2. SECTION 2 — diagnosis expansion
DIAG = """<div class="do"><strong>In practice</strong>
      <p>Ask for an <strong>excision biopsy</strong> wherever a node is accessible. Send <strong>every</strong> case for expert haematopathology review, not only the difficult ones. Take <strong>hepatitis B, hepatitis C and HIV serology</strong> before any anti-CD20 antibody. Record Ki-67 with a stated method. <strong>Re-biopsy at every new line of treatment.</strong></p>
    </div>
    <h3>Getting the right tissue</h3>
    <p>An excision biopsy of a lymph node is the preferred specimen. Use a core biopsy only where no node is readily accessible. A fine-needle aspirate is not adequate to diagnose mantle cell lymphoma and should not be relied on.</p>
    <p>Send the case for expert haematopathology review. The EHA–EU guideline asks for review of all cases, not only those where the phenotype is unclear (S01, graded V, A). Store additional material fresh-frozen where your service can do so — it is the material that later molecular work depends on.</p>
    <div class="changed"><strong>Re-biopsy at each new line — this is how transformation gets found</strong>
      <p>Repeat the biopsy whenever a new line of treatment is needed, and repeat Ki-67 and TP53 testing on the new sample (S01, graded IV, B). Where mutational analysis is not available, p53 by immunohistochemistry is the fallback.</p>
      <p>This is the single mechanism by which transformation to blastoid or pleomorphic disease is detected. Treating a relapse on the biology of the original diagnostic sample means treating a disease the patient may no longer have.</p>
    </div>
    <h3>Cyclin D1-negative disease</h3>
    <p>Where the phenotype fits mantle cell lymphoma but cyclin D1 immunohistochemistry is negative, ask for FISH for <em>CCND1</em> rearrangement. If that is also negative, ask for <em>CCND2</em> and <em>CCND3</em> studies. SOX11 supports the diagnosis in this setting. Routine karyotyping adds little outside a trial.</p>
    <h3>Ki-67 and p53 — state the method, use one cut-off</h3>
    <p>Ki-67 only means something if the method and the threshold are stated. Two thresholds are in use: European sources take <strong>30%</strong> as conferring inferior prognosis, American sources <strong>50%</strong>.</p>
    <div class="split"><strong>Decision taken for this guideline</strong>
      <p>This document uses <strong>Ki-67 ≥30%</strong> as the high-risk threshold, following European practice, and records that the American threshold is 50%. Where you report or read a Ki-67 result, state which threshold is being applied — a report that says only &ldquo;high&rdquo; is not usable.</p>
      <p>Two further points from S01. Ki-67 measured on bone marrow is less reliable and should not be used for prognostication. Where only p53 immunohistochemistry is available rather than mutational analysis, use a cut-off of <strong>50%</strong> to call it positive.</p>
    </div>
    <h3>Screening before anti-CD20 treatment</h3>
    <p>Test for hepatitis B, hepatitis C and HIV before starting treatment. Every mantle cell lymphoma regimen in this guideline contains an anti-CD20 antibody, and a positive hepatitis B result changes management — it requires antiviral cover to prevent reactivation. BSH grades this 1C (S42); the EHA–EU guideline makes the same point.</p>
    <p>Neither society specifies which antiviral agent or for how long. Follow your local viral hepatitis policy and involve hepatology where the result is positive. Record the result and the action taken.</p>
    <h3>Minimum dataset</h3>"""

h = must(h, '<h3>Minimum dataset</h3>', DIAG) if '<h3>Minimum dataset</h3>' in h else h
if 'Getting the right tissue' not in h:
    # v2.0 section 2 has no h3; insert before the bullet list instead
    h = must(h,
      '  <ul>\n    <li>Record morphology, including blastoid or pleomorphic features.</li>',
      '  ' + DIAG + '\n  <ul>\n    <li>Record morphology, including blastoid or pleomorphic features.</li>')

h = must(h, '<li>Record Ki-67 using an agreed reproducible method.</li>',
            '<li>Record Ki-67 using an agreed reproducible method, and state the threshold applied.</li>\n'
            '    <li>Record hepatitis B, hepatitis C and HIV serology, and the action taken on any positive result.</li>')

# ============================================== 3. SECTION 3 — staging expansion
h = must(h,
  '<p>Use molecular and pathological risk to support trial referral, treatment planning and consent. Do not claim that a novel regimen has neutralised high-risk biology unless comparative evidence demonstrates this.</p>',
  """<p>Use molecular and pathological risk to support trial referral, treatment planning and consent. Do not claim that a novel regimen has neutralised high-risk biology unless comparative evidence demonstrates this.</p>
    <h3>Endoscopy</h3>
    <p>PET-CT does not reliably detect gastrointestinal involvement, so imaging alone does not exclude it. Consider upper gastrointestinal endoscopy where the result would change management — most often when disease looks limited and the decision rests on it.</p>
    <div class="split"><strong>Where the societies differ</strong>
      <p>The EHA–EU guideline asks for gastroscopy <em>and</em> colonoscopy with biopsies when staging suspected limited-stage disease (S01, graded V, B). BSH advises <strong>upper gastrointestinal endoscopy only</strong>, on the basis that PET-CT concordance is poor for gastric involvement but good enough for colorectal disease to make colonoscopy unnecessary in an asymptomatic patient (S42).</p>
      <p><strong>This guideline follows BSH.</strong> Perform upper gastrointestinal endoscopy; reserve colonoscopy for patients with lower gastrointestinal symptoms. Record which position you followed.</p>
    </div>
    <h3>Features that define high risk</h3>
    <p>Four things move a patient into the high-risk group, and they are not interchangeable.</p>
    <ul>
      <li><strong>TP53 mutation or deletion</strong> — the strongest single factor, and the one that should change the conversation. See the high-risk section.</li>
      <li><strong>Ki-67 ≥30%</strong> — using the threshold set out in the diagnosis section.</li>
      <li><strong>Blastoid or pleomorphic morphology</strong> — an independent adverse feature recognised by EHA, BSH and EBMT. The EBMT cellular therapy guidance (S46) notes that morphology is used as high-risk defining <em>where Ki-67 is not available</em>, so where you have both, Ki-67 takes precedence.</li>
      <li><strong>High clinical risk score</strong> — MIPI and its variants. Combined scores incorporating Ki-67 and, more recently, TP53 status (MIPI53, S03) refine this, but each should be applied within the population it was validated in.</li>
    </ul>""")

# ================================== 4. NEW SECTION 5 — limited-stage disease
LIMITED = """
  <section id="limited-stage">
    <h2>5. Limited-stage disease</h2>
    <div class="do"><strong>In practice</strong>
      <p>Between 5% and 15% of patients present with stage I or II disease. Stage it properly before deciding — PET-CT, bone marrow biopsy and upper gastrointestinal endoscopy. In genuinely low-risk stage I, <strong>observation or involved-site radiotherapy</strong> are both reasonable. Where high-risk features are present, treat as advanced disease.</p>
    </div>
    <p>This section exists because limited-stage disease is managed differently and the rest of this guideline assumes advanced disease. It rests on the EHA–EU guideline (S01), which gives four graded recommendations, and on BSH (S42). No primary trial evidence has been independently verified for this section — see the note on evidence tier below.</p>
    <h3>Staging first</h3>
    <p>Do not accept a limited stage without confirming it. Stage with PET-CT, bone marrow biopsy and endoscopy with biopsies (S01, graded II, B). Understaging is the main risk here, because the treatment decision that follows is materially less intensive.</p>
    <h3>Treatment by risk</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Presentation</th><th scope="col">Option</th><th scope="col">EHA grade</th></tr></thead>
        <tbody>
          <tr><td>Stage I, no risk factors</td><td>Observation, or involved-site radiotherapy</td><td>II, B</td></tr>
          <tr><td>Intermediate risk or tumour load</td><td>Shortened systemic therapy followed by radiotherapy may be considered</td><td>IV, B</td></tr>
          <tr><td>Stage II with high-risk features</td><td>Systemic treatment as for advanced disease</td><td>IV, B</td></tr>
        </tbody>
      </table>
    </div>
    <p>The involved-site radiotherapy dose recorded in S01 is <strong>24 to 36 Gy</strong>. Discuss every case with clinical oncology — this guideline sets the indication, not the plan.</p>
    <h3>Radiotherapy for symptom control</h3>
    <p>Low-dose palliative radiotherapy, <strong>2 Gy given twice</strong>, can relieve symptoms in very frail patients, at diagnosis or at relapse (S01). It is well tolerated, it is often forgotten, and it does not require the patient to be fit for systemic treatment.</p>
    <div class="uk"><strong>Evidence tier for this section</strong>
      <p>Everything above is <span class="tier g">G</span> — adopted from a society guideline whose underlying trial evidence this document has not independently checked. That is a weaker footing than the randomised evidence cited elsewhere in this guideline, and it is labelled rather than blended in. See the evidence-to-recommendation model.</p>
    </div>
  </section>
"""

h = must(h, '<section id="first-line-fit"', LIMITED.strip() + '\n\n<section id="first-line-fit"')

# ========================================= 5. NEW SECTION 10 — CNS involvement
CNS = """
  <section id="cns">
    <h2>10. Central nervous system involvement</h2>
    <div class="do"><strong>In practice</strong>
      <p><strong>Do not give routine CNS prophylaxis.</strong> Do not perform a lumbar puncture or craniospinal MRI unless there are neurological signs or symptoms. If CNS disease appears and the patient has never had a covalent BTK inhibitor, ibrutinib is the suggested option.</p>
    </div>
    <p>CNS involvement is uncommon — under 1% of asymptomatic patients at diagnosis (S01) — but it is asked about at almost every MDT where a patient has blastoid disease or a high Ki-67. A guideline that says nothing invites high-dose methotrexate being given without a basis.</p>
    <h3>Investigation</h3>
    <p>Lumbar puncture with cytospin and immunophenotyping, together with craniospinal MRI, is indicated <strong>only where there are concerning neurological signs or symptoms</strong> (S42). A routine lumbar puncture at diagnosis in a neurologically well patient is not advised (S01).</p>
    <p>Risk of CNS involvement is higher with high Ki-67, blastoid histology, raised LDH, worse performance status and a high clinical risk score (S42). Higher risk raises your index of suspicion; it does not by itself justify investigating an asymptomatic patient.</p>
    <h3>Prophylaxis</h3>
    <p>BSH is explicit: <q>Primary CNS prophylaxis with CNS penetrating agents in front line MCL treatment algorithms is not recommended (2C)</q> (S42). <strong>This guideline adopts that position as written.</strong> It applies to high-risk patients too — the elevated risk in blastoid or high-Ki-67 disease has not been shown to be modifiable by prophylaxis.</p>
    <h3>Treating CNS disease</h3>
    <p>Where CNS disease occurs and the patient has not previously had a covalent BTK inhibitor, BSH suggests <q>ibrutinib for CNS relapse in patients who are previously cBTKi naïve (2C)</q> (S42). The EHA–EU guideline records a covalent BTK inhibitor with venetoclax as an option in the same population (S01, graded IV, B); note that the combination has no Great Britain mantle cell lymphoma licence.</p>
    <p>CAR-T has been given to patients with CNS disease. The EBMT guidance (S46) records that response rates appear comparable to patients without CNS involvement, but that response duration is short, particularly where CNS disease is active at lymphodepletion. Discuss with the cellular therapy centre rather than assuming eligibility either way.</p>
    <div class="uk"><strong>Evidence tier for this section</strong>
      <p>These recommendations are <span class="tier g">G</span> — adopted from society guidelines without independent verification of the underlying evidence. Both BSH recommendations are themselves graded 2C, which is weak. Treat them as the best available position rather than a settled one.</p>
    </div>
  </section>
"""

h = must(h, '<section id="response-mrd"', CNS.strip() + '\n\n<section id="response-mrd"')

# ---------------------------------- nav and sidebar entries for the new sections
h = must(h, '      <a href="#first-line-fit">6. First-line pathway for younger or treatment-fit adults</a>',
            '      <a href="#limited-stage">5. Limited-stage disease</a>\n'
            '      <a href="#first-line-fit">6. First-line pathway for younger or treatment-fit adults</a>')
h = must(h, '      <a href="#response-mrd">11. Response assessment, MRD and maintenance</a>',
            '      <a href="#cns">10. Central nervous system involvement</a>\n'
            '      <a href="#response-mrd">11. Response assessment, MRD and maintenance</a>')
h = must(h, '<li><a href="#first-line-fit">6. First-line pathway for younger or treatment-fit adults</a></li>',
            '<li><a href="#limited-stage">5. Limited-stage disease</a></li>\n'
            '          <li><a href="#first-line-fit">6. First-line pathway for younger or treatment-fit adults</a></li>')
h = must(h, '<li><a href="#response-mrd">11. Response assessment, MRD and maintenance</a></li>',
            '<li><a href="#cns">10. Central nervous system involvement</a></li>\n'
            '          <li><a href="#response-mrd">11. Response assessment, MRD and maintenance</a></li>')

# --------------------------------------------------------- tier G styling + defn
h = must(h, '.tier.e { background:#707070; }',
            '.tier.e { background:#707070; } .tier.g { background:#6b4d8b; }')

h = must(h,
  '<li><span class="tier e">E</span> Conference abstract or press release only, with no peer-reviewed primary publication retrievable.</li>',
  '<li><span class="tier e">E</span> Conference abstract or press release only, with no peer-reviewed primary publication retrievable.</li>\n'
  '      <li><span class="tier g">G</span> Adopted from a society guideline recommendation, where this document has <strong>not</strong> independently verified the trial evidence underneath it. Sections 5 and 10 rest largely on this tier. It is labelled separately so that inherited consensus is never mistaken for evidence read at source.</li>')

h = re.sub(r'@@N(\\d+)@@', lambda m: m.group(1), h)

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
