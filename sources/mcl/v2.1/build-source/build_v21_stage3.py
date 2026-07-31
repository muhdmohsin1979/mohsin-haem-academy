#!/usr/bin/env python3
"""Stage 3: add section 15 'Non-routine access routes', renumber, update cards,
add S44, extend anchor nav and sidebar."""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:160])
    return html.replace(needle, repl, n)


ACCESS = """
  <section id="non-routine-access">
    <h2>15. Non-routine access routes</h2>
    <p>Sections 13 and 15 record that several options with strong evidence have no NHS England commissioning route. That is a statement about commissioning, not about availability. Medicines do reach patients through routes that sit outside routine commissioning, and a guideline that records only the commissioning position will read as though those patients cannot be treated.</p>
    <p>The mechanisms below are genuinely different from one another in who supplies the medicine, who pays for it, what governance applies and whether they can serve a defined group of patients. Conflating them is the commonest error, and it has practical consequences: an arrangement described in the notes as &ldquo;compassionate use&rdquo; when it was in fact an NHS commissioning scheme will be governed, funded and audited wrongly.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Mechanism</th><th scope="col">Who supplies</th><th scope="col">Who pays for the drug</th><th scope="col">Controlling governance</th><th scope="col">Can it serve a defined cohort?</th></tr></thead>
        <tbody>
          <tr><td>Clinical trial</td><td>Sponsor</td><td>Sponsor</td><td>REC and HRA approval; trial protocol</td><td>Yes</td></tr>
          <tr><td>MHRA Early Access to Medicines Scheme</td><td>Scientific Opinion holder</td><td>Company — supplied free of charge</td><td>MHRA Scientific Opinion, risk management plan, safety registry</td><td>Yes, within the opinion</td></tr>
          <tr><td>Company free-of-charge scheme</td><td>Company, through provider pharmacy</td><td>Company</td><td>NHS England FoC policy PRN00297; chief pharmacist and medicines management committee</td><td>Yes</td></tr>
          <tr><td>Compassionate use or named-patient supply</td><td>Company</td><td>Company</td><td><strong>Outside</strong> the scope of PRN00297; GMC unlicensed-prescribing standards; local trust governance</td><td>Individual patients only</td></tr>
          <tr><td>NHS England interim commissioning scheme</td><td>Normal NHS supply</td><td>NHS</td><td>NHS England scheme reference and Blueteq prior approval</td><td>Yes</td></tr>
          <tr><td>Interim funding during a NICE appraisal</td><td>Normal NHS supply</td><td>NHS, from the Cancer Drugs Fund budget</td><td>Applies <strong>only after positive draft guidance</strong></td><td>Yes</td></tr>
          <tr><td>Individual funding request</td><td>Normal NHS supply</td><td>NHS</td><td>NHS England IFR commissioning policy; clinical exceptionality test</td><td><strong>No</strong> — see below</td></tr>
        </tbody>
      </table>
    </div>
    <div class="changed"><strong>An individual funding request cannot be a guideline route</strong>
      <p>The NHS England IFR commissioning policy states that <q>if there is evidence that other patients with the same condition could derive a similar type and degree of benefit from the treatment, the request is really for a new development in services for that group of patients</q>, and such requests are reclassified as a request for a new clinical policy. The test is clinical exceptionality against the typical patient population, and the policy is explicit that <q>severity of a patient's condition does not in itself usually indicate exceptionality</q>.</p>
      <p>It follows that <strong>no guideline can name an individual funding request as the access route for a defined population</strong>. Writing one in is self-defeating: the existence of the guideline cohort is itself evidence of non-exceptionality. Cohort access must be pursued through clinical policy development, a managed access fund, a free-of-charge scheme or a trial.</p>
    </div>
    <h3>What was found for each agent</h3>
    <p>The four regimens most often described as reaching patients outside commissioning were checked against ClinicalTrials.gov expanded-access records, EMA compassionate-use opinions, published company access policies and the MHRA scheme lists on 30 July 2026.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Agent or regimen</th><th scope="col">What is publicly documented</th><th scope="col">Assessment</th></tr></thead>
        <tbody>
          <tr><td><strong>Pirtobrutinib</strong>, relapsed or refractory</td><td><strong>NCT05172700</strong>, an individual-patient expanded access programme sponsored by Loxo Oncology at Eli Lilly, which explicitly names mantle cell lymphoma previously treated with a covalent BTK inhibitor. No United Kingdom site is listed; requests outside the United States route through the local Lilly office. The registry status reads &ldquo;approved for marketing&rdquo;, which on ClinicalTrials.gov means the expanded-access route has been overtaken by licensure rather than that it is open.</td><td><strong>Best documented of the four.</strong> A named programme exists and covers the right population.</td></tr>
          <tr><td><strong>Glofitamab</strong>, relapsed or refractory</td><td>Roche publishes a live list of active compassionate use programmes. The glofitamab programme covers diffuse large B-cell lymphoma, transformed follicular lymphoma and primary mediastinal B-cell lymphoma. <strong>Mantle cell lymphoma is not on that list.</strong> No expanded-access record exists on ClinicalTrials.gov for glofitamab in any indication. The MHRA Early Access to Medicines Scheme opinion for glofitamab covered relapsed or refractory diffuse large B-cell lymphoma only and expired on 16 October 2023.</td><td>No published mantle cell lymphoma scheme located. The documented United Kingdom route is the GLOBRYTE trial.</td></tr>
          <tr><td><strong>Acalabrutinib with bendamustine–rituximab</strong>, first line</td><td>No expanded-access record for acalabrutinib in any indication. AstraZeneca publishes a general position on early and post-trial access to medicines dated March 2024, with a request route through its early access mailbox and local medical affairs, but names no mantle cell lymphoma programme.</td><td>No published scheme located. A generic company request route exists and could carry unpublished case-by-case supply.</td></tr>
          <tr><td><strong>TRIANGLE-derived ibrutinib regimen</strong>, first line</td><td>The only ibrutinib expanded-access record, NCT01833039, is relapsed or refractory and runs in the United States, Brazil and Puerto Rico. The published pre-approval access list of the manufacturer does not include ibrutinib. <strong>What is documented in England is something different — see below.</strong></td><td>Not supported as compassionate or free-of-charge access. Most likely conflated with the NHS England interim scheme described below.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="uk"><strong>First-line ibrutinib in England was an NHS commissioning scheme, not compassionate use</strong>
      <p>From March 2020, NHS England approved ibrutinib with or without rituximab in England as an option instead of immunochemotherapy for patients with untreated mantle cell lymphoma, as part of the interim treatment options introduced during the COVID-19 pandemic. That is NHS commissioning with a scheme reference, not company supply, and it should never be recorded in the notes as compassionate use.</p>
      <p>The resulting cohort is real United Kingdom first-line covalent BTK-inhibitor data and is worth reading on its own terms (S44). One hundred and forty-nine patients from 43 English centres, median age 75, 92.2% not transplant candidates, 36.2% high-risk, and only 39.0% given rituximab. Overall response was 71.2% and complete response 20.2%. Median progression-free survival was 26.0 months overall, but 13.7 months in high-risk disease against not reached in low-risk. Grade 3 or higher toxicity occurred in 20.3% and 8.1% stopped for toxicity.</p>
      <p><strong>The figure to carry into a consent discussion is the last one.</strong> Median survival after stopping ibrutinib was 1.4 months — 8.6 months in the 41.9% who received any subsequent treatment against 0.6 months in those who did not. First-line continuous covalent BTK inhibition in an older population leaves a very narrow window at progression, and a patient choosing it should understand that.</p>
    </div>
    <h3>Governance for a free-of-charge scheme</h3>
    <p>Where a company scheme is used for a group of patients in England, the controlling document is the NHS England policy on free-of-charge medicines schemes. Its requirements are not administrative detail; several of them are the difference between a defensible arrangement and an indefensible one.</p>
    <ul>
      <li><strong>Definition.</strong> An arrangement where a licensed or unlicensed medicine is provided free of charge by a pharmaceutical company to an individual patient or an identified cohort. Heavily discounted supply is included.</li>
      <li><strong>Supply route.</strong> <q>All supplies of FOC medicines must be processed through the provider pharmacy departments to ensure appropriate governance standards are in place.</q> Never direct to a clinician or a patient.</li>
      <li><strong>Approval.</strong> Chief pharmacist sign-off, with the medicines management committee supporting suitability before any patient is offered treatment.</li>
      <li><strong>Written agreement</strong> covering the clinical criteria and unmet need, patient information, any data collection (non-identifiable only), labelling and storage, the length and scope of the agreement, <strong>exit arrangements if the medicine is not approved or approval is delayed beyond the scheme</strong>, and the position if patients do not meet the criteria eventually set by NICE or the commissioner.</li>
      <li><strong>Continuity.</strong> <q>In principle, all FOC supplies must continue until the medicine is commissioned and funding is in place.</q> Where NICE recommends, free supply stops at the funding date, not the publication date — mind the 90-day gap.</li>
      <li><strong>Consent.</strong> The policy requires that <q>the patient must be made aware and understand that treatment with the FOC medicine will be stopped if the medicine is no longer provided free of charge by the pharmaceutical company, even if the patient perceives they have had benefit from treatment.</q> Document this explicitly.</li>
      <li><strong>Scope.</strong> The policy expressly excludes compassionate use supplies, patient access schemes and the Early Access to Medicines Scheme. An individual compassionate supply therefore sits outside this framework and needs its own local governance.</li>
    </ul>
    <p>Two further points that are easy to miss. A widely used regional policy states that the Government Master Indemnity Agreement does not relate to free-of-charge medicines, so indemnity should be confirmed with the trust legal and risk team rather than assumed; this is regional rather than national policy and the national document contains no express indemnity clause. And the industry code of practice contains no clause specifically governing free-of-charge supply to the NHS — the applicable provisions are those on promotion before authorisation, on inducements, on samples and on donations. Company samples must never be used as a substitute for a properly constituted scheme.</p>
    <h3>Two mechanisms that do not currently help in mantle cell lymphoma</h3>
    <p><strong>Early Access to Medicines Scheme.</strong> No scientific opinion has been granted for mantle cell lymphoma at any point in the scheme's history, and no lymphoma medicine holds a current opinion. The scheme is worth re-checking when a new agent approaches licensing, because an EAMS designation also shortens the NHS funding requirement from 90 days to 30 days if NICE subsequently recommends.</p>
    <p><strong>Innovative Licensing and Access Pathway.</strong> A development-support designation that coordinates regulatory and access planning. It is not a licence, not a funding decision and confers no route to treatment for an individual patient. No lymphoma product holds an Innovation Passport under the reformed pathway. Do not cite it as an access route.</p>
    <div class="changed"><strong>Cellular therapy — the exit clause is the safeguard</strong>
      <p>The Cancer Drugs Fund standard operating procedure provides that where NICE does not recommend a drug at the end of managed access, funding from the Fund ceases on publication of final guidance, and that <q>any patient in receipt of the Drug will continue to receive it at [drug company]'s expense until the treating clinician will determine treatment of that patient is no longer clinically appropriate</q>. That is a contractual obligation on the company, and it is the mechanism behind the continuation safeguard described in the Government answer of 26 January 2026 in relation to brexucabtagene autoleucel. It protects patients already treated. It does not create access for new patients.</p>
    </div>
    <h3>Working through the options for a patient</h3>
    <ol>
      <li>Check the NICE position first. If a cancer drug has <em>positive</em> draft guidance, interim funding already applies and nothing further is needed.</li>
      <li>Check whether a Blueteq form exists for the drug and indication. If it does, that is the commissioned route.</li>
      <li>Check for an open trial with a United Kingdom site — see section 14. For glofitamab and sonrotoclax this is currently the only documented route.</li>
      <li>For a defined group with no route, this is a clinical policy or free-of-charge scheme question. Take it to pharmacy and the medicines management committee, not to an individual funding request.</li>
      <li>For a genuinely atypical single patient, an individual funding request may be appropriate. Build the exceptionality case explicitly against the typical population and supply full copies of the cited papers. If a second similar patient can be named, it will fail, and it should.</li>
      <li>Ask the company directly. Every manufacturer of the agents in this guideline publishes a pre-approval or early access request route, and named-patient supply is arranged case by case through medical affairs. Route any resulting supply through pharmacy under the governance above.</li>
    </ol>
    <div class="draft-banner" style="border-width:2px;">
      <strong>What this section can and cannot tell you</strong>
      <p>Absence of a public record does not mean a scheme does not exist. Only programmes intended for groups of patients are reliably registered; individual named-patient and single-patient free-of-charge supply is almost never registered anywhere. Published work using freedom-of-information requests to acute trusts has found that most United Kingdom schemes are company-led rather than run through the Early Access to Medicines Scheme, that no central national database of available schemes exists, and that more than half of the trusts approached held no centralised record of their own schemes. NHS England's own free-of-charge policy places compassionate use outside its scope, so those arrangements are not captured there either.</p>
      <p>An arrangement made directly between a treating consultant and a company's medical affairs team is therefore invisible to every source searched for this section. A clinician reporting local access to acalabrutinib–bendamustine–rituximab or to a TRIANGLE-derived regimen on a compassionate or free-of-charge basis is <strong>entirely consistent</strong> with the null findings recorded above. This guideline states what is publicly documented; it does not assert that undocumented arrangements do not exist. Confirm the position locally with pharmacy and with the company before concluding that a patient has no option.</p>
    </div>
  </section>
"""

