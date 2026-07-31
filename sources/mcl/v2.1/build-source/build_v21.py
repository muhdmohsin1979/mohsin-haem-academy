#!/usr/bin/env python3
"""Build MCL v2.1 DRAFT from the v2.0 CLL-prototype HTML.

Preserves the CLL prototype styling and structure verbatim. Applies targeted
section replacements, inserts two new sections, updates the access matrix and
extends the evidence ledger.
"""
import re, sys, io

SRC = '/mnt/user-data/uploads/mcl-pr-bundle-v1.5.2/mcl-v2.0-cll-prototype-r2.html'
OUT = '/home/claude/mcl-v2.1-draft.html'

h = io.open(SRC, encoding='utf-8').read()
orig_len = len(h)


def replace_section(html, sec_id, new_html):
    """Replace a <section id="..."> block, PRESERVING its original opening tag
    (which carries data-clinical-unit and claims-traceability attributes)."""
    pat = re.compile(r'(<section id="%s"[^>]*>).*?</section>' % re.escape(sec_id), re.S)
    m = pat.search(html)
    if not m:
        sys.exit('SECTION NOT FOUND: %s' % sec_id)
    open_tag = m.group(1)
    # strip the opening tag from the supplied replacement and reuse the original
    inner = re.sub(r'^<section id="[^"]*"[^>]*>', '', new_html.strip())
    return html[:m.start()] + open_tag + inner + html[m.end():]


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:120])
    return html.replace(needle, repl, n)


# ---------------------------------------------------------------- head / meta
h = must(h,
    '<meta name="description" content="Mantle Cell Lymphoma guideline v2.0 — Mohsin Haematology Academy. Evidence, marketing authorisation, NICE recommendation and NHS England commissioning recorded as separate determinations, with devolved-nation notes.">',
    '<meta name="description" content="Mantle Cell Lymphoma guideline v2.1 draft — Mohsin Haematology Academy. Unratified working draft. Evidence, marketing authorisation, HTA recommendation and NHS England commissioning recorded as separate determinations, with United Kingdom and non-United Kingdom positions demarcated throughout.">')

h = must(h, '<meta name="robots" content="index, follow">',
            '<meta name="robots" content="noindex, nofollow">')

h = must(h, '<title>Mantle Cell Lymphoma guideline v2.0</title>',
            '<title>Mantle Cell Lymphoma guideline v2.1 — unratified draft</title>')

# ------------------------------------------------------------- extra styling
h = must(h, '    @media (max-width:420px) { .flow-split { grid-template-columns:1fr; } }',
    """    @media (max-width:420px) { .flow-split { grid-template-columns:1fr; } }

    /* v2.1 additions */
    .draft-banner { border:3px solid #8b2e2e; background:#fff1f3; padding:1rem 1.2rem; margin-bottom:1.25rem; }
    .jx { border-left:5px solid #b08538; background:#fdf8ee; padding:.7rem .95rem; margin:.85rem 0; }
    .jx > strong:first-child { display:block; color:#7a5a15; font:700 .74rem/1.3 Arial,sans-serif; text-transform:uppercase; letter-spacing:.07em; margin-bottom:.35rem; }
    .uk { border-left:5px solid var(--navy); background:#eef2f7; padding:.7rem .95rem; margin:.85rem 0; }
    .uk > strong:first-child { display:block; color:var(--navy); font:700 .74rem/1.3 Arial,sans-serif; text-transform:uppercase; letter-spacing:.07em; margin-bottom:.35rem; }
    .changed { border-left:5px solid var(--red); background:#fff1f3; padding:.7rem .95rem; margin:.85rem 0; }
    .changed > strong:first-child { display:block; color:#8b2e2e; font:700 .74rem/1.3 Arial,sans-serif; text-transform:uppercase; letter-spacing:.07em; margin-bottom:.35rem; }
    .tbl-wrap { overflow-x:auto; margin:1rem 0; }
    .tbl-wrap table { min-width:640px; font-size:.9rem; }
    .tier { display:inline-block; padding:.1rem .42rem; border-radius:4px; font:700 .74rem/1.5 Arial,sans-serif; color:white; }
    .tier.a { background:#2e6b3e; } .tier.b { background:#3d6b8b; } .tier.c { background:#b08538; }
    .tier.d { background:#8a6a4f; } .tier.e { background:#707070; }
    .pri { display:inline-block; padding:.1rem .42rem; border:1px solid var(--line); border-radius:4px; font:700 .74rem/1.5 Arial,sans-serif; background:#eef2f7; color:var(--navy); }
    .trial-id { font:600 .82rem/1.4 Arial,sans-serif; }
    .status-card.alert { border-top-color:var(--red); }""")

