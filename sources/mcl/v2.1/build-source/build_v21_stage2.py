#!/usr/bin/env python3
"""Stage 2: section 12 international table, new sections 13-14, matrix updates,
extended evidence ledger, renumbering, release control, sidebar and footer."""
import re, sys, io

h = io.open('/home/claude/_stage1.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:160])
    return html.replace(needle, repl, n)


def replace_section(html, sec_id, new_html):
    pat = re.compile(r'(<section id="%s"[^>]*>).*?</section>' % re.escape(sec_id), re.S)
    m = pat.search(html)
    if not m:
        sys.exit('SECTION NOT FOUND: %s' % sec_id)
    inner = re.sub(r'^<section id="[^"]*"[^>]*>', '', new_html.strip())
    return html[:m.start()] + m.group(1) + inner + html[m.end():]


# ================================================ SECTION 12 with intl table
h = replace_section(h, 'jurisdictions', """<section id="jurisdictions">
    <h2>12. Regulatory and access boundary</h2>
    <p>The publication model uses an England access framework with separate devolved-nation notes. GB marketing authorisation, NICE recommendations, NHS England operational funding, SMC/NHSScotland, AWMSG/NHS Wales and HSCNI implementation are distinct determinations.</p>
    <p>Absence of a national route does not prove that treatment is unavailable through a trial, early-access programme or individual decision. Those routes must be described as non-routine and confirmed before treatment.</p>
    <h3>United Kingdom against other jurisdictions</h3>
    <p>The table records regulatory status only. Nothing in the non-United Kingdom columns creates a route to treatment for a patient here, and the England column records commissioning, which is a separate determination from the Great Britain licence.</p>
    <div class="tbl-wrap">
      <table>
        <caption class="sidebar-note" style="text-align:left;caption-side:bottom;padding-top:.4rem;">Retrieved 30 July 2026. &ldquo;Not identified&rdquo; means no authorisation was found in the checked sources, not that none exists.</caption>
        <thead><tr><th scope="col">Agent or regimen</th><th scope="col">Great Britain licence</th><th scope="col">United States</th><th scope="col">European Union</th><th scope="col">England routine commissioning</th></tr></thead>
        <tbody>
          <tr><td>Ibrutinib, first line with R-CHOP/R-DHAP (ASCT-eligible)</td><td>Authorised</td><td><strong>Indication withdrawn</strong>, effective 18 Dec 2023</td><td>Authorised</td><td>No — appraisal unfinished</td></tr>
          <tr><td>Ibrutinib monotherapy, relapsed or refractory</td><td>Authorised</td><td><strong>Indication withdrawn</strong>, effective 18 Dec 2023</td><td>Authorised</td><td><strong>Yes</strong> — TA502, after exactly one line</td></tr>
          <tr><td>Zanubrutinib monotherapy, relapsed or refractory</td><td>Authorised</td><td>Approved, accelerated approval 14 Nov 2019, not yet converted</td><td><strong>No mantle cell lymphoma indication</strong></td><td><strong>Yes</strong> — TA1081, after exactly one line</td></tr>
          <tr><td>Acalabrutinib with bendamustine–rituximab, first line, transplant-ineligible</td><td>Authorised</td><td>Approved 16 Jan 2025, full approval</td><td>Approved 6 May 2025</td><td>No — negative draft guidance, appraisal rescheduled</td></tr>
          <tr><td>Acalabrutinib monotherapy, relapsed or refractory, BTKi-naive</td><td>Authorised</td><td>Approved; accelerated approval converted to full 16 Jan 2025</td><td>Authorised</td><td>No — appraisal awaiting development</td></tr>
          <tr><td>Pirtobrutinib monotherapy, after BTK inhibitor</td><td>Authorised</td><td>Accelerated approval 27 Jan 2023, ≥2 lines including a BTK inhibitor</td><td>Conditional authorisation 30 Oct 2023</td><td>No — one appraisal suspended, one awaiting development</td></tr>
          <tr><td>Brexucabtagene autoleucel</td><td>Authorised</td><td><strong>Full approval 2 Apr 2026</strong> (converted from accelerated)</td><td>Conditional authorisation 14 Dec 2020</td><td>Managed access under TA677; <strong>review at appeal, outcome unresolved</strong></td></tr>
          <tr><td>Lisocabtagene maraleucel</td><td>Authorised</td><td>Accelerated approval 30 May 2024</td><td>Mantle cell lymphoma extension approved 24 Nov 2025</td><td>No — appraisal awaiting development</td></tr>
          <tr><td>Sonrotoclax</td><td><strong>Not identified</strong></td><td><strong>Accelerated approval 13 May 2026</strong>, ≥2 lines including a BTK inhibitor</td><td>Not identified</td><td>No — trial only</td></tr>
          <tr><td>Venetoclax (any mantle cell lymphoma use)</td><td>Not authorised</td><td>Not approved</td><td>Not approved (orphan designation only)</td><td>No — trial only</td></tr>
          <tr><td>Glofitamab</td><td>Not authorised for mantle cell lymphoma</td><td>No mantle cell lymphoma indication</td><td>No mantle cell lymphoma indication</td><td>No — trial only</td></tr>
          <tr><td>Epcoritamab</td><td>Not authorised for mantle cell lymphoma</td><td>No mantle cell lymphoma indication</td><td>No mantle cell lymphoma indication</td><td>No — trial only</td></tr>
          <tr><td>Bortezomib, VR-CAP, first line, HSCT unsuitable</td><td>Authorised</td><td>Approved Oct 2014</td><td>Authorised</td><td><strong>Yes</strong> — TA370</td></tr>
          <tr><td>Lenalidomide monotherapy, relapsed or refractory</td><td>Authorised</td><td>Approved Jun 2013, after two prior therapies including bortezomib</td><td>Authorised</td><td>No — TA774 terminated on non-submission</td></tr>
        </tbody>
      </table>
    </div>
    <div class="jx"><strong>The three divergences most likely to mislead</strong>
      <p><strong>1. Ibrutinib.</strong> A United States source contains no ibrutinib in mantle cell lymphoma at any line. In England ibrutinib is a routinely commissioned second-line option. Do not conclude from a United States algorithm that ibrutinib has been superseded here.</p>
      <p><strong>2. Zanubrutinib.</strong> A European Union source contains no zanubrutinib in mantle cell lymphoma at all, because there is no European authorisation. In England it is NICE-recommended after exactly one line. Do not conclude from a European algorithm that it is unavailable here.</p>
      <p><strong>3. Sonrotoclax.</strong> A United States source published after May 2026 will present sonrotoclax as an approved post-BTK-inhibitor option. There is no Great Britain licence. The only United Kingdom route is trial entry.</p>
    </div>
    <div class="uk"><strong>Society guidance and its jurisdiction</strong>
      <p>The 2025 EHA–EU mantle cell lymphoma network guideline is the most current European society document and is the primary society anchor used here. The <em>Lymphomas: ESMO Clinical Practice Guideline</em> (2025; PMID 40774601) supersedes the 2017 ESMO mantle cell lymphoma guideline. NCCN B-Cell Lymphomas is a United States document whose regimen listings assume United States licensing, including the absence of ibrutinib; its current version could not be verified because the source is access-controlled, and no NCCN category of evidence is quoted anywhere in this document.</p>
      <p>None of these documents is a commissioning instrument in England. A society recommendation is not a funding route.</p>
    </div>
  </section>""")

# =============================================== NEW SECTION 13 evidence model
EVIDENCE_MODEL = """
  <section id="evidence-model">
    <h2>13. Evidence-to-recommendation model</h2>
    <p>This section states, for each clinical decision in the guideline, the strength of the underlying evidence and — separately — whether the option can actually be delivered in England. The two are recorded independently and deliberately. A recommendation may rest on strong randomised evidence and still have no route to the patient; an option may be routinely funded on evidence that is weaker than a clinician would assume.</p>
    <h3>How the classifications are assigned</h3>
    <p><strong>Evidence certainty</strong> describes the design and consistency of the supporting evidence, not the size of the effect.</p>
    <ul>
      <li><span class="tier a">A</span> One or more randomised phase III trials in mantle cell lymphoma with a consistent direction of effect, or a society guideline recommendation built directly on such trials.</li>
      <li><span class="tier b">B</span> A single randomised trial with material limitations, a randomised phase II trial, or randomised evidence in a mixed population from which a mantle cell lymphoma-specific effect cannot be isolated.</li>
      <li><span class="tier c">C</span> Prospective single-arm trial evidence.</li>
      <li><span class="tier d">D</span> Registry, real-world or other observational evidence, or a non-randomised secondary analysis of a randomised trial.</li>
      <li><span class="tier e">E</span> Conference abstract or press release only, with no peer-reviewed primary publication retrievable.</li>
    </ul>
    <p><strong>England access class</strong> describes deliverability, which is a separate determination from the licence.</p>
    <ul>
      <li><strong>R1</strong> Routine NHS England funding through a positive technology appraisal.</li>
      <li><strong>R2</strong> Managed access — Cancer Drugs Fund, subject to live national criteria.</li>
      <li><strong>R3</strong> Guideline-supported conventional practice delivered through network SACT or transplant services without a regimen-specific technology appraisal.</li>
      <li><strong>R4</strong> Holds a Great Britain marketing authorisation but has no demonstrated routine national route.</li>
      <li><strong>R5</strong> No Great Britain mantle cell lymphoma marketing authorisation; trial or an individually approved exceptional route only.</li>
    </ul>
    <p><strong>United Kingdom priority</strong> is the practical instruction that follows from combining the two.</p>
    <ul>
      <li><span class="pri">P1</span> Offer as a standard option when clinically appropriate.</li>
      <li><span class="pri">P2</span> Offer where the exact appraisal or national criteria are met, after confirming the live position.</li>
      <li><span class="pri">P3</span> Consider only through a clinical trial or a specifically approved exceptional route; discuss at MDT.</li>
      <li><span class="pri">P4</span> Do not use outside a clinical trial.</li>
    </ul>
    <h3>First-line, younger or treatment-fit adults</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Option</th><th scope="col">Certainty</th><th scope="col">Key records</th><th scope="col">Access</th><th scope="col">Priority</th><th scope="col">Basis and limits</th></tr></thead>
        <tbody>
          <tr><td>Cytarabine-containing induction, ASCT, 3 years rituximab maintenance</td><td><span class="tier a">A</span></td><td>S01, S26, S27, S28</td><td>R3</td><td><span class="pri">P1</span></td><td>MCL Younger tests a bundled strategy and does not isolate the effect of ASCT; LYMA supports maintenance, with the long-term overall survival difference not statistically significant.</td></tr>
          <tr><td>TRIANGLE-derived ibrutinib-containing regimen without routine ASCT</td><td><span class="tier a">A</span></td><td>S06, S24</td><td>R4</td><td><span class="pri">P3</span></td><td>Licensed in Great Britain; no final NICE guidance. Increased grade 3–5 infection. Applicability limited to the trial protocol and ages 18–65.</td></tr>
          <tr><td>Rituximab maintenance within a TRIANGLE-derived pathway</td><td><span class="tier d">D</span></td><td>S23</td><td>R3</td><td><span class="pri">P2</span></td><td>Non-randomised secondary analysis with residual confounding and more grade 3–5 infection. EHA–EU recommends it; do not present it as risk-free.</td></tr>
          <tr><td>Obinutuzumab substituted for rituximab</td><td><span class="tier d">D</span></td><td>S32</td><td>R5</td><td><span class="pri">P4</span></td><td>Propensity-matched, not randomised. No mantle cell lymphoma marketing authorisation.</td></tr>
        </tbody>
      </table>
    </div>
    <h3>First-line, older or transplant-ineligible adults</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Option</th><th scope="col">Certainty</th><th scope="col">Key records</th><th scope="col">Access</th><th scope="col">Priority</th><th scope="col">Basis and limits</th></tr></thead>
        <tbody>
          <tr><td>Bendamustine–rituximab, then rituximab maintenance ≥2 years</td><td><span class="tier b">B</span></td><td>S25, S21, S29</td><td>R3</td><td><span class="pri">P1</span></td><td>StiL was a pooled indolent and mantle cell lymphoma population with no mantle cell-specific effect in the abstract; maintenance-after-BR evidence is substantially observational.</td></tr>
          <tr><td>VR-CAP</td><td><span class="tier a">A</span></td><td>S31</td><td>R1</td><td><span class="pri">P2</span></td><td>TA370 recommends within the marketing authorisation. More neutropenia and thrombocytopenia than R-CHOP. Do not generalise to transplant-suitable patients.</td></tr>
          <tr><td>R-BAC</td><td><span class="tier c">C</span></td><td>S30</td><td>R3</td><td><span class="pri">P2</span></td><td>Single-arm; no randomised comparison against BR; greater haematological toxicity; no maintenance given in the study.</td></tr>
          <tr><td>Adding bortezomib to bendamustine–rituximab induction</td><td><span class="tier a">A</span></td><td>S35</td><td>—</td><td><span class="pri">P4</span></td><td><strong>Randomised and negative.</strong> Hazard ratio 0.90 (90% CI 0.70–1.16) at 7.5 years.</td></tr>
          <tr><td>Adding lenalidomide to rituximab maintenance</td><td><span class="tier a">A</span></td><td>S35</td><td>—</td><td><span class="pri">P4</span></td><td><strong>Randomised and negative.</strong> Hazard ratio 0.84 (90% CI 0.62–1.15).</td></tr>
          <tr><td>Acalabrutinib with bendamustine–rituximab</td><td><span class="tier a">A</span></td><td>S08</td><td>R4</td><td><span class="pri">P3</span></td><td>Progression-free survival benefit without demonstrated overall survival advantage. Negative draft guidance 25 Feb 2026; appraisal rescheduled at the company's request.</td></tr>
          <tr><td>Ibrutinib with bendamustine–rituximab (SHINE)</td><td><span class="tier a">A</span></td><td>S22</td><td>R5</td><td><span class="pri">P4</span></td><td>Progression-free survival benefit, no overall survival advantage, more grade 3–4 toxicity. No first-line route identified.</td></tr>
          <tr><td>Ibrutinib–rituximab (ENRICH)</td><td><span class="tier a">A</span></td><td>S07</td><td>R5</td><td><span class="pri">P4</span></td><td>Superiority over the pooled control, not over bendamustine–rituximab specifically. No first-line route.</td></tr>
          <tr><td>Ibrutinib with venetoclax, first line, ≥65 or TP53-mutated</td><td><span class="tier c">C</span></td><td>S36</td><td>R5</td><td><span class="pri">P4</span></td><td>Open-label single-arm cohort. No Great Britain mantle cell lymphoma authorisation; NICE appraisal suspended 20 Jan 2026.</td></tr>
        </tbody>
      </table>
    </div>
    <h3>TP53-mutated and other high-risk disease</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Option or statement</th><th scope="col">Certainty</th><th scope="col">Key records</th><th scope="col">Access</th><th scope="col">Priority</th><th scope="col">Basis and limits</th></tr></thead>
        <tbody>
          <tr><td>TP53 mutation is adverse under intensive chemoimmunotherapy</td><td><span class="tier b">B</span></td><td>S04, S02, S03</td><td>—</td><td><span class="pri">P1</span></td><td>Molecular cohort evidence; prognostic, not a demonstration that any one alternative is superior.</td></tr>
          <tr><td>TP53 mutation remains adverse under BTK inhibitor plus BCL2 inhibitor</td><td><span class="tier c">C</span></td><td>S36</td><td>—</td><td><span class="pri">P1</span></td><td>High response rate with markedly shorter disease control; median progression-free survival 22.0 months if aged ≥65, 15.4 months if younger.</td></tr>
          <tr><td>Trial referral in TP53-mutated disease</td><td><span class="tier a">A</span></td><td>S01</td><td>R3</td><td><span class="pri">P1</span></td><td>Guideline recommendation; operationally the most reliable route to a targeted combination in England.</td></tr>
          <tr><td>Anti-CD20 with BTK inhibitor and BCL2 inhibitor, first line</td><td><span class="tier c">C</span></td><td>S09, S01</td><td>R5</td><td><span class="pri">P4</span></td><td>BOVen is single-arm, n=25. EHA–EU recommends the class combination, but no such combination is licensed for mantle cell lymphoma in Great Britain.</td></tr>
          <tr><td>MRD-guided treatment cessation</td><td><span class="tier b">B</span></td><td>S12, S12C, S13, S11</td><td>R5</td><td><span class="pri">P4</span></td><td>Studied within protocols. Not a validated universal surrogate; do not omit maintenance outside a trial.</td></tr>
        </tbody>
      </table>
    </div>
    <h3>Relapsed or refractory disease</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Option</th><th scope="col">Certainty</th><th scope="col">Key records</th><th scope="col">Access</th><th scope="col">Priority</th><th scope="col">Basis and limits</th></tr></thead>
        <tbody>
          <tr><td>Ibrutinib after exactly one previous line</td><td><span class="tier b">B</span></td><td>TA502</td><td>R1</td><td><span class="pri">P2</span></td><td>Licence is broader than the NICE restriction. Subject to the commercial arrangement and Blueteq criteria.</td></tr>
          <tr><td>Zanubrutinib after exactly one previous line</td><td><span class="tier b">B</span></td><td>TA1081</td><td>R1</td><td><span class="pri">P2</span></td><td>TA1081 directs use of the least expensive suitable option, naming zanubrutinib and ibrutinib. Intolerance transfer from ibrutinib requires absence of progression.</td></tr>
          <tr><td>Brexucabtagene autoleucel after ≥2 lines including a BTK inhibitor</td><td><span class="tier c">C</span></td><td>S15, S37, S17, S18</td><td>R2</td><td><span class="pri">P2</span></td><td>Durable single-arm and registry activity with material attrition and 24-month non-relapse mortality of 25% in United Kingdom data. <strong>TA677 review at appeal; outcome unresolved.</strong> Confirm live criteria before referral.</td></tr>
          <tr><td>Ibrutinib with venetoclax</td><td><span class="tier a">A</span></td><td>S38, S39</td><td>R5</td><td><span class="pri">P4</span></td><td>Randomised phase III benefit, hazard ratio 0.65. No Great Britain mantle cell lymphoma authorisation; appraisal suspended because an MHRA application was not being pursued. Strong evidence, no route.</td></tr>
          <tr><td>Pirtobrutinib after covalent BTK-inhibitor exposure</td><td><span class="tier c">C</span></td><td>S14</td><td>R4</td><td><span class="pri">P3</span></td><td>Single-arm. One appraisal suspended on non-submission, a second in a BTKi-untreated population awaiting development. Do not transpose the CLL route.</td></tr>
          <tr><td>Lisocabtagene maraleucel after ≥2 lines including a BTK inhibitor</td><td><span class="tier c">C</span></td><td>S16</td><td>R4</td><td><span class="pri">P3</span></td><td>Phase I. No head-to-head comparison with brexucabtagene autoleucel or pirtobrutinib.</td></tr>
          <tr><td>Glofitamab</td><td><span class="tier c">C</span></td><td>S19</td><td>R5</td><td><span class="pri">P4</span></td><td>Phase I/II, fixed duration. GLOBRYTE phase III is recruiting with United Kingdom sites and is the referable route.</td></tr>
          <tr><td>Sonrotoclax</td><td><span class="tier c">C</span></td><td>S20, S20C</td><td>R5</td><td><span class="pri">P4</span></td><td>Phase I/II; erratum content unresolved. United States approved, no Great Britain licence. CELESTIAL-RRMCL is recruiting with United Kingdom sites.</td></tr>
          <tr><td>Mosunetuzumab with polatuzumab vedotin</td><td><span class="tier c">C</span></td><td>S40</td><td>R5</td><td><span class="pri">P4</span></td><td>Single-arm, n=42. Neither agent licensed for mantle cell lymphoma anywhere.</td></tr>
          <tr><td>Bortezomib added to rituximab, high-dose cytarabine and dexamethasone</td><td><span class="tier a">A</span></td><td>S41</td><td>R5</td><td><span class="pri">P4</span></td><td>Randomised phase III, n=128; time to treatment failure 12 versus 2.6 months. No regimen-specific appraisal in this setting.</td></tr>
          <tr><td>Lenalidomide monotherapy</td><td><span class="tier c">C</span></td><td>—</td><td>R4</td><td><span class="pri">P3</span></td><td>TA774 was terminated on non-submission, which is no recommendation rather than a negative clinical recommendation.</td></tr>
          <tr><td>Cross-trial ranking of post-BTKi options</td><td><span class="tier e">E</span></td><td>—</td><td>—</td><td><span class="pri">P4</span></td><td>No head-to-head randomised comparison exists between pirtobrutinib, cellular therapy, bispecific antibodies and BCL2 inhibition. Unadjusted response rates must not be used to rank them.</td></tr>
        </tbody>
      </table>
    </div>
    <div class="changed"><strong>Where evidence and access are furthest apart</strong>
      <p>Three options carry <span class="tier a">A</span>-level randomised evidence and no route to an English patient outside a trial: ibrutinib with venetoclax in relapsed disease, acalabrutinib with bendamustine–rituximab in the first line, and the TRIANGLE-derived regimen. In each the constraint is regulatory or economic, not clinical. State this to patients plainly rather than implying the evidence is weak.</p>
      <p>One option runs the other way. Brexucabtagene autoleucel rests on <span class="tier c">C</span>-level single-arm evidence, is the only cellular therapy with an England route, and that route is currently under challenge at appeal.</p>
    </div>
  </section>
"""

# ==================================================== NEW SECTION 14 trials
TRIALS = """
  <section id="trials">
    <h2>14. Clinical trials</h2>
    <p>Trial entry is the only route to several options recorded in this guideline as having evidence but no commissioned pathway. This section lists studies identified on 30 July 2026 and exists so that a referral can be made rather than an option merely noted as unavailable.</p>
    <div class="draft-banner" style="border-width:2px;">
      <strong>Verify before referring.</strong>
      <p>Recruitment status changes without notice and a registry record may lag the site. Confirm current status, site activation and eligibility with the local principal investigator or the coordinating centre before discussing a trial with a patient. Registry identifiers below are recorded exactly as retrieved; where a field could not be verified it is marked as such rather than filled.</p>
    </div>
    <h3>Recruiting in the United Kingdom — first line</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Trial</th><th scope="col">Identifier</th><th scope="col">Phase</th><th scope="col">Population and intervention</th><th scope="col">Sponsor</th></tr></thead>
        <tbody>
          <tr><td>ZEBRA</td><td class="trial-id">NCT05635162</td><td>II</td><td>Indolent or low-burden mantle cell lymphoma. Zanubrutinib with rituximab against active observation. United Kingdom only, 13 sites.</td><td>University College London</td></tr>
        </tbody>
      </table>
    </div>
    <p>ZEBRA was the only first-line mantle cell lymphoma study identified as actively recruiting in the United Kingdom at retrieval. It is directly relevant to section 4, because it tests whether early treatment improves on observation in exactly the population that guideline recommends observing.</p>
    <h3>Recruiting in the United Kingdom — relapsed or refractory</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Trial</th><th scope="col">Identifier</th><th scope="col">Phase</th><th scope="col">Population and intervention</th><th scope="col">United Kingdom sites</th></tr></thead>
        <tbody>
          <tr><td>GLOBRYTE</td><td class="trial-id">NCT06084936</td><td>III</td><td>After a BTK inhibitor. Glofitamab with obinutuzumab pretreatment against rituximab–bendamustine or rituximab–lenalidomide.</td><td>Glasgow, Lincoln, London, Manchester, Oxford, Plymouth</td></tr>
          <tr><td>CELESTIAL-RRMCL</td><td class="trial-id">NCT06742996</td><td>III</td><td>One to five prior lines. Sonrotoclax with zanubrutinib against placebo with zanubrutinib.</td><td>Glasgow, Oxford, Wirral, Plymouth, Bournemouth, London</td></tr>
          <tr><td>CaDAnCe-101</td><td class="trial-id">NCT05006716</td><td>I/II</td><td>BGB-16673, a BTK degrader, in relapsed or refractory B-cell malignancies including mantle cell lymphoma.</td><td>Edinburgh, Leeds, Newcastle, Cambridge, Nottingham, Plymouth</td></tr>
          <tr><td>NX-5948 first-in-human</td><td class="trial-id">NCT05131022</td><td>I</td><td>BTK degrader; mantle cell lymphoma is a defined expansion cohort.</td><td>United Kingdom among eight countries</td></tr>
          <tr><td>ALETA-001</td><td class="trial-id">NCT06045910</td><td>I/II</td><td>CD19-directed CAR-T engager designed to be given after CAR-T.</td><td>United Kingdom only — Birmingham, Cambridge, Leeds, London, Manchester, Sutton</td></tr>
          <tr><td>AZD0486</td><td class="trial-id">NCT06564038</td><td>I/II</td><td>CD19×CD3 T-cell engager, alone or with acalabrutinib or R-CHOP.</td><td>Four United Kingdom sites among 13 countries</td></tr>
          <tr><td>Sonrotoclax ramp-up study</td><td class="trial-id">NCT06697184</td><td>I/II</td><td>Novel ramp-up schedule with or without zanubrutinib, in chronic lymphocytic leukaemia and mantle cell lymphoma.</td><td>United Kingdom among four countries</td></tr>
          <tr><td>LY4152199</td><td class="trial-id">NCT07101328</td><td>I</td><td>First-in-human, B-cell malignancies.</td><td>United Kingdom among 12 countries</td></tr>
          <tr><td>ABBV-291</td><td class="trial-id">NCT06667687</td><td>I</td><td>First-in-human, intravenous.</td><td>Manchester, Plymouth</td></tr>
          <tr><td>EXS73565</td><td class="trial-id">NCT06980116</td><td>I</td><td>Oral agent, B-cell malignancies.</td><td>Leeds, Plymouth</td></tr>
        </tbody>
      </table>
    </div>
    <p>GLOBRYTE and CELESTIAL-RRMCL matter most operationally. They are the referable routes to the two agents this guideline records as having activity after BTK-inhibitor failure with no United Kingdom licence — glofitamab and sonrotoclax. Both are randomised phase III, which means a patient entering either has a defined chance of receiving an active comparator rather than the investigational agent, and consent must say so.</p>
    <h3>United Kingdom studies no longer recruiting but relevant to interpretation</h3>
    <p>CARAMEL (<span class="trial-id">NCT05004064</span>, acalabrutinib with rituximab in elderly or frail untreated patients, University College London), OASIS-II (<span class="trial-id">NCT04802590</span>, ibrutinib with an anti-CD20 antibody and venetoclax, LYSARC), MANGROVE (<span class="trial-id">NCT04002297</span>, zanubrutinib with rituximab against bendamustine–rituximab in transplant-ineligible disease), TrAVeRse (<span class="trial-id">NCT05951959</span>, acalabrutinib with venetoclax and rituximab), ENRICH (<span class="trial-id">ISRCTN11038174</span>) and BRUIN MCL-321 (<span class="trial-id">NCT04662255</span>, pirtobrutinib against investigator-choice covalent BTK inhibitor in BTKi-naive patients) are all active and not recruiting with United Kingdom involvement. Their readouts will bear directly on sections 6 and 8.</p>
    <div class="changed"><strong>MANGROVE has not been published</strong>
      <p>No peer-reviewed primary publication of MANGROVE was retrievable on 30 July 2026. Topline results have circulated through company communication and secondary reporting. Under the evidence model in section 13 that is <span class="tier e">E</span>-level, and no MANGROVE efficacy figure is quoted anywhere in this guideline. Reassess when the primary publication appears.</p>
    </div>
    <h3>Selected international studies without United Kingdom sites</h3>
    <p>These are recorded for horizon scanning only and are <strong>not referable</strong> for a patient in the United Kingdom. First line: a randomised comparison of continuous against intermittent zanubrutinib in older untreated patients (<span class="trial-id">NCT05976763</span>, phase III, United States); CARMAN, first-line brexucabtagene autoleucel with ibrutinib against chemoimmunotherapy in high-risk disease (<span class="trial-id">NCT06482684</span>, phase II, Germany); BRAZAN (<span class="trial-id">NCT06854003</span>, United States); and several randomised orelabrutinib combinations in China. Relapsed or refractory: randomised pirtobrutinib with brexucabtagene autoleucel (<span class="trial-id">NCT06553872</span>, United States); glofitamab with pirtobrutinib (<span class="trial-id">NCT05833763</span>, Australia); and a randomised comparison of rocbrutinib against investigator-choice BTK inhibitor (<span class="trial-id">NCT07377578</span>, China).</p>
    <div class="uk"><strong>Search limits</strong>
      <p>The sweep covered ClinicalTrials.gov, with partial retrieval from ISRCTN and from a United Kingdom charity trial finder. <strong>The European Union Clinical Trials Information System returned HTTP 403 and was not searched</strong>, so any European study not cross-registered on ClinicalTrials.gov is absent. ISRCTN could not be searched systematically, so a United Kingdom academic study registered only there may be missing. This list is therefore a floor, not a complete census.</p>
    </div>
  </section>
"""

# insert new sections before the access matrix
anchor = '  <section id="access-status">'
if anchor not in h:
    sys.exit('access-status anchor not found')
h = h.replace(anchor, EVIDENCE_MODEL + TRIALS + anchor, 1)

# ============================================================== renumbering
h = must(h, '<h2>13. Regulatory and access matrix</h2>', '<h2>15. Regulatory and access matrix</h2>')
h = must(h, '<h2>14. Evidence boundary</h2>', '<h2>16. Evidence boundary</h2>')
h = must(h, '<h2>15. Evidence references</h2>', '<h2>17. Evidence references</h2>')
h = must(h, '<h2>16. Release control</h2>', '<h2>18. Release control</h2>')

# ================================================= matrix card text updates
CARD_EDITS = [
    # TRIANGLE ibrutinib regimen
    ('<p><strong>NICE:</strong> GID-TA11802/ID6596 remains in progress. June 2026 draft guidance recommends not using the regimen; this is not final guidance.</p>',
     '<p><strong>NICE:</strong> GID-TA11802/ID6596 remains in progress; expected publication TBC. The live project timeline runs only to an invitation to participate on 3 November 2025 and shows no committee meeting and no draft guidance. <strong>The v2.0 statement that a June 2026 draft recommendation exists could not be reproduced on 30 July 2026 and has been withdrawn.</strong> The documents tab returned HTTP 403 to automated retrieval; confirm directly before ratification.</p>'),
    # acalabrutinib + BR
    ('<p><strong>NICE:</strong> GID-TA11091/ID6155 remains in progress; February 2026 draft guidance recommends not using it. The displayed expected-publication date is overdue.</p>',
     '<p><strong>NICE:</strong> GID-TA11091/ID6155 remains in development. Committee meeting 3 February 2026; draft guidance published for consultation 25 February 2026 recommending against use on the basis that there is not enough evidence to determine value for money; consultation closed 18 March 2026. The displayed expected-publication date of 4 June 2026 has passed. Project note: <q>following on from advice received from the company this appraisal will be rescheduled to align with latest regulatory expectations.</q> Draft guidance is not final guidance.</p>'),
    # pirtobrutinib
    ('<p><strong>NICE:</strong> GID-TA10858/ID3975 returned to the NICE work programme on 14 July 2026 and remains in progress.</p>',
     '<p><strong>NICE:</strong> Two separate appraisals. <strong>GID-TA10858/ID3975</strong> (relapsed or refractory mantle cell lymphoma) is <strong>Suspended</strong>; the last timeline entry, 29 March 2024, records that the company informed NICE it will not provide an evidence submission. Expected publication TBC. <strong>The v2.0 statement that this appraisal returned to the work programme on 14 July 2026 could not be reproduced on 30 July 2026 and has been withdrawn.</strong> <strong>GID-TA11639/ID6493</strong> (relapsed or refractory mantle cell lymphoma <em>untreated with a BTK inhibitor</em>) is awaiting development; a note of 31 July 2025 records rescheduling with an anticipated start during early March 2026. Note that the second appraisal covers a different population from the licensed post-BTKi indication.</p>'),
    # brexu-cel NICE
    ('<p><strong>NICE:</strong> TA677 remains a Cancer Drugs Fund managed-access recommendation while review continues.</p>',
     '<p><strong>NICE:</strong> TA677 remains a Cancer Drugs Fund managed-access recommendation and is live at the cut-off. The review is <strong>GID-TA11545/ID6325</strong>: committee meetings 1 July and 2 September 2025; draft guidance consultation 23 July to 13 August 2025 concluding that brexucabtagene autoleucel <q>could not be recommended</q>; final draft guidance 24 December 2025 to 21 January 2026; <strong>appeal 30 March 2026; appeal decision published 9 June 2026</strong>. Expected publication TBC and no final guidance issued. <strong>The appeal decision content was not retrievable and the outcome is unknown to this draft.</strong> A Government answer of 26 January 2026 confirms NICE <q>has been unable to recommend the treatment in the final draft guidance</q> and records a continuation safeguard for patients already treated in managed access.</p>'),
    # brexu-cel England access
    ('<p><strong>England access:</strong> NHS England list v1.405 retains KTE01a/KTE01b managed-access forms and national eligibility criteria. Do not describe this as unrestricted baseline commissioning.</p>',
     '<p><strong>England access:</strong> NHS England list v1.405 retains KTE01a/KTE01b managed-access forms and national eligibility criteria. Do not describe this as unrestricted baseline commissioning. <strong>Given the unresolved appeal, confirm the live commissioning position before referral and do not promise a durable route to a patient.</strong></p>'),
    # ibrutinib+venetoclax evidence
    ('<p><strong>Evidence:</strong> Randomised progression-free survival evidence does not itself establish a licensed or commissioned route</p>',
     '<p><strong>Evidence:</strong> SYMPATICO, a double-blind placebo-controlled randomised phase III trial in 267 patients with one to five prior lines, reported median progression-free survival 31.9 versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia 31% versus 11%. A first-line open-label cohort in patients aged 65 or over or with TP53 mutation reported complete response 69% and median progression-free survival 40.2 months. Randomised progression-free survival evidence does not itself establish a licensed or commissioned route.</p>'),
    # zanubrutinib NICE verbatim
    ('<p><strong>NICE:</strong> TA1081 recommends an option after one line only, subject to the commercial arrangement and least-expensive-suitable-option wording.</p>',
     '<p><strong>NICE:</strong> TA1081, published 10 July 2025, states that <q>zanubrutinib can be used as an option to treat relapsed or refractory mantle cell lymphoma in adults who have had 1 line of treatment only</q> and directs clinicians to <q>use the least expensive option of the suitable treatments (including zanubrutinib and ibrutinib), having discussed the advantages and disadvantages of the available treatments with the person with the condition</q>. Subject to the commercial arrangement.</p>'),
    # acalabrutinib monotherapy NICE
    ('<p><strong>NICE:</strong> GID-TA11470/ID6389 is awaiting development; publication TBC.</p>',
     '<p><strong>NICE:</strong> GID-TA11470/ID6389 is awaiting development. Topic selection 24 November 2023; a note of 21 June 2024 records that, following advice from the company, timelines for this appraisal are to be confirmed. Publication TBC.</p>'),
    # glofitamab England access
    ('<p><strong>England access:</strong> No demonstrated national MCL commissioning route; DLBCL routes must not be extrapolated.</p>',
     '<p><strong>England access:</strong> No demonstrated national MCL commissioning route; DLBCL routes must not be extrapolated. The referable route is the GLOBRYTE randomised phase III trial, which is recruiting at United Kingdom sites — see section 14.</p>'),
]
for old, new in CARD_EDITS:
    h = must(h, old, new)

# ------------------------------------------- new matrix card: sonrotoclax
SONRO_CARD = """<article class="status-card alert" id="status-sonrotoclax"><h3>Sonrotoclax</h3><p><strong>Population:</strong> Adult relapsed or refractory MCL after at least two systemic lines including a BTK inhibitor, in the jurisdiction where it is approved</p><p><strong>Evidence:</strong> Phase I/II monotherapy after anti-CD20 and covalent BTK-inhibitor exposure; overall response 52.4% (95% CI 42.4–62.4), complete response 15.5%, median duration of response 15.8 months and median progression-free survival 6.5 months at 14.2 months median follow-up. A published erratum exists whose substantive correction has not been retrieved.</p><p><strong>Marketing authorisation:</strong> <strong>No Great Britain mantle cell lymphoma marketing authorisation was identified.</strong> Outside the United Kingdom: United States FDA accelerated approval 13 May 2026 for adults with relapsed or refractory mantle cell lymphoma after at least two lines of systemic therapy including a BTK inhibitor — the first BCL2 inhibitor approved in mantle cell lymphoma in any jurisdiction. No European Union authorisation was identified.</p><p><strong>NICE:</strong> No mantle cell lymphoma appraisal was identified in the documented live search.</p><p><strong>England access:</strong> No demonstrated national commissioning route. The referable route is the CELESTIAL-RRMCL randomised phase III trial, recruiting at United Kingdom sites — see section 14.</p><p><strong>Devolved nations:</strong> No national route was demonstrated in Scotland, Wales or Northern Ireland.</p><p><strong>Regimen:</strong> No licensed Great Britain mantle cell lymphoma regimen established.</p><p><strong>Dose, schedule and duration:</strong> Not applicable for United Kingdom practice: no Great Britain mantle cell lymphoma indication was recorded. A United States dose has been reported in secondary sources but is <strong>not reproduced here</strong>, because no verified Great Britain SmPC exists and a foreign label must not be used as a prescribing protocol.</p><p><strong>Administration and monitoring boundary:</strong> Do not use another jurisdiction's label or another indication's pathway as a mantle cell lymphoma protocol. BCL2 inhibition carries tumour-lysis risk requiring a validated ramp-up, and no United Kingdom-verified schedule is available.</p><p><strong>Pharmacy evidence status:</strong> NOT_APPLICABLE_NO_CURRENT_GB_MCL_INDICATION</p><p class="public-wording"><strong>Provisional public wording:</strong> Approved in the United States for relapsed or refractory mantle cell lymphoma after at least two lines including a BTK inhibitor; no Great Britain licence and no national commissioning route, so United Kingdom access is through a clinical trial only.</p></article>"""

# insert the new card immediately before the Epcoritamab card
epc = h.find('<article class="status-card" id="status-epcoritamab">')
if epc < 0:
    # fall back: find by heading
    m = re.search(r'<article class="status-card"[^>]*id="[^"]*epcoritamab[^"]*"', h)
    if not m:
        sys.exit('epcoritamab card not found')
    epc = m.start()
h = h[:epc] + SONRO_CARD + h[epc:]

# =============================================== extend the evidence ledger
NEW_REFS = """<li class="evidence-reference" id="reference-S32"><strong>S32:</strong> Sarkozy C et al. Obinutuzumab versus rituximab for transplant-eligible patients with mantle cell lymphoma. Blood. 2024. PMID 38669626; DOI 10.1182/blood.2024023944<br><strong>Design/population:</strong> Prospective LyMa-101 cohort, N=85, with propensity-score matching against LYMA rituximab controls<br><strong>Verified extraction:</strong> 5-year PFS 83.4% and OS 86.9%; matched comparison PFS 82.8% versus 66.6% and OS 86.4% versus 71.4%<br><strong>Integrity:</strong> V2.1; abstract-level; non-randomised comparison, residual confounding; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S33"><strong>S33:</strong> Khouja M et al. Noninvasive genotyping and early disease dynamics in the TRIANGLE trial. Leukemia. 2026. PMID 41184633; DOI 10.1038/s41375-025-02787-0<br><strong>Design/population:</strong> Biomarker substudy within randomised phase III TRIANGLE; n=57 genotyped<br><strong>Verified extraction:</strong> Faster ctDNA clearance in ibrutinib-containing arms (59% versus 24%); attenuated TP53-mutation hazard relative to control<br><strong>Integrity:</strong> V2.1; abstract-level; exploratory subset analysis, not a demonstration that TP53 risk is removed; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S34"><strong>S34:</strong> Jiang L et al. Marked survival gains in patients aged 65 years or younger with advanced-stage mantle cell lymphoma: pooled analysis of six randomised phase III trials, 1996–2020. Haematologica. 2026. PMID 41163573; DOI 10.3324/haematol.2025.288929<br><strong>Design/population:</strong> Pooled individual-patient analysis of six randomised trials; N=2,541<br><strong>Verified extraction:</strong> Median OS in patients aged ≤65 rose from 4.9 years to 13.8 years to not reached across successive eras, 5-year OS 49% to 84%; older or transplant-ineligible patients 3.8 to 4.8 years<br><strong>Integrity:</strong> V2.1; abstract-level; pooled across trials with differing eligibility; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S35"><strong>S35:</strong> Smith MR, Jegede OA, Martin P et al. Randomized study of induction with bendamustine-rituximab with or without bortezomib and maintenance with rituximab with or without lenalidomide for mantle cell lymphoma (E1411). Blood. 2024;144(10):1083–1092. PMID 38820500; DOI 10.1182/blood.2024023962<br><strong>Design/population:</strong> Open-label randomised phase II, two-by-two design; N=373 treatment-naive, 87% aged 60 or over; median follow-up 7.5 years<br><strong>Verified extraction:</strong> Bortezomib addition median PFS 6.4 versus 5.5 years, HR 0.90 (90% CI 0.70–1.16); lenalidomide maintenance median PFS 7.2 versus 5.9 years, HR 0.84 (90% CI 0.62–1.15); both randomised comparisons negative<br><strong>Integrity:</strong> V2.1; abstract-level; no correction or retraction found; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S36"><strong>S36:</strong> Wang M et al. First-line ibrutinib plus venetoclax for non-blastoid mantle cell lymphoma in patients aged 65 years or older or with TP53 mutations. Blood. 2026. PMID 42462092; DOI 10.1182/blood.2025032833<br><strong>Design/population:</strong> Open-label first-line cohort of the phase III SYMPATICO study; N=78 treated<br><strong>Verified extraction:</strong> Complete response 69%, overall response 95%, median PFS 40.2 months, 3-year OS 79%; TP53-mutated aged ≥65 complete response 44%, median PFS 22.0 months, 3-year OS 66%; TP53-mutated aged &lt;65 complete response 73%, median PFS 15.4 months<br><strong>Integrity:</strong> V2.1; abstract-level; single-arm open-label cohort; no editorial notice found; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S37"><strong>S37:</strong> van Meerten T et al. Brexucabtagene autoleucel for BTK-inhibitor-naive relapsed or refractory mantle cell lymphoma: primary analysis of ZUMA-2 cohort 3. Blood. 2026. PMID 41160777; DOI 10.1182/blood.2025029734<br><strong>Design/population:</strong> Phase II, registered NCT04880434 (cohort 1 was NCT02601313); 95 enrolled, 86 infused; data cut 26 November 2023; median follow-up 15.5 months<br><strong>Verified extraction:</strong> Treated set overall response 91%, complete response 73%, 12-month PFS 75% and OS 90%; enrolled set overall response 82%; grade 3 or higher treatment-related events 88%; four grade 5 treatment-related events<br><strong>Integrity:</strong> V2.1; abstract-level; single-arm; basis of the United States conversion to full approval; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S38"><strong>S38:</strong> Wang M et al. Ibrutinib plus venetoclax in relapsed or refractory mantle cell lymphoma (SYMPATICO): a multicentre, randomised, double-blind, placebo-controlled, phase 3 study. Lancet Oncol. 2025;26(2):200–213. PMID 39914418; DOI 10.1016/S1470-2045(24)00682-X<br><strong>Design/population:</strong> Randomised double-blind placebo-controlled phase III; N=267; one to five prior lines; median follow-up 51.2 months<br><strong>Verified extraction:</strong> Median PFS 31.9 months (95% CI 22.8–47.0) versus 22.1 months (16.5–29.5), HR 0.65 (0.47–0.88), p=0.0052; grade 3–4 neutropenia 31% versus 11%<br><strong>Integrity:</strong> V2.1-CORRECTED; published correction Lancet Oncol 2025;26(5):e238, DOI 10.1016/S1470-2045(25)00210-4, PMID 40318652, correction content not retrieved; a final analysis is published as Br J Haematol 2026, PMID 42438219, whose abstract was not retrievable; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S39"><strong>S39:</strong> Handunnetti SM et al. Seven-year outcomes of venetoclax-ibrutinib therapy in mantle cell lymphoma: durable responses and treatment-free remissions. Blood. 2024. PMID 38662991; DOI 10.1182/blood.2023023388<br><strong>Design/population:</strong> Phase II AIM study; N=24, of whom 23 relapsed or refractory<br><strong>Verified extraction:</strong> 7-year PFS 30% (95% CI 14–49) and OS 43% (23–62); eight patients in MRD-negative complete response entered elective treatment interruption, four recurred<br><strong>Integrity:</strong> V2.1; abstract-level; very small single-arm cohort; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S40"><strong>S40:</strong> Budde LE et al. Mosunetuzumab plus polatuzumab vedotin in relapsed or refractory mantle cell lymphoma after BTK-inhibitor therapy: a phase 2 study. Blood. 2026. PMID 42013019; DOI 10.1182/blood.2025032422<br><strong>Design/population:</strong> Multicentre phase II; N=42; median three prior lines; 26% prior CAR-T; TP53 aberrant 48%<br><strong>Verified extraction:</strong> Overall response 88.1% (74.4–96.0), complete response 78.6% (63.2–89.7), median PFS 18.6 months at median follow-up 15.9 months; cytokine release syndrome 42.9%, all grade 1–2<br><strong>Integrity:</strong> V2.1; abstract-level; single-arm; neither agent licensed for mantle cell lymphoma in any checked jurisdiction; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S41"><strong>S41:</strong> Fischer L et al. The addition of bortezomib to rituximab, high-dose cytarabine and dexamethasone in relapsed or refractory mantle cell lymphoma: a randomised, open-label phase III trial of the European MCL Network. Leukemia. 2024. PMID 38678093; DOI 10.1038/s41375-024-02254-2<br><strong>Design/population:</strong> Randomised open-label phase III; N=128<br><strong>Verified extraction:</strong> Median time to treatment failure 12 versus 2.6 months (p=0.045); overall response 63% versus 45% (p=0.049); complete response 42% versus 19% (p=0.0062); greater grade 3 or higher haematological toxicity<br><strong>Integrity:</strong> V2.1; abstract-level; no correction or retraction found; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S42"><strong>S42:</strong> Eyre TA, Bishton M, McCulloch R et al. Diagnosis and management of mantle cell lymphoma: a British Society for Haematology guideline. Br J Haematol. 2023;204(1):108–126. PMID 37880821; DOI 10.1111/bjh.19131<br><strong>Design/population:</strong> United Kingdom society clinical guideline<br><strong>Verified extraction:</strong> Current British Society for Haematology mantle cell lymphoma guideline; first three authors verified against the indexed record on 30 July 2026<br><strong>Integrity:</strong> V2.1; identity verified by PMID and DOI; predates the mature TRIANGLE analysis, ECHO, lisocabtagene maraleucel in mantle cell lymphoma and the 2025 EHA–EU guideline; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S43"><strong>S43:</strong> Lymphomas: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. Ann Oncol. 2025. PMID 40774601<br><strong>Design/population:</strong> European society clinical guideline covering seven systemic lymphomas including mantle cell lymphoma<br><strong>Verified extraction:</strong> Citation identity verified; <strong>mantle cell lymphoma recommendation text was not retrievable</strong> (source returned HTTP 403) and no ESMO recommendation is quoted anywhere in this guideline<br><strong>Integrity:</strong> V2.1; identity only; supersedes the 2017 ESMO mantle cell lymphoma guideline; NEW IN v2.1</li>
"""

anchor_ref = '    </ol>'
idx = h.find('id="reference-S31"')
if idx < 0:
    sys.exit('S31 reference not found')
close_ol = h.find('</ol>', idx)
if close_ol < 0:
    sys.exit('closing ol not found')
h = h[:close_ol] + NEW_REFS + h[close_ol:]

# -------------------------------------------------- evidence boundary update
h = must(h,
  '<p>Scientific extraction is abstract-only except for the verified full text of S01 (PMCID PMC12541557) and the PubMed-linked VALERIA correction notice.</p>',
  """<p>Scientific extraction is abstract-only except for the verified full text of S01 (PMCID PMC12541557), the PubMed-linked VALERIA correction notice, and the published Department of Error for S25.</p>
    <p><strong>Resolved since v2.0.</strong> The StiL erratum (S25, DOI 10.1016/S0140-6736(13)60801-6) has been retrieved and read. It makes two numerical corrections to the primary report: in Table 1, prognostic groups by FLIPI, the intermediate-risk figure in the bendamustine–rituximab group should read 57/139 (41%); and in the Results, the overall response rate in the R-CHOP group should read 231 (91%) of 253. Both are typographical and neither alters the non-inferiority conclusion. The v2.0 note that the substantive correction was not retrieved is now closed.</p>
    <p><strong>Still unresolved.</strong> The sonrotoclax erratum (S20C, PMID 42447415, DOI 10.1200/JCO-26-01699) carries no abstract in PubMed, Europe PMC or scite, and the publisher returned HTTP 403. What was corrected in S20 remains unknown, so every sonrotoclax figure in this document is quoted from a record known to have been corrected in an unknown respect. Manual retrieval of the publisher PDF is required before ratification.</p>
    <p><strong>Editorial-notice audit.</strong> All records S01 to S31 were re-checked on 30 July 2026. No retraction and no expression of concern affects any of them. Linked comment articles were identified for S04, S17, S24, S25, S29 and S31; comments are commentary, not corrections, and do not change the extracted findings. New records S32 to S43 were checked on the same basis, with one correction identified and recorded against S38.</p>
    <p><strong>Evidence not admitted.</strong> Topline MANGROVE results circulating through company communication and secondary reporting have been excluded because no peer-reviewed primary publication was retrievable. Conference abstracts, including preclinical proteasome and BTK-degrader material, have been excluded from the ledger. No figure from an excluded source appears anywhere in this document.</p>""")

# ------------------------------------------------------- release control
h = must(h, '<td>MHA-MCL-2026-v2.0</td>', '<td>MHA-MCL-2026-v2.1-DRAFT</td>')
h = must(h, '<td>PREVIEW</td>', '<td>DRAFT — NOT FOR CLINICAL USE</td>')
h = h.replace('<td>2026-07-28</td>', '<td>2026-07-30</td>')
h = must(h, '<td>PASS</td>', '<td>PENDING — not yet performed for v2.1 content</td>')
h = must(h, '<td>COMPLETE — IDENTITY RETAINED PRIVATELY</td>',
            '<td>PENDING — v2.0 verification does not extend to v2.1 additions</td>')
h = must(h, '<td>TRUE — 29 JULY 2026</td>', '<td>FALSE — no publication authority</td>')
h = must(h, '<td>TRUE</td>', '<td>PENDING — owner scope approval for v2.1 not yet given</td>')

# ----------------------------------------------------- sidebar and footer
h = must(h, '<strong>Mohsin Haematology Academy</strong> · Accountable owner: Dr Muhammad Mohsin, Consultant Haematologist · MHA-MCL-2026-v2.0 · published guideline',
            '<strong>Mohsin Haematology Academy</strong> · Accountable owner: Dr Muhammad Mohsin, Consultant Haematologist · MHA-MCL-2026-v2.1-DRAFT · unratified working draft, not for clinical use')

# sidebar table of contents additions
h = must(h, '<li><a href="#jurisdictions">12. Regulatory and access boundary</a></li>',
            '<li><a href="#jurisdictions">12. Regulatory and access boundary</a></li>\n          <li><a href="#evidence-model">13. Evidence-to-recommendation model</a></li>\n          <li><a href="#trials">14. Clinical trials</a></li>')

# downloads in sidebar: neutralise v2.0 artefact links (no v2.1 artefacts exist)
h = re.sub(r'<ul class="artefact-links">.*?</ul>',
  '<ul class="artefact-links"><li>No v2.1 artefacts have been generated. The published v2.0 downloads are deliberately not linked from this draft to prevent a reader mixing draft text with ratified files.</li></ul>',
  h, flags=re.S)

# the algorithm is still the v2.0 artefact and now contradicts the corrected text
h = re.sub(r'<figure>\s*<a class="mobile-algorithm-link".*?</figure>',
  """<div class="changed"><strong>The algorithm has not been regenerated for v2.1</strong>
      <p>The published v2.0 diagram is deliberately not displayed here. It encodes the v2.0 statements on the NICE positions for the TRIANGLE regimen, pirtobrutinib and brexucabtagene autoleucel, three of which this draft has corrected or withdrawn. Displaying it beside the corrected text would put a contradiction in front of the reader.</p>
      <p>Regeneration is a required step before ratification, through the single node model that generates the SVG and the Excalidraw scene together, followed by the parity test. Until then there is no v2.1 algorithm.</p>
    </div>""",
  h, flags=re.S)

# remove the orphaned v2.0 publication-model paragraph now duplicated inside the draft banner
h = must(h, '<p><strong>Publication model:</strong> England access framework with separate devolved-nation notes. Clinical evidence and access status are deliberately presented as separate determinations.</p>', '')

# number the remaining sidebar TOC entries for consistency
h = must(h, '<li><a href="#access-status">Regulatory and access matrix</a></li>', '<li><a href="#access-status">15. Regulatory and access matrix</a></li>')
h = must(h, '<li><a href="#evidence-references">Evidence references</a></li>', '<li><a href="#evidence-references">17. Evidence references</a></li>')
h = must(h, '<li><a href="#release-control">Release control</a></li>', '<li><a href="#release-control">18. Release control</a></li>')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s  bytes=%d' % (OUT, len(h)))