anchor = '  <section id="access-status">'
h = must(h, anchor, ACCESS + anchor)

# ------------------------------------------------------------- renumbering
h = must(h, '<h2>15. Regulatory and access matrix</h2>', '<h2>16. Regulatory and access matrix</h2>')
h = must(h, '<h2>16. Evidence boundary</h2>', '<h2>17. Evidence boundary</h2>')
h = must(h, '<h2>17. Evidence references</h2>', '<h2>18. Evidence references</h2>')
h = must(h, '<h2>18. Release control</h2>', '<h2>19. Release control</h2>')

# cross-reference in section 13 header text
h = must(h, 'Sections 13 and 15 record that several options',
            'Sections 13 and 16 record that several options')

# ------------------------------------------------------------- navigation
h = must(h,
    '      <a href="#trials">14. Clinical trials</a>\n'
    '      <a href="#access-status">15. Regulatory and access matrix</a>\n'
    '      <a href="#evidence-references">17. Evidence references</a>\n'
    '      <a href="#release-control">18. Release control</a>',
    '      <a href="#trials">14. Clinical trials</a>\n'
    '      <a href="#non-routine-access">15. Non-routine access routes</a>\n'
    '      <a href="#access-status">16. Regulatory and access matrix</a>\n'
    '      <a href="#evidence-references">18. Evidence references</a>\n'
    '      <a href="#release-control">19. Release control</a>')

