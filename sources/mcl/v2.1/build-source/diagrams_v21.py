#!/usr/bin/env python3
"""Generate the v2.1 inline SVG pathway diagrams from a single node model.

One model per diagram; the SVG is derived from it. Text is wrapped here rather
than relying on renderer behaviour, and every box height is computed from its
own content so nothing overflows.
"""
import textwrap

NAVY = '#1B2A4A'
RED = '#C41E3A'
PAPER = '#F7F8FA'
INK = '#172033'
LINE = '#D7DCE2'
MUTED = '#5B6472'
G_GREEN = '#2e6b3e'
G_AMBER = '#8a6410'  # WCAG 1.4.3: 5.37:1 on white, 5.07:1 on #fdf8ee (was #b08538 at 3.36:1)
G_RED = '#8b2e2e'
G_GREY = '#707070'
PANEL = '#eef2f7'

TITLE_SIZE = 12.5
BODY_SIZE = 11.0
TITLE_CW = 6.95
BODY_CW = 5.72
LINE_H = 14.5
PAD_X = 11
PAD_TOP = 17
PAD_BOT = 12


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def wrap(text, width_px, cw):
    n = max(8, int(width_px / cw))
    return textwrap.wrap(text, n) or ['']


class Box:
    """A single node. Height is computed from wrapped content."""

    def __init__(self, x, y, w, title, lines=None, kind='option', access=None):
        self.x, self.y, self.w = x, y, w
        self.title, self.kind, self.access = title, kind, access
        self.lines = lines or []
        inner = w - 2 * PAD_X
        self.tw = wrap(title, inner, TITLE_CW) if title else []
        self.bw = []
        for ln in self.lines:
            self.bw.extend(wrap(ln, inner, BODY_CW))
        self.h = PAD_TOP + len(self.tw) * (LINE_H + 1.5) + len(self.bw) * LINE_H + PAD_BOT
        if access:
            self.h += LINE_H + 3

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def bottom(self):
        return self.y + self.h

    def svg(self):
        fill, stroke, tcol, bcol, sw = 'white', LINE, NAVY, INK, 1
        if self.kind == 'start':
            fill, stroke, tcol, bcol, sw = NAVY, NAVY, 'white', '#dfe6f2', 1
        elif self.kind == 'decision':
            fill, stroke, sw = '#fdf8ee', G_AMBER, 2
        elif self.kind == 'warn':
            fill, stroke, tcol, sw = '#fff1f3', RED, '#8b2e2e', 2
        elif self.kind == 'note':
            fill, stroke, bcol = PANEL, LINE, MUTED
        out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="%s" stroke="%s" stroke-width="%d"/>'
               % (self.x, self.y, self.w, self.h, fill, stroke, sw)]
        ty = self.y + PAD_TOP
        for ln in self.tw:
            out.append('<text x="%.1f" y="%.1f" font-family="Arial,Helvetica,sans-serif" font-size="%.1f" font-weight="700" fill="%s">%s</text>'
                       % (self.x + PAD_X, ty, TITLE_SIZE, tcol, esc(ln)))
            ty += LINE_H + 1.5
        for ln in self.bw:
            out.append('<text x="%.1f" y="%.1f" font-family="Arial,Helvetica,sans-serif" font-size="%.1f" fill="%s">%s</text>'
                       % (self.x + PAD_X, ty, BODY_SIZE, bcol, esc(ln)))
            ty += LINE_H
        if self.access:
            label, colour = self.access
            out.append('<circle cx="%.1f" cy="%.1f" r="4.6" fill="%s"/>' % (self.x + PAD_X + 4.6, ty - 4, colour))
            out.append('<text x="%.1f" y="%.1f" font-family="Arial,Helvetica,sans-serif" font-size="%.1f" font-weight="700" fill="%s">%s</text>'
                       % (self.x + PAD_X + 15, ty, 10.5, colour, esc(label)))
        return '\n'.join(out)