# --------------------------------------------------------------- anchor nav
h = must(h,
    '      <a href="#jurisdictions">12. Regulatory and access boundary</a>\n'
    '      <a href="#access-status">Regulatory and access matrix</a>\n'
    '      <a href="#evidence-references">Evidence references</a>\n'
    '      <a href="#release-control">Release control</a>',
    '      <a href="#jurisdictions">12. Regulatory and access boundary</a>\n'
    '      <a href="#evidence-model">13. Evidence-to-recommendation model</a>\n'
    '      <a href="#trials">14. Clinical trials</a>\n'
    '      <a href="#access-status">15. Regulatory and access matrix</a>\n'
    '      <a href="#evidence-references">17. Evidence references</a>\n'
    '      <a href="#release-control">18. Release control</a>')

# --------------------------------------------------------------------- hero
h = must(h,
    '  <span class="preview">PUBLISHED 29 JULY 2026</span>\n'
    '  <h1>Mantle Cell Lymphoma v2.0</h1>\n'
    '  <p>MHA-MCL-2026-v2.0 · evidence and access cut-off 2026-07-28</p>',
    '  <span class="preview">DRAFT — NOT FOR CLINICAL USE</span>\n'
    '  <h1>Mantle Cell Lymphoma v2.1</h1>\n'
    '  <p>MHA-MCL-2026-v2.1-DRAFT · evidence and access cut-off 2026-07-30 · supersedes nothing until ratified</p>')

# ------------------------------------------------------------ warning banner
old_warn_start = h.find('<aside class="warning" role="note" aria-labelledby="preview-warning-heading">')
old_warn_end = h.find('</aside>', old_warn_start) + len('</aside>')
if old_warn_start < 0:
    sys.exit('warning aside not found')
h = h[:old_warn_start] + """<aside class="draft-banner" role="note" aria-labelledby="draft-warning-heading">
    <strong id="draft-warning-heading">Unratified working draft. Not for clinical use.</strong>
    <p>This is a revision candidate prepared for the accountable owner. Independent clinical review is <strong>PENDING</strong> and pharmacy verification is <strong>PENDING</strong> for all material added since v2.0. It carries no publication authority and must not be used to make a treatment or funding decision. The published guideline remains v2.0.</p>
    <p>Every statement of marketing authorisation, HTA recommendation and commissioning status below must be re-checked against the official source before ratification. Where a v2.0 statement could not be reproduced against the live source on 30 July 2026, the change is marked with a <strong>changed since v2.0</strong> block giving the reason.</p>
    <p><strong>Publication model:</strong> England access framework with separate devolved-nation notes. United Kingdom and non-United Kingdom positions are demarcated throughout: blocks headed <strong>outside the United Kingdom</strong> describe evidence or regulatory status in other jurisdictions and <em>never</em> establish a route to treatment for a patient in the United Kingdom.</p>
  </aside>""" + h[old_warn_end:]