h = must(h,
    '<li><a href="#trials">14. Clinical trials</a></li>\n'
    '          <li><a href="#access-status">15. Regulatory and access matrix</a></li>\n'
    '          <li><a href="#evidence-references">17. Evidence references</a></li>\n'
    '          <li><a href="#release-control">18. Release control</a></li>',
    '<li><a href="#trials">14. Clinical trials</a></li>\n'
    '          <li><a href="#non-routine-access">15. Non-routine access routes</a></li>\n'
    '          <li><a href="#access-status">16. Regulatory and access matrix</a></li>\n'
    '          <li><a href="#evidence-references">18. Evidence references</a></li>\n'
    '          <li><a href="#release-control">19. Release control</a></li>')

# ----------------------------------------------------- boundary cross-ref
h = must(h,
  '<p>Absence of a national route does not prove that treatment is unavailable through a trial, early-access programme or individual decision. Those routes must be described as non-routine and confirmed before treatment.</p>',
  '<p>Absence of a national route does not prove that treatment is unavailable through a trial, early-access programme or individual decision. Those routes must be described as non-routine and confirmed before treatment. <strong>Section 15 sets out what each of those routes actually is, which of them was found to be documented for the agents in this guideline, and the governance that applies.</strong></p>')

# --------------------------------------------------------- card updates
CARDS = [
 ('<p><strong>England access:</strong> No demonstrated national MCL commissioning route; CLL access must not be transposed to MCL.</p>',
  '<p><strong>England access:</strong> No demonstrated national MCL commissioning route; CLL access must not be transposed to MCL. A named individual-patient expanded access programme exists (NCT05172700, Loxo Oncology at Eli Lilly) covering mantle cell lymphoma previously treated with a covalent BTK inhibitor, with no United Kingdom site listed and requests routed through the local company office — see section 15.</p>'),
 ('<p><strong>England access:</strong> No demonstrated national MCL commissioning route; DLBCL routes must not be extrapolated. The referable route is the GLOBRYTE randomised phase III trial, which is recruiting at United Kingdom sites — see section 14.</p>',
  '<p><strong>England access:</strong> No demonstrated national MCL commissioning route; DLBCL routes must not be extrapolated. The manufacturer\'s published compassionate use list covers diffuse large B-cell lymphoma, transformed follicular lymphoma and primary mediastinal B-cell lymphoma but <strong>not</strong> mantle cell lymphoma, and the expired MHRA early-access opinion was DLBCL-only. The referable route is the GLOBRYTE randomised phase III trial, recruiting at United Kingdom sites — see sections 14 and 15.</p>'),
 ('<p><strong>England access:</strong> No final recommendation or demonstrated national MCL Blueteq route.</p>',
  '<p><strong>England access:</strong> No final recommendation or demonstrated national MCL Blueteq route. No published expanded access or company scheme for this combination was located; a general manufacturer early-access request route exists. Interim NHS funding does not apply because it requires <em>positive</em> draft guidance. See section 15.</p>'),
 ('<p><strong>England access:</strong> No final NICE entitlement or demonstrated national commissioning route at the cut-off.</p>',
  '<p><strong>England access:</strong> No final NICE entitlement or demonstrated national commissioning route at the cut-off. Note that first-line ibrutinib was separately available in England from March 2020 under the NHS England COVID-19 interim treatment options, which was NHS commissioning rather than compassionate supply and generated a 149-patient national cohort (S44). That scheme must not be cited as evidence of a current route. See section 15.</p>'),
]
for old, new in CARDS:
    h = must(h, old, new)