def arrow(x1, y1, x2, y2, label=None, colour=NAVY):
    s = ['<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" marker-end="url(#ah)"/>'
         % (x1, y1, x2, y2, colour)]
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        w = len(label) * 5.6 + 10
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="15" rx="7" fill="white" stroke="%s"/>'
                 % (mx - w / 2, my - 8, w, LINE))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="%s">%s</text>'
                 % (mx, my + 3.5, colour, esc(label)))
    return '\n'.join(s)


def elbow(x1, y1, x2, y2, label=None):
    """Down, across, down."""
    midy = y1 + (y2 - y1) / 2
    s = ['<path d="M %.1f %.1f V %.1f H %.1f V %.1f" fill="none" stroke="%s" stroke-width="2" marker-end="url(#ah)"/>'
         % (x1, y1, midy, x2, y2, NAVY)]
    if label:
        w = len(label) * 5.6 + 10
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="15" rx="7" fill="white" stroke="%s"/>'
                 % ((x1 + x2) / 2 - w / 2, midy - 7.5, w, LINE))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="%s">%s</text>'
                 % ((x1 + x2) / 2, midy + 4, NAVY, esc(label)))
    return '\n'.join(s)


def document(width, height, tid, title, desc, parts):
    """Marker ids are namespaced per diagram — a document-wide id must be unique."""
    out = _document(width, height, tid, title, desc, parts)
    return out.replace('id="ah"', 'id="%s-ah"' % tid).replace('url(#ah)', 'url(#%s-ah)' % tid)


def _document(width, height, tid, title, desc, parts):
    return ('<svg class="pathway" viewBox="0 0 %d %d" role="img" aria-labelledby="%s-t %s-d" '
            'xmlns="http://www.w3.org/2000/svg">\n'
            '<title id="%s-t">%s</title>\n<desc id="%s-d">%s</desc>\n'
            '<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7.5" refY="3.2" orient="auto">'
            '<path d="M0,0 L0,6.4 L7.5,3.2 z" fill="%s"/></marker></defs>\n'
            '<rect width="%d" height="%d" fill="%s"/>\n%s\n</svg>'
            % (width, height, tid, tid, tid, esc(title), tid, esc(desc), NAVY, width, height, PAPER,
               '\n'.join(parts)))


def col_header(x, y, w, text, colour=NAVY):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="26" rx="6" fill="%s"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            'font-size="12" font-weight="700" fill="white">%s</text>'
            % (x, y, w, colour, x + w / 2, y + 17.5, esc(text)))