# ============================================================ SECTION 1 scope
h = replace_section(h, 'scope', """<section id="scope">
    <h2>1. Scope and use</h2>
    <p>This specialist guideline covers adult mantle cell lymphoma from diagnosis through first-line and relapsed or refractory treatment. It separates clinical evidence, marketing authorisation, HTA recommendation and operational NHS access.</p>
    <p>It is not a prescribing instruction, commissioning decision or substitute for the current SmPC, live national criteria, local SACT governance, MDT review and patient-specific judgement.</p>
    <div class="uk"><strong>How to read the jurisdiction markers</strong>
      <p>This revision records evidence and regulatory positions from outside the United Kingdom because international divergence in mantle cell lymphoma is now large enough to mislead a reader working from an overseas algorithm. Two rules apply without exception.</p>
      <p>First, a block headed <strong>outside the United Kingdom</strong> is context only. A United States or European Union approval does not create a Great Britain marketing authorisation, a NICE recommendation or an NHS England commissioning route, and must never be used to justify treatment here.</p>
      <p>Second, where international practice and United Kingdom practice diverge, the divergence is stated explicitly rather than smoothed over. The three divergences that most affect reading of an overseas source are set out in section 12.</p>
    </div>
    <div class="uk"><strong>Relationship to the current United Kingdom society guideline</strong>
      <p>The British Society for Haematology guideline on the diagnosis and management of mantle cell lymphoma remains the current United Kingdom society document (2023; PMID 37880821; DOI 10.1111/bjh.19131). It predates the mature TRIANGLE analysis, the ECHO readout and acalabrutinib–bendamustine–rituximab licensing, lisocabtagene maraleucel in mantle cell lymphoma and the 2025 EHA–EU guideline. Where this document differs from BSH 2023, the difference reflects evidence published after that guideline and is identified in section 13. This document does not replace, and has no standing against, the BSH guideline.</p>
    </div>
  </section>""")