# --------------------------------------------------------------- S44 record
S44 = """<li class="evidence-reference" id="reference-S44"><strong>S44:</strong> Tivey A, Shotton R, Eyre TA et al. Ibrutinib as first-line therapy for mantle cell lymphoma: a multicenter, real-world UK study. Blood Adv. 2024;8(5):1209–1219. DOI 10.1182/bloodadvances.2023011152<br><strong>Design/population:</strong> Observational cohort of patients treated under the NHS England COVID-19 interim scheme; N=149 from 43 English centres; median age 75; 92.2% not autologous transplant candidates; 36.2% high-risk; 39.0% received rituximab; median follow-up 15.6 months<br><strong>Verified extraction:</strong> Overall response 71.2% and complete response 20.2% among 104 response-assessed patients; median progression-free survival 26.0 months overall, 13.7 months in high-risk versus not reached in low-risk; median overall survival not reached overall, 14.8 months in high-risk; grade 3 or higher toxicity 20.3%; 8.1% discontinued for toxicity; median post-ibrutinib survival 1.4 months, 8.6 months in the 41.9% receiving subsequent treatment versus 0.6 months in those who did not<br><strong>Integrity:</strong> V2.1; abstract-level; observational and non-randomised; documents an NHS commissioning scheme, not a compassionate access route; NEW IN v2.1</li>
"""
idx = h.find('id="reference-S43"')
if idx < 0:
    sys.exit('S43 not found')
close_ol = h.find('</ol>', idx)
h = h[:close_ol] + S44 + h[close_ol:]

# ------------------------------------------------- BSH verbatim in section 1
h = must(h,
  'Where this document differs from BSH 2023, the difference reflects evidence published after that guideline and is identified in section 13. This document does not replace, and has no standing against, the BSH guideline.',
  'Where this document differs from BSH 2023, the difference reflects evidence published after that guideline and is identified in section 13. This document does not replace, and has no standing against, the BSH guideline. Its relapsed-setting recommendation remains directly applicable: <q>Offer ibrutinib monotherapy as an approved and reimbursed standard of care option in the United Kingdom at first relapse (1B). Where the choice of ibrutinib, acalabrutinib or zanubrutinib is available, treatment should be individualised based on the specific toxicity profile of each agent (1B). Where a covalent BTKi has been used in first line as continuous therapy, consider clinical trials or immunochemotherapy at first relapse (2B).</q>')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