# =========================================================== A. FIRST LINE
def diagram_first_line():
    W = 1020
    p = []
    start = Box(310, 14, 400, 'Confirmed mantle cell lymphoma, treatment indicated',
                ['Diagnosis integrated on morphology, immunophenotype and cyclin D1 or a '
                 'CCND-family rearrangement. Record Ki-67 and TP53 before planning.'], 'start')
    p.append(start.svg())
    dec = Box(285, start.bottom + 34, 450, 'Is the patient suitable for dose-intensive treatment and ASCT?',
              ['Decide on biological risk, treatment requirement, physiological fitness and '
               'transplant suitability — not chronological age alone.',
               'The two first-line licensed populations divide at this same point.'], 'decision')
    p.append(arrow(start.cx, start.bottom, dec.cx, dec.y - 4))
    p.append(dec.svg())

    ly, ry = dec.bottom + 46, dec.bottom + 46
    LX, RX, CW = 24, 528, 468
    p.append(col_header(LX, ly, CW, 'Transplant-suitable  ·  see section 6'))
    p.append(col_header(RX, ry, CW, 'Older or transplant-ineligible  ·  see section 7'))
    p.append(elbow(dec.cx - 90, dec.bottom, LX + CW / 2, ly - 4, 'suitable'))
    p.append(elbow(dec.cx + 90, dec.bottom, RX + CW / 2, ry - 4, 'not suitable'))
    ly += 40
    ry += 40

    left = [
        Box(LX, ly, CW, 'Rituximab with high-dose cytarabine induction, ASCT, then rituximab maintenance 3 years',
            ['Bundled strategy — MCL Younger does not isolate the effect of ASCT. '
             'LYMA maintenance improved 4-year EFS, PFS and OS; the long-term OS difference was not significant.'],
            'option', ('Guideline-supported conventional practice', G_AMBER)),
        Box(LX, 0, CW, 'TRIANGLE regimen — ibrutinib with R-CHOP alternating R-DHAP or R-DHAOx, then ibrutinib',
            ['GB licence covers previously untreated patients who WOULD BE ELIGIBLE for ASCT.',
             'Adding ASCT gave no failure-free survival gain; ibrutinib arms improved OS and increased '
             'grade 3-5 infection. Do not add ASCT merely because the patient was eligible.',
             'NICE appraisal in development. Draft guidance of 30 June 2026 says the regimen should not be '
             'used. This is draft, not final guidance, and creates no funding mandate. Owner-attested '
             'company scheme — see section 17.'],
            'option', ('Licensed; no routine route; company scheme', G_RED)),
    ]
    right = [
        Box(RX, ry, CW, 'Bendamustine with rituximab, then rituximab maintenance at least 2 years',
            ['Routinely commissioned under NHS England policy 17088P for patients unable to tolerate '
             'more intensive treatment, performance status 0-1, up to six cycles.',
             'That policy states plainly that BR is not a licensed medicine for this indication — '
             'commissioned and off-label at the same time.'],
            'option', ('Routine NHS England commissioning', G_GREEN)),
        Box(RX, 0, CW, 'VR-CAP',
            ['Improved PFS versus R-CHOP with more neutropenia and thrombocytopenia. '
             'TA370 recommends within the marketing authorisation. Do not generalise to transplant-suitable patients.'],
            'option', ('Routine NHS England commissioning', G_GREEN)),
        Box(RX, 0, CW, 'R-BAC',
            ['Single-arm long-term data in untreated older patients: complete response 91%, 7-year PFS 55%. '
             'No randomised comparison against BR; greater haematological toxicity; no maintenance given.'],
            'option', ('Guideline-supported conventional practice', G_AMBER)),
        Box(RX, 0, CW, 'Acalabrutinib with bendamustine and rituximab',
            ['GB licence covers previously untreated patients NOT ELIGIBLE for ASCT.',
             'ECHO showed a PFS benefit without a demonstrated OS advantage. NICE draft guidance of '
             '25 February 2026 did not recommend it; the appraisal was rescheduled.',
             'An NHS network pathway records this as available via an owner-attested early access programme — see section 17.'],
            'option', ('Licensed; no routine route; company scheme', G_RED)),
    ]

    def stack(boxes, y0):
        y = y0
        prev = None
        for b in boxes:
            b.y = y
            p.append(b.svg())
            if prev is not None:
                p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5" stroke-dasharray="4 4"/>'
                         % (b.cx, prev.bottom, b.cx, b.y, LINE))
            prev = b
            y = b.bottom + 16
        return y

    ly2 = stack(left, ly)
    ry2 = stack(right, ry)

    warn_y = max(ly2, ry2) + 12
    w1 = Box(LX, warn_y, CW, 'Do not add to a bendamustine–rituximab platform',
             ['E1411 randomised 373 previously untreated patients. Adding bortezomib to induction did not '
              'improve PFS (HR 0.90). Adding lenalidomide to rituximab maintenance did not improve PFS (HR 0.84). '
              'Both randomised questions were negative at 7.5 years.'], 'warn')
    p.append(w1.svg())
    w2 = Box(RX, warn_y, CW, 'TP53 mutation changes the conversation, not just the prognosis',
             ['Assess TP53 before treatment planning wherever feasible. If mutated, move to the high-risk '
              'pathway and discuss trial entry early — see section 8.'], 'warn')
    p.append(w2.svg())

    foot_y = max(w1.bottom, w2.bottom) + 16
    foot = Box(LX, foot_y, CW + CW + 36, 'Access is a separate determination from evidence',
               ['A regimen with strong randomised evidence may still have no commissioned route, and a '
                'routinely commissioned regimen may be off-label. Confirm the marketing authorisation, the '
                'NICE position and the commissioning route separately before treating. Section 17 sets out '
                'the non-routine routes, including company early access schemes and the four-nation funding tests.'],
               'note')
    p.append(foot.svg())
    H = int(foot.bottom + 18)
    return document(W, H, 'algo-1l', 'First-line treatment algorithm for mantle cell lymphoma',
                    'Decision flow from confirmed diagnosis through transplant-eligibility assessment to '
                    'first-line options, split into transplant-suitable and older or transplant-ineligible '
                    'branches, each option labelled with its England access class.', p)