# =================================================== SECTION 5 first-line fit
h = replace_section(h, 'first-line-fit', """<section id="first-line-fit">
    <h2>5. First-line pathway for younger or treatment-fit adults</h2>
    <p>Select treatment according to biological risk, treatment requirement, physiological fitness and suitability for dose-intensive treatment or ASCT—not chronological age alone.</p>
    <h3>Current conventional pathway when first-line covalent BTK inhibition is not routinely commissioned</h3>
    <p>Offer rituximab plus high-dose cytarabine-containing induction followed by ASCT consolidation and 3 years of rituximab maintenance. This is a bundled strategy: the MCL Younger trial does not isolate the independent effect of ASCT. Use the current network SACT/transplant protocol for the exact induction, conditioning, doses, administration and modifications.</p>
    <p>After ASCT, the LYMA schedule was rituximab 375 mg/m² every 2 months for 3 years. It improved 4-year EFS, PFS and OS versus observation; prolonged follow-up retained the PFS benefit without a statistically significant OS difference. Confirm the current rituximab SmPC and local protocol before prescribing.</p>
    <p>Substitution of obinutuzumab for rituximab in a transplant-eligible pathway has been studied prospectively in LyMa-101 with propensity-matched comparison against LYMA controls (S32). The comparison is not randomised, the matched analysis is susceptible to residual confounding, and obinutuzumab has no mantle cell lymphoma marketing authorisation. Do not substitute outside a trial.</p>
    <h3>TRIANGLE-derived pathway</h3>
    <p>The mature TRIANGLE analysis applies to adults aged 18–65 who matched that protocol. Adding ASCT to the studied ibrutinib-containing regimen did not improve failure-free survival, while ibrutinib-containing arms improved reported overall survival versus control and increased infection burden.</p>
    <p>The exact ibrutinib regimen has a GB marketing authorisation. The NICE appraisal remains unfinished and no final guidance exists.</p>
    <div class="changed"><strong>Changed since v2.0 — NICE status for the TRIANGLE regimen</strong>
      <p>v2.0 stated that a June 2026 NICE draft guidance recommends not using this regimen. On 30 July 2026 the live project page for GID-TA11802 / ID6596 records the status as <em>in progress</em> with expected publication <em>TBC</em>, and a timeline running to an invitation to participate on 3 November 2025. No committee meeting, no consultation on draft guidance and no draft guidance document are shown, and a targeted search of the project documents returned only the draft scope, the draft matrix and the final scope. <strong>The claim that a negative June 2026 draft recommendation exists could not be reproduced and has been withdrawn from this draft.</strong> The document tab returned an HTTP 403 to automated retrieval, so absence is not proof; the accountable owner should open the page directly before ratification.</p>
    </div>
    <p>Do not present this pathway as routinely commissioned NHS treatment. If it is used through an authorised funding route, follow the exact SmPC regimen and do not add routine ASCT solely because the patient was initially transplant-eligible.</p>
    <p>Rituximab maintenance within a TRIANGLE-derived pathway is recommended by the EHA–EU guideline, but the supporting TRIANGLE maintenance analysis was non-randomised and recorded more serious infection. It must not be represented as a risk-free default.</p>
    <p>Circulating tumour DNA and circulating tumour cell dynamics were measured prospectively within TRIANGLE (S33). Molecular response was faster in ibrutinib-containing arms and the excess risk carried by TP53 mutation appeared attenuated relative to the control arm. This is an exploratory biomarker substudy in a subset, it does not establish that TP53-associated risk has been removed, and it must not be used to justify withholding trial referral.</p>
    <div class="uk"><strong>Long-run outcome context</strong>
      <p>A pooled individual-patient analysis of six randomised phase III trials conducted between 1996 and 2020 (S34) recorded a substantial improvement in survival for patients aged 65 or under with advanced-stage disease: median overall survival 4.9 years in the earliest treatment era, 13.8 years in the middle era, and not reached in the most recent, with 5-year overall survival rising from 49% to 84%. The same analysis recorded a far smaller gain in older and transplant-ineligible patients, from 3.8 to 4.8 years. Use this to frame prognosis honestly at diagnosis, and note that the gain is concentrated in the population this section covers.</p>
    </div>
    <div class="jx"><strong>Outside the United Kingdom — first-line ibrutinib</strong>
      <p>The regulatory position on ibrutinib in mantle cell lymphoma diverges sharply and this is the single most important reason not to read an overseas first-line algorithm directly.</p>
      <p><strong>United States:</strong> the ibrutinib mantle cell lymphoma indication was <em>withdrawn</em>. The manufacturer requested voluntary withdrawal of the accelerated approval on 6 April 2023 and the Federal Register withdrawal was effective 18 December 2023. A current United States algorithm therefore contains no ibrutinib option in mantle cell lymphoma at any line.</p>
      <p><strong>European Union:</strong> the ibrutinib mantle cell lymphoma indications are retained, including the TRIANGLE-derived first-line regimen for adults who would be eligible for autologous stem-cell transplantation, and relapsed or refractory monotherapy.</p>
      <p><strong>United Kingdom:</strong> a GB marketing authorisation covers the first-line regimen, and ibrutinib remains routinely commissioned in the relapsed setting after exactly one previous line under TA502. A United Kingdom clinician therefore has an option that a United States clinician does not.</p>
    </div>
  </section>""")

