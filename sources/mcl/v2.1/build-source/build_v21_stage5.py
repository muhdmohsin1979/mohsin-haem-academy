#!/usr/bin/env python3
"""Stage 5: UK-source findings. NSSG corroboration of the acalabrutinib EAP,
NHS England commissioning policy for BR, devolved-nation non-routine routes,
and SMC reference corrections."""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:170])
    return html.replace(needle, repl, n)


# ---------------------------------------- NSSG corroboration into section 15
h = must(h,
  '<p>That AstraZeneca operates schemes of this kind in United Kingdom haematology is independently documented.',
  """<div class="uk"><strong>An NHS network pathway names the route in writing</strong>
      <p>The Thames Valley Network Site Specific Group front-line mantle cell lymphoma pathway (document <strong>LPW.8, version 1.3, reviewed September 2025, review due September 2027</strong>) lists <q>BR3 +/- acala (preferred)</q> as a first-line option, and its footnote 3 reads verbatim, typographical error included: <q>BR+Acalabrutinib according the ECHO trial. Avaliable via EAP.</q></p>
      <p>This is an NHS network document, published by a cancer alliance site-specific group, recording an early access programme as the route to acalabrutinib–bendamustine–rituximab in first-line disease. It corroborates the mechanism independently of any company source. It names neither the company nor the funder, and it carries no Blueteq or commissioning reference, which is what one would expect of an arrangement held under a written agreement at trust level.</p>
      <p><strong>One discrepancy to resolve locally.</strong> That pathway places <q>BR3 +/- acala (preferred)</q> in <em>both</em> the transplant-eligible and the transplant-ineligible branches. The Great Britain marketing authorisation covers only patients <strong>not eligible</strong> for autologous stem-cell transplantation. Use in a transplant-eligible patient is therefore off-label against the SmPC and needs the governance that off-label use attracts, whatever the supply route. Check the branch placement against your own network pathway before relying on it.</p>
    </div>
    <p>That AstraZeneca operates schemes of this kind in United Kingdom haematology is independently documented.""")

# ------------------------------- what NHS-side searching did and did not find
h = must(h,
  '<h3>The other two agents</h3>',
  """<h3>What NHS-side sources show for all four regimens</h3>
    <p>A second search, restricted to NHS sources — Specialist Pharmacy Service, the national Cancer Drugs Fund list, NHS England commissioning policies, network site-specific group protocol libraries, cancer alliance protocol archives, trust and regional formularies and free-of-charge policies — produced the following.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Regimen</th><th scope="col">NHS-side documentation</th><th scope="col">Route class</th></tr></thead>
        <tbody>
          <tr><td>Acalabrutinib with bendamustine–rituximab, first line</td><td><strong>Found.</strong> Thames Valley NSSG pathway LPW.8 v1.3 names an early access programme.</td><td>Company early access programme</td></tr>
          <tr><td>Ibrutinib, TRIANGLE regimen, first line</td><td><strong>Not found in any protocol library read.</strong> The only NHS document located on first-line ibrutinib in mantle cell lymphoma is the Thames Valley protocol L.38 v3.1, which records the opposite direction of travel: the COVID-era indication is <q>not commissioned for new patients</q> from 1 October 2022, with funding continuing only for patients who had Blueteq approval before that date.</td><td>Company scheme, attested but not publicly documented</td></tr>
          <tr><td>Glofitamab, relapsed or refractory</td><td><strong>Not found.</strong> Every NHS glofitamab protocol located is restricted to diffuse large B-cell lymphoma, primary mediastinal B-cell lymphoma or high-grade B-cell lymphoma. The Thames Valley protocol L.149 v3.0 records <q>EAMS closed; NICE TA published</q> and carries no mantle cell lymphoma indication.</td><td>Trial (GLOBRYTE), or an undocumented local arrangement</td></tr>
          <tr><td>Pirtobrutinib, relapsed or refractory</td><td><strong>Not found for mantle cell lymphoma.</strong> The only NHS pirtobrutinib protocol located is restricted to chronic lymphocytic leukaemia and small lymphocytic lymphoma. Note that pirtobrutinib <em>is</em> routinely funded in England for chronic lymphocytic leukaemia under TA1173; that route must not be transposed.</td><td>Registered expanded access programme, or an undocumented local arrangement</td></tr>
        </tbody>
      </table>
    </div>
    <p>Two limits on the negative findings. Large parts of the NHS formulary estate could not be read — the netFormulary platform disallows automated retrieval, several regional sites failed to resolve, and the Specialist Pharmacy Service prescribing outlook and its prior-approval standardisation content sit behind NHS authentication. And a network pathway is published only where a network chooses to publish; the Thames Valley finding surfaced only because that group publishes its pathways openly. Equivalent arrangements almost certainly exist elsewhere without leaving a public trace.</p>
    <h3>Pirtobrutinib and glofitamab — the registry position</h3>""")