# ====================================================== B. RELAPSED / REFRACTORY
def diagram_relapsed():
    W = 1020
    p = []
    start = Box(210, 14, 600, 'Relapse or progression confirmed',
                ['Record prior regimens and classes, depth and duration of response, reason for stopping, '
                 'disease tempo, organ function, infection history and access constraints. '
                 'Re-biopsy where transformation is suspected.'], 'start')
    p.append(start.svg())
    dec = Box(235, start.bottom + 32, 550, 'Has the patient already had a covalent BTK inhibitor?',
              ['Distinguish intolerance from progression — the two lead to different places. '
               'Intolerance may permit a within-class switch; progression does not.'], 'decision')
    p.append(arrow(start.cx, start.bottom, dec.cx, dec.y - 4))
    p.append(dec.svg())

    y = dec.bottom + 46
    LX, RX, CW = 24, 528, 468
    p.append(col_header(LX, y, CW, 'BTK-inhibitor naive'))
    p.append(col_header(RX, y, CW, 'Progression on a covalent BTK inhibitor'))
    p.append(elbow(dec.cx - 100, dec.bottom, LX + CW / 2, y - 4, 'no'))
    p.append(elbow(dec.cx + 100, dec.bottom, RX + CW / 2, y - 4, 'yes'))
    y += 40

    left = [
        Box(LX, y, CW, 'After exactly one previous line — ibrutinib or zanubrutinib',
            ['TA1081 directs use of the least expensive of the suitable treatments, naming zanubrutinib '
             'and ibrutinib, after discussion of advantages and disadvantages with the patient.',
             'TA502 covers ibrutinib after one previous line. Both subject to their commercial arrangements '
             'and live Blueteq criteria. Intolerance transfer requires absence of progression.'],
            'option', ('Routine NHS England commissioning', G_GREEN)),
        Box(LX, 0, CW, 'Acalabrutinib monotherapy',
            ['GB-licensed for relapsed or refractory disease not previously treated with a BTK inhibitor. '
             'NICE GID-TA11470 awaiting development, timelines to be confirmed. No national route.'],
            'option', ('Licensed; no demonstrated routine route', G_RED)),
        Box(LX, 0, CW, 'Plan the next line before you need it',
            ['Median survival after stopping first-line ibrutinib in the England COVID-scheme cohort was '
             '1.4 months — 8.6 months where subsequent treatment was given, 0.6 months where it was not. '
             'Identify the next option and assess cellular-therapy eligibility early.'], 'warn'),
    ]
    right = [
        Box(RX, y, CW, 'Assess cellular-therapy eligibility and refer early',
            ['Manufacturing time and bridging risk are part of the decision. UK intention-to-treat data '
             'record material attrition between approval and infusion, and 24-month non-relapse mortality '
             'of 25%, mainly infection.'], 'option', ('Assessment step', G_GREY)),
        Box(RX, 0, CW, 'Brexucabtagene autoleucel',
            ['ZUMA-2 cohort 1: median duration of response 36.5 months at 67.8 months follow-up. '
             'Cohort 3 in BTKi-naive disease: response 91%, complete response 73%.',
             'TA677 managed access remains live, forms KTE01a and KTE01b. The June 2026 appeal was upheld in '
             'part and the appraisal was remitted to committee. No final review guidance has been issued. '
             'Confirm live CDF and Blueteq eligibility before referral.'],
            'option', ('Managed access — CDF; post-review position unresolved', G_AMBER)),
        Box(RX, 0, CW, 'Pirtobrutinib',
            ['BRUIN: response 57.8%, median duration of response 21.6 months. Single-arm.',
             'Official NICE status is internally inconsistent — see the access matrix. A second appraisal '
             'covers a BTKi-untreated population. A registered individual-patient expanded access '
             'programme exists. Do not transpose the CLL route — that is a different indication.'],
            'option', ('Licensed; no demonstrated routine route', G_RED)),
        Box(RX, 0, CW, 'Lisocabtagene maraleucel',
            ['Phase I: response 83.1% among 88 infused. GB-licensed after at least two lines including a '
             'BTK inhibitor. NICE GID-TA11930 awaiting development. No head-to-head against brexu-cel.'],
            'option', ('Licensed; no demonstrated routine route', G_RED)),
        Box(RX, 0, CW, 'Trial routes — often the only route',
            ['GLOFITAMAB: no GB mantle cell licence. GLOBRYTE phase III recruiting at Glasgow, Lincoln, '
             'London, Manchester, Oxford and Plymouth.',
             'SONROTOCLAX: US-approved May 2026, no GB licence. CELESTIAL-RRMCL phase III recruiting at '
             'Glasgow, Oxford, Wirral, Plymouth, Bournemouth and London.',
             'Both are randomised, so a patient may receive the comparator. Say so at consent.'],
            'option', ('Clinical trial', G_GREY)),
        Box(RX, 0, CW, 'After CAR-T failure — the pathway does not stop here',
            ['EBMT 2026 guidance: no role for repeat CD19-directed CAR-T once CAR-T-exposed.',
             'ALLOGENEIC HCT is a clinical option in salvage-sensitive patients. It is the only remaining '
             'modality with curative intent, evidence is limited and largely extrapolated from large '
             'B-cell lymphoma, and outcomes in this heavily pretreated group are poor. Discuss with a '
             'transplant centre before CAR-T, not after it fails.',
             'Bispecific antibody or trial entry are the alternatives — 26% of patients in the '
             'mosunetuzumab with polatuzumab study had prior CAR-T.'],
            'option', ('Trial or specialist transplant decision', G_GREY)),
    ]

    def stack(boxes, y0):
        yy = y0
        prev = None
        for b in boxes:
            b.y = yy
            p.append(b.svg())
            if prev is not None:
                p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5" stroke-dasharray="4 4"/>'
                         % (b.cx, prev.bottom, b.cx, b.y, LINE))
            prev = b
            yy = b.bottom + 16
        return yy

    ly = stack(left, y)
    ry = stack(right, y)
    fy = max(ly, ry) + 8
    f1 = Box(LX, fy, CW * 2 + 36, 'Do not rank these options against one another',
             ['No head-to-head randomised comparison exists between pirtobrutinib, cellular therapy, '
              'bispecific antibodies and BCL2 inhibition. Unadjusted cross-trial response rates must not be '
              'used to construct a hierarchy.',
              'Ibrutinib with venetoclax has randomised phase III evidence in this setting — median PFS 31.9 '
              'versus 22.1 months, hazard ratio 0.65 (CORRECTION_UNRESOLVED: a published correction exists '
              'against this report and its content has not been retrieved) — and no GB mantle cell licence '
              'and no route. Strong evidence and no access are not a contradiction; record them separately.'], 'warn')
    p.append(f1.svg())
    H = int(f1.bottom + 18)
    return document(W, H, 'algo-rr', 'Relapsed or refractory treatment algorithm for mantle cell lymphoma',
                    'Decision flow from confirmed relapse, branching on prior covalent BTK-inhibitor exposure, '
                    'through commissioned options, cellular therapy, licensed options without a route, and '
                    'trial routes, each labelled with its England access class.', p)