# ================================================= SECTION 6 first-line older
h = replace_section(h, 'first-line-older', """<section id="first-line-older">
    <h2>6. First-line pathway for older or transplant-ineligible adults</h2>
    <p>Treatment selection should integrate disease tempo, TP53 status, frailty, renal function, infection risk, cardiac and bleeding risk, drug interactions, treatment duration, patient preference and confirmed access.</p>
    <h3>Clinically actionable options</h3>
    <ul>
      <li><strong>Bendamustine–rituximab:</strong> offer as a standard first-line immunochemotherapy option when clinically appropriate, followed in responders by rituximab maintenance for at least 2 years. The BR comparison in StiL was a mixed indolent/MCL population, and maintenance-after-BR evidence includes observational data; retain those limits. Use the current local/network SACT protocol for exact doses and modifications.</li>
      <li><strong>VR-CAP:</strong> consider as an alternative for previously untreated adults for whom HSCT is unsuitable. It improved PFS versus R-CHOP but caused more neutropenia and thrombocytopenia. NICE TA370 recommends it within its marketing authorisation. Rituximab maintenance for at least 2 years is an EHA–EU guideline recommendation and was not tested in the original VR-CAP trial.</li>
      <li><strong>R-BAC:</strong> rituximab, bendamustine and cytarabine has single-arm prospective long-term follow-up in previously untreated older patients, with complete response 91%, 7-year PFS 55% and OS 63% and no maintenance given. It is a recognised option in this population but has no randomised comparison against BR and no regimen-specific technology appraisal; haematological toxicity is greater than with BR and dose attenuation in the frail is essential.</li>
    </ul>
    <h3>Two additions that the randomised evidence does not support</h3>
    <p>E1411 randomised 373 previously untreated patients, 87% aged 60 or over, in a two-by-two design (S35). Adding bortezomib to bendamustine–rituximab induction did not improve progression-free survival (median 6.4 versus 5.5 years; hazard ratio 0.90, 90% CI 0.70–1.16). Adding lenalidomide to rituximab maintenance did not improve progression-free survival (median 7.2 versus 5.9 years; hazard ratio 0.84, 90% CI 0.62–1.15). Both randomised questions were negative at 7.5 years of follow-up. Do not add either agent to a bendamustine–rituximab platform outside a trial.</p>
    <h3>Trial evidence that does not create routine NHS England access</h3>
    <ul>
      <li><strong>ENRICH:</strong> ibrutinib–rituximab improved PFS over the pooled immunochemotherapy control but did not establish superiority over BR specifically. No first-line NICE or national CDF route was identified.</li>
      <li><strong>ECHO:</strong> acalabrutinib plus BR improved PFS without a demonstrated OS advantage. It is licensed in Great Britain, but NICE GID-TA11091 / ID6155 remains unfinished. Draft guidance published for consultation on 25 February 2026 did <em>not</em> recommend the combination, on the stated basis that there is not enough evidence to determine whether it offers value for money in this population; consultation ran to 18 March 2026. The displayed expected publication date of 4 June 2026 has passed, and the project note records that <q>following on from advice received from the company this appraisal will be rescheduled to align with latest regulatory expectations</q>. Draft guidance is not final guidance.</li>
      <li><strong>SHINE:</strong> ibrutinib plus BR improved PFS without an OS advantage and increased grade 3–4 toxicity. No first-line NICE or national CDF route was identified. A pre-specified secondary analysis reports longer progression-free survival among patients achieving complete response, which is a prognostic association within responders and not evidence of an overall survival gain.</li>
      <li><strong>Ibrutinib–venetoclax in an older or TP53-mutated first-line population:</strong> the open-label first-line cohort of SYMPATICO treated 78 patients aged 65 or over, or younger with TP53 mutation, with non-blastoid disease (S36). Complete response was 69%, overall response 95%, median progression-free survival 40.2 months and 3-year overall survival 79%. The combination has <strong>no Great Britain mantle cell lymphoma marketing authorisation</strong>, and the NICE appraisal was suspended on 20 January 2026 because an MHRA application was no longer being pursued. This is an important dataset with no route to the patient in England outside a trial.</li>
    </ul>
    <div class="jx"><strong>Outside the United Kingdom — first-line acalabrutinib with bendamustine–rituximab</strong>
      <p>Acalabrutinib with bendamustine and rituximab is approved for previously untreated transplant-ineligible mantle cell lymphoma in the <strong>United States</strong> (16 January 2025, full approval on the ECHO trial) and in the <strong>European Union</strong> (European Commission approval 6 May 2025). At the same date the United States converted the relapsed or refractory acalabrutinib monotherapy accelerated approval to traditional approval.</p>
      <p>In <strong>England</strong> the combination is licensed but has no final NICE recommendation and no demonstrated national commissioning route. A clinician reading a United States or European treatment algorithm will find this regimen presented as a first-line standard; it is not routinely available here.</p>
    </div>
  </section>""")