# ---------------------------------- devolved nations subsection (before governance)
DEVOLVED = """<h3>Non-routine routes in Scotland, Wales and Northern Ireland</h3>
    <p>The four nations do not share a mechanism, and — this is the point most often got wrong — they do not share a <em>test</em>. A funding request drafted for one nation can argue against itself in another.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Nation</th><th scope="col">Mechanism</th><th scope="col">The test to argue</th><th scope="col">Decision-maker</th></tr></thead>
        <tbody>
          <tr><td>England</td><td>Individual funding request</td><td><strong>Clinical exceptionality.</strong> The patient must be materially different from the typical patient population. Cohorts are excluded by definition.</td><td>ICB or NHS England IFR panel</td></tr>
          <tr><td>Scotland</td><td><strong>PACS Tier 2</strong> (Peer Approved Clinical System). Covers licensed medicines not recommended by SMC, use outside an SMC restriction, and — importantly — <strong>medicines awaiting or undergoing SMC evaluation</strong>.</td><td><strong>No exceptionality test.</strong> Two limbs: that a reasonable attempt has been made to use SMC-accepted options first, and an evidence-based case that this patient will achieve benefit <q>at least comparable to if not better than</q> the population SMC considered. <strong>Arguing exceptionality actively weakens the application.</strong></td><td>Local board panel: senior physician plus senior pharmacist. Appeal to the Healthcare Improvement Scotland national review panel.</td></tr>
          <tr><td>Wales</td><td><strong>Individual patient funding request</strong>, in two limbs; plus <strong>One Wales</strong> for a defined cohort where use is unlicensed or off-label.</td><td>Limb (a), where guidance recommends against: the patient must be significantly different and gain significantly more benefit. <strong>Limb (b), where the intervention has not been appraised: significant clinical benefit and reasonable value for money only — atypicality is not required.</strong></td><td>Health board IPFR panel including two lay representatives. One Wales runs through OWMAG to health board chief executives.</td></tr>
          <tr><td>Northern Ireland</td><td>Individual funding request; NICE appraisals are separately endorsed for Health and Social Care before they apply.</td><td>Exceptionality-based. Applications may be made <strong>only by a hospital consultant</strong>.</td><td>IFR Regional Scrutiny Committee</td></tr>
        </tbody>
      </table>
    </div>
    <div class="uk"><strong>Two consequences worth acting on</strong>
      <p><strong>Scotland.</strong> Acalabrutinib with bendamustine–rituximab is under SMC consideration (SMC2929), and a medicine awaiting SMC evaluation falls squarely inside PACS Tier 2. An application can be made now. Pirtobrutinib was a non-submission (SMC2897, published 19 January 2026), which means SMC issued advice of <q>not recommended</q> without ever assessing the evidence — that is a legitimate argument to put in a PACS Tier 2 application, not an obstacle to it. Glofitamab has no mantle cell lymphoma licence, so PACS Tier 2 does not apply and the board's off-label medicines route is the correct one.</p>
      <p><strong>Wales.</strong> The TRIANGLE regimen is licensed but has never been appraised, which puts it in IPFR limb (b) — significant clinical benefit and reasonable value for money, with no requirement to show the patient is atypical. That is a materially lower bar than the English test, and a letter written for an English panel will be arguing the wrong thing. Separately, One Wales decision OW09 already supports bendamustine with rituximab in mantle cell lymphoma, issued March 2017 and last reviewed March 2026.</p>
    </div>
    <h3>Governance for a free-of-charge scheme</h3>"""

h = must(h, '<h3>Governance for a free-of-charge scheme</h3>', DEVOLVED)

# -------------------------------------------- BR card correction (major)
h = must(h,
 '<p><strong>NICE:</strong> No regimen-specific first-line MCL NICE technology appraisal was identified; this does not establish absence of local or baseline access.</p>',
 '<p><strong>NICE:</strong> No regimen-specific first-line MCL NICE technology appraisal was identified. <strong>This does not mean there is no national route.</strong> NHS England clinical commissioning policy <strong>17088P</strong> (6 July 2018) states that <q>NHS England will commission bendamustine with rituximab for first line treatment of mantle cell lymphoma in accordance with the criteria outlined in this document</q>, and classifies it as <q>Routinely Commissioned</q>. A companion policy, reference 1604, covers relapsed and refractory disease.</p>')

h = must(h,
 '<p><strong>Marketing authorisation:</strong> No single BR combination marketing-authorisation statement was verified in this work package; current component SmPCs and local protocol must be checked.</p>',
 '<p><strong>Marketing authorisation:</strong> No single BR combination marketing-authorisation statement was verified; current component SmPCs and local protocol must be checked. <strong>Note that NHS England policy 17088P states plainly that <q>BR is not a licensed medicine for this indication</q></strong> and requires providers to establish internal governance arrangements before prescribing. Routine commissioning and marketing authorisation are separate determinations, and this is a clear worked example of a routinely commissioned regimen that is off-label.</p>')