# =============================================================== C. HIGH RISK
def diagram_high_risk():
    W = 1020
    p = []
    start = Box(260, 14, 500, 'Risk assessment before treatment planning',
                ['Assess TP53 status wherever technically feasible, alongside morphology, Ki-67 by an agreed '
                 'reproducible method, and a clinical risk score.'], 'start')
    p.append(start.svg())
    y = start.bottom + 34
    LX, MX, RX, CW = 24, 356, 688, 308
    p.append(col_header(LX, y, CW, 'TP53 mutated'))
    p.append(col_header(MX, y, CW, 'Other adverse features'))
    p.append(col_header(RX, y, CW, 'Standard risk'))
    for cx in (LX + CW / 2, MX + CW / 2, RX + CW / 2):
        p.append(elbow(start.cx, start.bottom, cx, y - 4))
    y += 40

    a = Box(LX, y, CW, 'Treat as a distinct clinical problem',
            ['Early specialist discussion, explicit communication of uncertainty, and consideration of a '
             'clinical trial as the primary option rather than the fallback.'], 'option')
    p.append(a.svg())
    b = Box(LX, a.bottom + 14, CW, 'What the evidence does and does not show',
            ['Descriptive subgroup outcomes in a small, non-randomised cohort were poorer with TP53 mutation despite high response rates, suggesting the regimen may not eliminate TP53-associated risk. It does not establish an independent prognostic effect. In the first-line SYMPATICO '
             'cohort, patients aged 65 or over with TP53 mutation achieved complete response 44%, median '
             'PFS 22.0 months and 3-year OS 66%, against 76%, 40.2 months and 85% without mutation. '
             'Younger patients with TP53 mutation reached complete response 73% but median PFS 15.4 months.',
             'A high response rate with markedly shorter disease control is the pattern to expect.'], 'option')
    p.append(b.svg())
    c = Box(LX, b.bottom + 14, CW, 'The guideline recommendation you cannot deliver',
            ['The 2025 EHA-EU guideline favours first-line anti-CD20 with a BTK inhibitor and a BCL2 '
             'inhibitor. No such combination holds a GB mantle cell licence, and venetoclax is not '
             'authorised for mantle cell lymphoma in the UK, EU or US. In England this is deliverable '
             'only inside a trial.'], 'warn')
    p.append(c.svg())

    d = Box(MX, y, CW, 'Features that should raise concern',
            ['Blastoid or pleomorphic morphology. High Ki-67. High-risk clinical score. '
             'Rapid tempo or early progression. Central nervous system involvement.'], 'option')
    p.append(d.svg())
    e = Box(MX, d.bottom + 14, CW, 'Molecular risk beyond TP53',
            ['In the FIL V-RBAC biomarker analysis of 132 evaluable patients, ATM was the most frequently '
             'mutated gene at 41.7%, ahead of TP53 and KMT2D at 23.5% each; ATM deletion 24%, CDKN2A loss 22%.',
             'These are prognostic associations within one trial population. They do not yet direct '
             'treatment selection and should not be used to withhold an otherwise indicated regimen.'], 'option')
    p.append(e.svg())
    f = Box(MX, e.bottom + 14, CW, 'Prognostic models',
            ['Use molecular and pathological risk to support trial referral, treatment planning and consent. '
             'State the limitations of applying a newer model outside its validation setting.'], 'note')
    p.append(f.svg())

    g = Box(RX, y, CW, 'Proceed on the first-line pathway',
            ['Return to section 6 or section 7 according to transplant suitability.'], 'option')
    p.append(g.svg())
    hh = Box(RX, g.bottom + 14, CW, 'Observation remains appropriate for some',
            ['Selected asymptomatic patients with low-volume, indolent or non-nodal disease may be observed '
             'after diagnostic confidence and MDT review. Review every 3 to 6 months with objective triggers '
             'recorded. A rising lymphocyte count alone is not a trigger.'], 'option')
    p.append(hh.svg())
    i = Box(RX, hh.bottom + 14, CW, 'MRD',
            ['May refine prognosis and has guided cessation in protocols. It is not a validated universal '
             'surrogate and does not justify omitting effective maintenance outside a trial.'], 'note')
    p.append(i.svg())

    fy = max(c.bottom, f.bottom, i.bottom) + 14
    z = Box(LX, fy, W - 48, 'The claim to avoid',
            ['Do not state or imply that a novel regimen has neutralised high-risk biology unless comparative '
             'evidence demonstrates it. No regimen in current use has done so for TP53-mutated mantle cell '
             'lymphoma. Say this plainly to patients rather than implying that a targeted agent removes the risk.'],
            'warn')
    p.append(z.svg())
    H = int(z.bottom + 18)
    return document(W, H, 'algo-hr', 'High-risk and TP53-mutated pathway for mantle cell lymphoma',
                    'Three-branch flow from pre-treatment risk assessment covering TP53-mutated disease, '
                    'other adverse features and standard risk, with the evidence limits and the claim to avoid.', p)