# ================================================== SECTION 7 TP53 / high risk
h = replace_section(h, 'high-risk', """<section id="high-risk">
    <h2>7. TP53-mutated and other high-risk MCL</h2>
    <p>TP53-mutated disease should prompt early specialist discussion, explicit communication of uncertainty and consideration of an appropriate clinical trial. BOVen and other response-adapted novel combinations show activity and feasibility, but available single-arm studies do not prove comparative superiority or elimination of TP53-associated risk.</p>
    <p>Prospective data continue to show that TP53 mutation remains adverse under targeted therapy rather than being neutralised by it. In the first-line SYMPATICO cohort (S36), patients aged 65 or over <em>without</em> TP53 mutation achieved complete response 76%, median progression-free survival 40.2 months and 3-year overall survival 85%. In the same study, patients aged 65 or over <em>with</em> TP53 mutation achieved complete response 44%, median progression-free survival 22.0 months and 3-year overall survival 66%; younger patients with TP53 mutation achieved complete response 73% but median progression-free survival of only 15.4 months. A regimen can produce a high response rate in TP53-mutated disease and still deliver markedly shorter disease control.</p>
    <p>MRD may refine prognosis and has been used to guide treatment cessation in selected studies. It is not a universal surrogate and does not justify omission of effective maintenance in routine practice.</p>
    <p>Molecular risk beyond TP53 continues to be defined. In the FIL V-RBAC biomarker analysis of 132 evaluable patients, <em>ATM</em> was the most frequently mutated gene at 41.7%, ahead of <em>TP53</em> and <em>KMT2D</em> at 23.5% each; <em>ATM</em> deletion was present in 24% and <em>CDKN2A</em> loss in 22%. These are prognostic associations within one trial population and do not yet direct treatment selection.</p>
    <div class="jx"><strong>Outside the United Kingdom — society position on first-line TP53-mutated disease</strong>
      <p>The 2025 EHA–EU mantle cell lymphoma network guideline recommends that conventional chemoimmunotherapy is inadequate in TP53-mutated disease and favours first-line combinations of an anti-CD20 antibody with a BTK inhibitor and a BCL2 inhibitor, with strong encouragement of trial enrolment. <strong>No such combination holds a Great Britain mantle cell lymphoma marketing authorisation.</strong> Venetoclax is not authorised for mantle cell lymphoma in the United Kingdom, the European Union or the United States. In England this recommendation is deliverable only inside a clinical trial, and the guideline recommendation must not be read as evidence that a funding route exists.</p>
    </div>
  </section>""")