h = must(h,
 '<p><strong>England access:</strong> Use only through the current local/network SACT protocol.</p>',
 '<p><strong>England access:</strong> Routinely commissioned under NHS England policy 17088P subject to its criteria — the patient must be unable to tolerate more intensive treatment and have performance status 0 to 1, with up to six cycles of bendamustine 90 mg/m² on two days every 28 days plus rituximab 375 mg/m² on day 1, and an MDT decision. Use through the current local or network SACT protocol.</p>')

h = must(h,
 '<p><strong>Devolved nations:</strong> Nation-specific and local implementation were not audited for this generic combination pathway.</p>',
 '<p><strong>Devolved nations:</strong> In Wales, One Wales decision <strong>OW09</strong> makes bendamustine with rituximab available for previously untreated and relapsed mantle cell lymphoma in patients deemed unsuitable for anthracycline-based therapy or other appraised regimens; issued March 2017, last reviewed March 2026, recorded as off-label use. Scottish and Northern Irish implementation were not audited for this combination.</p>')

# ------------------------------------- SMC reference corrections
h = must(h,
 '<p><strong>Devolved nations:</strong> SMC2351 is interim in Scotland; Welsh handling follows TA677 managed access; an HSCNI TA677 record was located.</p>',
 '<p><strong>Devolved nations:</strong> <strong>The reference &ldquo;SMC2351&rdquo; carried in v2.0 could not be located on the SMC register on 30 July 2026 and no SMC advice for brexucabtagene autoleucel in mantle cell lymphoma was found; the reference has been withdrawn pending confirmation.</strong> Do not cite it. The brexucabtagene autoleucel advice that does exist, SMC2548 of 9 October 2023, is for B-cell precursor acute lymphoblastic leukaemia and must not be cited for mantle cell lymphoma. In Wales the AWTTC record is marked excluded due to NICE appraisal, so TA677 applies; TA677 was endorsed in Northern Ireland in March 2021.</p>')

h = must(h,
 '<p><strong>Devolved nations:</strong> SMC2909 is awaiting a decision; no national Welsh or Northern Irish MCL route was demonstrated.</p>',
 '<p><strong>Devolved nations:</strong> <strong>Correction: SMC2909 is a live submission for lisocabtagene maraleucel but its indication is large B-cell lymphoma, not mantle cell lymphoma</strong>, so it does not establish a Scottish mantle cell lymphoma route and the v2.0 entry was wrong to imply otherwise. No SMC advice for lisocabtagene maraleucel in mantle cell lymphoma was located. No national Welsh or Northern Irish route was demonstrated. Note the Great Britain licence does cover mantle cell lymphoma after at least two lines including a BTK inhibitor.</p>')

h = must(h,
 '<p><strong>Devolved nations:</strong> SMC2897 is a non-submission route; no positive national Welsh or Northern Irish MCL route was demonstrated.</p>',
 '<p><strong>Devolved nations:</strong> SMC2897, published 19 January 2026, records that pirtobrutinib <q>is not recommended for use within NHSScotland</q> following a <strong>non-submission</strong> — SMC issued advice without assessing the evidence, because the company did not submit. That distinction matters: it is not a negative clinical or cost-effectiveness finding, and it can be argued in a PACS Tier 2 application. No positive national Welsh or Northern Irish route was demonstrated.</p>')

h = must(h,
 '<p><strong>Devolved nations:</strong> SMC2929 is under consideration; no final positive Welsh or Northern Irish route was demonstrated.</p>',
 '<p><strong>Devolved nations:</strong> SMC2929 remains under consideration in Scotland, with publication and meeting dates to be confirmed. A medicine awaiting SMC evaluation falls within PACS Tier 2, so an individual application can be made in Scotland now. No final positive Welsh or Northern Irish route was demonstrated; in Wales the AWTTC record is excluded due to NICE appraisal, so the NICE outcome will govern.</p>')

# ------------------------------ CDF list version note on the brexu-cel card
h = must(h,
 '<p><strong>England access:</strong> NHS England list v1.405 retains KTE01a/KTE01b managed-access forms and national eligibility criteria.',
 '<p><strong>England access:</strong> The national Cancer Drugs Fund list retains the brexucabtagene autoleucel managed-access forms <strong>KTE01a_v1.2</strong> (leucapheresis and manufacture) and <strong>KTE01b_v1.3</strong> (infusion) with national eligibility criteria; these were confirmed against list version 1.401 dated 29 May 2026.')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