# ============================================================ D. ACCESS ROUTE
def diagram_access():
    W = 1020
    p = []
    start = Box(230, 14, 560, 'A licensed treatment is clinically indicated. Is there a route?',
                ['Marketing authorisation, HTA recommendation and commissioning are three separate '
                 'determinations. Work through them in order — most access questions are answered before '
                 'the fourth step.'], 'start')
    p.append(start.svg())
    y = start.bottom + 26
    steps = [
        ('1. Is there a positive NICE technology appraisal?',
         ['If yes, funding is mandatory within 90 days of publication, or 30 days for a product that held '
          'an early-access designation or was appraised by the fast-track route. Complete the Blueteq form '
          'for the drug and indication. Stop here.'], ('Routine NHS England commissioning', G_GREEN)),
        ('2. Is it recommended for managed access?',
         ['Cancer Drugs Fund or Innovative Medicines Fund entry, with a Blueteq prior-approval form and '
          'mandatory SACT data collection. Time-limited, and the exit position matters — if NICE does not '
          'recommend at exit, the company must continue supplying existing patients at its own expense, '
          'but no new patients are funded.'], ('Managed access', G_AMBER)),
        ('3. Is there positive NICE draft guidance, and is this a cancer drug?',
         ['Interim funding runs from publication of positive draft guidance until final guidance. '
          'Note the asymmetry: a NEGATIVE draft creates no interim funding, which is exactly the window '
          'in which company schemes are used.'], ('Interim funding', G_AMBER)),
        ('4. Is there an open trial with a UK site?',
         ['For several agents in this guideline this is the only documented route. Confirm recruitment '
          'status and site activation with the principal investigator — registry records lag reality.'],
         ('Clinical trial', G_GREY)),
        ('5. Is there a company early access or free-of-charge scheme?',
         ['Ask the company and ask your chief pharmacist what agreements the trust already holds. These are '
          'not publicly listed and there is no national register. Governance: chief pharmacist approval, '
          'medicines management committee support, a written company-trust agreement with pre-specified '
          'exit arrangements, supply through pharmacy only, and consent that records that treatment stops '
          'if the company withdraws supply.'], ('Company scheme', G_RED)),
    ]
    prev_bottom = start.bottom
    prev_cx = start.cx
    for title, lines, acc in steps:
        b = Box(160, y, 700, title, lines, 'decision', acc)
        p.append(arrow(prev_cx, prev_bottom, b.cx, b.y - 4))
        p.append(b.svg())
        prev_bottom, prev_cx = b.bottom, b.cx
        y = b.bottom + 26

    dec = Box(160, y, 700, '6. No scheme. Is this one atypical patient, or a group?',
              ['This is the fork that most often goes wrong.'], 'decision')
    p.append(arrow(prev_cx, prev_bottom, dec.cx, dec.y - 4))
    p.append(dec.svg())

    y2 = dec.bottom + 44
    LX, RX, CW = 24, 528, 468
    p.append(col_header(LX, y2, CW, 'One atypical patient'))
    p.append(col_header(RX, y2, CW, 'A defined group of patients', RED))
    p.append(elbow(dec.cx - 140, dec.bottom, LX + CW / 2, y2 - 4, 'individual'))
    p.append(elbow(dec.cx + 140, dec.bottom, RX + CW / 2, y2 - 4, 'cohort'))
    y2 += 40

    l1 = Box(LX, y2, CW, 'Individual funding request — and the test differs by nation',
             ['ENGLAND: clinical exceptionality. The patient must be materially different from the typical '
              'population and likely to gain benefit a typical patient would not.',
              'SCOTLAND, PACS Tier 2: no exceptionality test. Show that SMC-accepted options were tried or '
              'are unsuitable, and that this patient will do at least as well as the population SMC '
              'considered. Arguing exceptionality weakens the application. Tier 2 also covers medicines '
              'still awaiting SMC evaluation.',
              'WALES, IPFR: limb (b), for an intervention never appraised, needs significant clinical '
              'benefit and reasonable value for money only — atypicality is not required.',
              'NORTHERN IRELAND: consultant-only application to the IFR Regional Scrutiny Committee.'], 'option')
    p.append(l1.svg())
    l2 = Box(LX, l1.bottom + 14, CW, 'Write it for the right jurisdiction',
             ['A letter drafted for an English panel argues the patient is not representative. A Scottish '
              'PACS panel is being asked the opposite. The same letter sent unaltered argues against itself.'],
             'warn')
    p.append(l2.svg())

    r1 = Box(RX, y2, CW, 'An individual funding request is the wrong instrument',
             ['NHS England policy reclassifies any request where other patients could derive similar benefit '
              'as a request for a new clinical policy. If you can name a second similar patient, the request '
              'will fail — and should.',
              'No guideline can name an individual funding request as the route for a defined population. '
              'The guideline cohort is itself proof of non-exceptionality.'], 'warn')
    p.append(r1.svg())
    r2 = Box(RX, r1.bottom + 14, CW, 'Use a cohort mechanism instead',
             ['Clinical policy development through the ICB or NHS England specialised commissioning.',
              'A free-of-charge scheme for an identified cohort, under the governance above.',
              'In Wales, One Wales for a defined cohort where use is unlicensed or off-label — decision OW09 '
              'already covers bendamustine with rituximab in mantle cell lymphoma.'], 'option')
    p.append(r2.svg())

    fy = max(l2.bottom, r2.bottom) + 14
    z = Box(LX, fy, W - 48, 'Absence of a commissioned route is not absence of access',
            ['Company early access and free-of-charge schemes are not publicly listed, there is no national '
             'register, and most UK schemes are company-run rather than run through any regulatory pathway. '
             'A null result in a public search is not evidence that no scheme exists. Ask the company and '
             'ask pharmacy before telling a patient there is nothing available.'], 'warn')
    p.append(z.svg())
    H = int(z.bottom + 18)
    return document(W, H, 'algo-access', 'Access-route decision flow for a licensed treatment without routine commissioning',
                    'Six-step sequence from NICE technology appraisal through managed access, interim funding, '
                    'trials and company schemes to funding requests, with the individual and cohort branches '
                    'separated and the differing tests in England, Scotland, Wales and Northern Ireland.', p)


DIAGRAMS = {
    'first-line': diagram_first_line,
    'relapsed': diagram_relapsed,
    'high-risk': diagram_high_risk,
    'access': diagram_access,
}

if __name__ == '__main__':
    for k, fn in DIAGRAMS.items():
        s = fn()
        open('/home/claude/dg-%s.svg' % k, 'w', encoding='utf-8').write(s)
        print('%-12s %6d bytes' % (k, len(s)))