# ================================================== SECTION 8 relapsed pathway
h = replace_section(h, 'relapsed', """<section id="relapsed">
    <h2>8. Relapsed or refractory pathway</h2>
    <p>At each relapse, record prior regimens and classes, depth and duration of response, reason for stopping, current disease tempo, performance status, organ function, infection history and access constraints. Distinguish covalent-BTKi intolerance from progression.</p>
    <h3>Options with a routine England route</h3>
    <ul>
      <li>After exactly one previous line in England, ibrutinib and zanubrutinib have separate positive NICE recommendations subject to their exact criteria. TA1081 states that <q>zanubrutinib can be used as an option to treat relapsed or refractory mantle cell lymphoma in adults who have had 1 line of treatment only</q> and directs clinicians to <q>use the least expensive option of the suitable treatments (including zanubrutinib and ibrutinib), having discussed the advantages and disadvantages of the available treatments with the person with the condition</q>. Both are subject to their commercial arrangements.</li>
      <li>At covalent-BTKi progression, assess cellular-therapy eligibility and refer early where appropriate. Manufacturing time and bridging risk must be considered. The access position for cellular therapy is changing and is set out immediately below.</li>
    </ul>
    <h3>Cellular therapy — a live access question</h3>
    <p>At 67.8 months median follow-up in ZUMA-2 cohort 1, median duration of response with brexucabtagene autoleucel was 36.5 months and median overall survival 46.5 months. Cohort 3 of the same study subsequently treated 86 BTK-inhibitor-naive patients and reported overall response 91%, complete response 73% and 12-month progression-free survival 75%, with grade 3 or higher treatment-related events in 88% and four grade 5 treatment-related events (S37). United Kingdom intention-to-treat data record material attrition between approval and infusion and 24-month non-relapse mortality of 25%, mainly infection.</p>
    <div class="changed"><strong>Changed since v2.0 — the TA677 review is at appeal, not merely &ldquo;continuing&rdquo;</strong>
      <p>v2.0 stated only that TA677 remains a Cancer Drugs Fund managed-access recommendation while review continues. The review is <strong>GID-TA11545 / ID6325</strong>, and on 30 July 2026 its recorded timeline is: committee meeting 1 on 1 July 2025; draft guidance consultation 23 July to 13 August 2025; committee meeting 2 on 2 September 2025; <strong>final draft guidance 24 December 2025 to 21 January 2026</strong>; <strong>appeal 30 March 2026</strong>; <strong>appeal decision published 9 June 2026</strong>. Expected publication remains TBC and no final guidance has been issued.</p>
      <p>The consultation document records the committee conclusion that brexucabtagene autoleucel <q>could not be recommended for treating relapsed or refractory mantle cell lymphoma</q>, having accepted clinical effectiveness but found cost-effectiveness estimates <q>substantially above the range NICE normally considers to be a cost-effective use of NHS resources</q>. A United Kingdom Government answer of 26 January 2026 confirms that NICE <q>has been unable to recommend the treatment in the final draft guidance</q> and records a safeguard under which patients who started treatment during managed access may continue.</p>
      <p><strong>The content of the 9 June 2026 appeal decision was not retrievable</strong> and the outcome is therefore unknown to this draft. TA677 remains live at the cut-off. Counsel patients about the possibility that routine access changes, do not promise a durable route, and confirm the live position with the commissioning team before referral.</p>
    </div>
    <p>Lisocabtagene maraleucel has phase I activity after BTKi exposure with overall response 83.1% among 88 infused patients, but no demonstrated routine MCL route in England at the access cut-off; NICE GID-TA11930 is awaiting development.</p>
    <h3>Options with evidence but no routine England route</h3>
    <ul>
      <li><strong>Pirtobrutinib</strong> has single-arm activity after covalent BTKi exposure, with overall response 57.8% and median duration of response 21.6 months in BRUIN. There is no demonstrated national MCL commissioning route.</li>
      <li><strong>Ibrutinib with venetoclax</strong> now has randomised evidence in the relapsed setting. SYMPATICO was a double-blind placebo-controlled phase III trial in 267 patients with one to five prior lines (S38); median progression-free survival was 31.9 months versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia in 31% versus 11%. Seven-year follow-up of the AIM study additionally documents durable remission and elective treatment interruption in a small MRD-negative subgroup (S39). <strong>None of this creates access:</strong> there is no Great Britain mantle cell lymphoma marketing authorisation for the combination and the NICE appraisal was suspended on 20 January 2026 because an MHRA application was no longer being pursued.</li>
      <li><strong>Glofitamab</strong> has fixed-duration phase I/II activity after prior BTKi, with overall response 85% and 74.2% among BTKi-exposed patients, but no current MCL marketing authorisation or routine commissioning route. The referable route in the United Kingdom is the GLOBRYTE randomised phase III trial — see section 14.</li>
      <li><strong>Sonrotoclax</strong> has phase I/II monotherapy activity after anti-CD20 and covalent BTKi exposure, with overall response 52.4% and median progression-free survival 6.5 months in the corrected report. There is no Great Britain licence. The referable route in the United Kingdom is the CELESTIAL-RRMCL randomised phase III trial — see section 14.</li>
      <li><strong>Mosunetuzumab with polatuzumab vedotin</strong> reported a phase II study in 42 patients after BTK-inhibitor therapy, 26% of whom had prior CAR-T and 48% of whom had TP53 aberration (S40): overall response 88.1%, complete response 78.6% and median progression-free survival 18.6 months, with cytokine release syndrome in 42.9%, all grade 1–2. This is a small single-arm study and neither agent is licensed for mantle cell lymphoma in any jurisdiction surveyed.</li>
      <li><strong>Bortezomib added to rituximab, high-dose cytarabine and dexamethasone</strong> was tested in a randomised open-label phase III trial of the European MCL Network in 128 patients, improving median time to treatment failure from 2.6 to 12 months with greater grade 3 or higher haematological toxicity. It has no regimen-specific technology appraisal in this setting.</li>
      <li>Do not use unadjusted cross-trial response rates to rank pirtobrutinib, cellular therapy, bispecific antibodies or investigational BCL2 inhibition.</li>
    </ul>
    <div class="changed"><strong>Changed since v2.0 — pirtobrutinib is subject to two NICE appraisals, and the one v2.0 cites is suspended</strong>
      <p>v2.0 stated that GID-TA10858 / ID3975 returned to the NICE work programme on 14 July 2026 and remains in progress. On 30 July 2026 the live project page records the status as <strong>Suspended</strong>, with the last timeline entry dated 29 March 2024: <q>The company has informed NICE that it will not provide an evidence submission for this appraisal.</q> Expected publication is TBC and no later event is shown. <strong>The v2.0 statement could not be reproduced and has been withdrawn.</strong></p>
      <p>Separately, a <strong>second and distinct</strong> appraisal exists that v2.0 does not record: <strong>GID-TA11639 / ID6493, pirtobrutinib for treating relapsed or refractory mantle cell lymphoma untreated with a BTK inhibitor</strong>. Its status is <em>awaiting development</em>; topic selection is recorded in October 2024, referral in December 2024 and April 2025, and a note of 31 July 2025 records that the appraisal was rescheduled and anticipated to start during early March 2026. Note the population: this second appraisal covers patients who have <em>not</em> had a BTK inhibitor, which is not the licensed post-BTKi population.</p>
    </div>
    <div class="jx"><strong>Outside the United Kingdom — relapsed and refractory divergence</strong>
      <p><strong>Ibrutinib:</strong> withdrawn for mantle cell lymphoma in the United States; retained in the European Union; routinely commissioned in England after exactly one line under TA502.</p>
      <p><strong>Zanubrutinib:</strong> approved in the United States under accelerated approval for relapsed or refractory disease after at least one prior therapy, and recommended by NICE under TA1081 in England. <strong>Not authorised for mantle cell lymphoma in the European Union at all.</strong> A European algorithm will not contain it.</p>
      <p><strong>Pirtobrutinib:</strong> United States accelerated approval 27 January 2023 after at least two lines including a BTK inhibitor; European Union conditional marketing authorisation 30 October 2023 after previous BTK-inhibitor treatment. Great Britain authorisation exists; no national commissioning route.</p>
      <p><strong>Brexucabtagene autoleucel:</strong> converted to <em>full</em> United States approval on 2 April 2026 on the strength of ZUMA-2 cohort 3; conditional European Union authorisation. In England the position is the unresolved TA677 review described above — an unusual divergence in which the evidence base strengthened internationally while the domestic funding route came under challenge.</p>
      <p><strong>Lisocabtagene maraleucel:</strong> United States accelerated approval 30 May 2024; European Commission approval of the mantle cell lymphoma extension 24 November 2025.</p>
      <p><strong>Sonrotoclax:</strong> United States accelerated approval <strong>13 May 2026</strong> for adults with relapsed or refractory mantle cell lymphoma after at least two lines of systemic therapy including a BTK inhibitor — the first BCL2 inhibitor approved in mantle cell lymphoma in any jurisdiction. No European Union authorisation and no Great Britain licence were identified. United Kingdom access is through trial entry only.</p>
      <p><strong>Glofitamab and epcoritamab:</strong> neither holds a mantle cell lymphoma indication in the United States or the European Union. Use in mantle cell lymphoma is investigational everywhere; a diffuse large B-cell lymphoma licence must never be extrapolated.</p>
    </div>
  </section>""")

print('sections replaced OK, length now %d (was %d)' % (len(h), orig_len))
io.open('/home/claude/_stage1.html', 'w', encoding='utf-8').write(h)
