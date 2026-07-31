#!/usr/bin/env python3
"""Stage 10: apply the independent audit findings of 30 July 2026.

Two corrections reverse changes this build made earlier and were wrong.
"""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'
AUD = ('verified by independent audit on 30 July 2026 from the official NICE document; '
       'this document&rsquo;s own automated retrieval returned HTTP 403 and could not reproduce it')


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:180])
    return html.replace(needle, repl, n)


# =============================================== 1. TRIANGLE — restore and correct
h = must(h,
  '<div class="changed"><strong>Changed since v2.0 — NICE status for the TRIANGLE regimen</strong>',
  '<div class="changed"><strong>Corrected 30 July 2026 — the June 2026 draft guidance does exist</strong>')

h = re.sub(
  r'<p>v2\.0 stated that a June 2026 NICE draft guidance recommends not using this regimen\..*?before ratification\.</p>',
  '<p><strong>An earlier revision of this draft withdrew the v2.0 statement that a June 2026 draft recommendation exists. That withdrawal was wrong and has been reversed.</strong> The withdrawal rested on the absence of any draft-guidance entry in an automated read of the project page, together with an HTTP 403 on the documents tab. Absence from a partial page render was treated as evidence of absence, and it should not have been.</p>'
  '<p>An independent audit on 30 July 2026 retrieved the official document. <strong>NICE published draft guidance on 30 June 2026</strong> for GID-TA11802 / ID6596, whose recommendation 1.1 states that the specified ibrutinib-containing regimen <q>should not be used</q> for untreated adult mantle cell lymphoma when autologous stem-cell transplantation is suitable.</p>'
  '<p><strong>This is draft guidance, not final guidance.</strong> It creates no NICE funding mandate and it is not a final negative recommendation. The appraisal remains in development. Check the live project status before ratification. Source: nice.org.uk/guidance/gid-ta11802/documents/draft-guidance (' + AUD + ').</p>',
  h, count=1, flags=re.S)

h = must(h,
  '<p>The exact ibrutinib regimen has a GB marketing authorisation. The NICE appraisal remains unfinished and no final guidance exists.</p>',
  '<p>The exact ibrutinib regimen has a GB marketing authorisation. The NICE appraisal remains in development, and draft guidance of 30 June 2026 says the regimen should not be used in this population. No final guidance exists, so there is no funding mandate either way.</p>')

# matrix card
h = re.sub(
  r'<p><strong>NICE:</strong> GID-TA11802/ID6596 remains in progress; expected publication TBC\..*?confirm directly before ratification\.</p>',
  '<p><strong>NICE:</strong> GID-TA11802/ID6596 remains in development; expected publication TBC. <strong>Draft guidance published 30 June 2026 states that this regimen <q>should not be used</q></strong> for untreated adult mantle cell lymphoma when ASCT is suitable. Draft guidance is not final guidance and creates no funding mandate. Source: nice.org.uk/guidance/gid-ta11802/documents/draft-guidance (' + AUD + ').</p>',
  h, count=1, flags=re.S)

# =========================================== 2. TA677 appeal — outcome is known
APPEAL = ('<div class="changed"><strong>Corrected 30 July 2026 — the appeal decision is retrievable and the outcome is known</strong>'
  '<p>An earlier revision said the 9 June 2026 appeal decision could not be retrieved and its outcome was unknown. <strong>That is no longer defensible.</strong> The decision is published on the NICE project documents page and was downloaded and read during an independent audit on 30 July 2026.</p>'
  '<p>The appeal panel <strong>upheld</strong> the appeal point concerning transparency and scrutiny of the NHS England CAR-T delivery tariff, raised by both the company and the patient organisations, and <strong>upheld</strong> the point that use of the McCulloch comparator data was unreasonable in the analysis performed. The remaining appeal points were <strong>dismissed</strong>. The appraisal was <strong>remitted to the appraisal committee</strong> for further consideration.</p>'
  '<p><strong>What this does and does not mean.</strong> It does not mean brexucabtagene autoleucel has received a positive final NICE recommendation. It does not mean routine access has ceased. It does mean the previous final-draft conclusion cannot be treated as the final outcome, that the appraisal is in progress following remittal, and that no final guidance has been issued. TA677 remains live. Confirm the current Cancer Drugs Fund and Blueteq position before referral. Source: nice.org.uk/guidance/gid-ta11545/documents/appeal-decision.</p>'
  '</div>')

h = re.sub(
  r'<div class="changed"><strong>Changed since v2\.0 — the TA677 review is at appeal.*?</div>',
  APPEAL, h, count=1, flags=re.S)

# every remaining "unresolved / unknown" surface
h = h.replace('<strong>The appeal decision content was not retrievable and the outcome is unknown to this draft.</strong>',
              '<strong>The appeal was upheld in part and the appraisal remitted to the committee; no final guidance has been issued.</strong>')
h = h.replace('appeal decision published 9 June 2026, outcome unresolved',
              'appeal decision published 9 June 2026 — upheld in part, appraisal remitted to committee')
h = h.replace('<strong>The appeal decision content was not retrievable and the outcome is unknown to this draft.</strong> ', '')
h = h.replace('review at appeal, outcome unresolved', 'review remitted to committee after part-upheld appeal')
h = h.replace('<strong>TA677 review at appeal; outcome unresolved.</strong>',
              '<strong>TA677 review remitted to committee after a part-upheld appeal; no final guidance.</strong>')
h = h.replace('<strong>R2 CDF — review at appeal</strong>', '<strong>R2 CDF — review remitted after appeal</strong>')
h = h.replace('and that route is currently under challenge at appeal',
              'and that route is unresolved — the review was remitted to committee after a part-upheld appeal')
h = h.replace('THE REVIEW IS AT APPEAL — final draft guidance did not recommend; appeal decision published 9 June 2026, outcome unresolved. Confirm the live position before referral and do not promise a durable route.',
              'THE REVIEW IS UNRESOLVED — final draft guidance did not recommend; the 9 June 2026 appeal was upheld in part on tariff transparency and comparator method, and the appraisal was remitted to committee. No final guidance. Confirm the live position before referral.')

# ================================= 3. Pirtobrutinib — record the page discrepancy
h = re.sub(
  r'<div class="changed"><strong>Changed since v2\.0 — pirtobrutinib is subject to two NICE appraisals.*?</div>',
  '<div class="changed"><strong>Corrected 30 July 2026 — the v2.0 statement was substantially right</strong>'
  '<p>An earlier revision of this draft said the v2.0 claim that GID-TA10858 / ID3975 returned to the NICE work programme on 14 July 2026 <q>could not be reproduced</q> and withdrew it. <strong>That withdrawal was wrong.</strong> An independent audit on 30 July 2026 read the live project page and found a timeline entry dated <strong>14 July 2026</strong>: <q>In progress. Appraisal scheduled back into the work programme, anticipated to begin in late September 2026.</q></p>'
  '<p><strong>The official page is internally inconsistent, and both facts should be recorded.</strong> Its headline status reads <em>In progress</em>, while its timeline still carries the entry of 29 March 2024 stating that the company would not provide an evidence submission and that the appraisal was suspended. Describing the appraisal simply as &ldquo;suspended&rdquo; is therefore incomplete, and so is describing it simply as active.</p>'
  '<p>This document&rsquo;s own automated retrieval continued to return a page showing status <em>Suspended</em> with no entry later than 29 March 2024, on repeated attempts. That is recorded here so the discrepancy is visible rather than silently resolved. <strong>Open the page directly before ratification.</strong></p>'
  '<p>Separately, a <strong>second and distinct</strong> appraisal exists that v2.0 does not record: <strong>GID-TA11639 / ID6493, pirtobrutinib for relapsed or refractory mantle cell lymphoma untreated with a BTK inhibitor</strong>, status <em>awaiting development</em>. Its timeline carries entries dated 26 March 2026 and 1 July 2026, and the 26 March entry anticipates the appraisal beginning in <strong>late October 2026</strong>. Note the population: that appraisal covers patients who have <em>not</em> had a BTK inhibitor, which is not the licensed post-BTKi indication.</p>'
  '</div>',
  h, count=1, flags=re.S)

h = re.sub(
  r'<p><strong>NICE:</strong> Two separate appraisals\..*?licensed post-BTKi indication\.</p>',
  '<p><strong>NICE:</strong> Two separate appraisals. <strong>GID-TA10858/ID3975</strong> (relapsed or refractory mantle cell lymphoma): the official page carries a headline status of <em>In progress</em> and a timeline entry of 14 July 2026 recording that the appraisal was <q>scheduled back into the work programme, anticipated to begin in late September 2026</q>, while the same timeline retains the 29 March 2024 suspension entry. Both are recorded because the page is internally inconsistent. <strong>GID-TA11639/ID6493</strong> (relapsed or refractory disease <em>untreated with a BTK inhibitor</em>) is awaiting development, with entries dated 26 March 2026 and 1 July 2026 and an anticipated start in late October 2026. That second appraisal covers a different population from the licensed post-BTKi indication.</p>',
  h, count=1, flags=re.S)

h = h.replace('one appraisal suspended, one awaiting development',
              'one in progress after remittal to the work programme, one awaiting development')
h = h.replace('One NICE appraisal suspended on company non-submission, a second in a BTKi-untreated population awaiting development.',
              'One appraisal carries an inconsistent official status — headline in progress, timeline retaining a 2024 suspension. A second, in a BTKi-untreated population, is awaiting development.')
h = h.replace('One appraisal suspended on non-submission, a second in a BTKi-untreated population awaiting development. Do not transpose the CLL route.',
              'Official status inconsistent — see the access matrix. A second appraisal covers a BTKi-untreated population. Do not transpose the CLL route.')

# ============================================ 4. CDF list version
h = h.replace('these were confirmed against list version 1.401 dated 29 May 2026.',
              'the current national list is version <strong>1.405</strong>. Form versions and eligibility wording must be read from the live list rather than assumed unchanged from the version 1.401 entries recorded during drafting.')

# ============================================ 5. IVIG eligibility condition
h = must(h,
  '<tr><td>Immunoglobulin replacement</td><td>Where IgG is below 400 mg/dL: <q>400–500 mg/kg IVIG q 3–4 weeks or 100–200 mg/kg q 1–2 weeks subcutaneous</q>.',
  '<tr><td>Immunoglobulin replacement</td><td>For patients with IgG below 400 mg/dL <strong>and severe or recurrent infections, particularly sinopulmonary infections</strong> — a low IgG alone is not the trigger: <q>400–500 mg/kg IVIG q 3–4 weeks or 100–200 mg/kg q 1–2 weeks subcutaneous</q>, following local immunology and pharmacy protocols.')

# ======================================= 6. anti-CD20 overgeneralisation
h = must(h,
  'Every mantle cell lymphoma regimen in this guideline contains an anti-CD20 antibody, and a positive hepatitis B result changes management',
  'Every immunochemotherapy regimen in this guideline contains an anti-CD20 antibody, and screening applies before any of them. It also applies before treatments carrying their own reactivation or immunosuppression risk, including BTK inhibitors and cellular therapy. A positive hepatitis B result changes management')

# ======================================= 7. relapse ASCT absolute
h = must(h,
  '<p>Two conditions do the work in that sentence: standard risk, and chemosensitive disease. It is not an option for TP53-mutated disease, and it is not an option for disease that has not responded to salvage.</p>',
  '<p>Two conditions do the work in that sentence: standard risk, and chemosensitive disease. The recommendation is directed at standard-risk, chemosensitive disease and should not be extrapolated into a routine recommendation for TP53-mutated or otherwise high-risk disease. It is not a stated contraindication either — such cases need individual expert review and, wherever possible, trial consideration. Chemosensitivity remains a separate requirement in its own right.</p>')

# ======================================= 8. TRIANGLE ASCT categorical claim
h = must(h,
  '<p>The mature TRIANGLE analysis applies to adults aged 18–65 who matched that protocol. Adding ASCT to the studied ibrutinib-containing regimen did not improve failure-free survival, while ibrutinib-containing arms improved reported overall survival versus control and increased infection burden.</p>',
  '<p>The mature TRIANGLE analysis applies to adults aged 18–65 who matched that protocol. <strong>In the overall trial population</strong>, adding ASCT to the studied ibrutinib-containing regimen did not demonstrate an additional failure-free survival advantage, while ibrutinib-containing arms improved reported overall survival versus control and increased infection burden.</p>'
  '<p>Do not apply that overall result categorically to every biologically high-risk patient. An <strong>unplanned subgroup analysis</strong> suggested a possible benefit from ASCT in high-risk disease. It is unplanned and hypothesis-generating, so it does not establish a benefit either — but it is a reason to keep individual biological risk in the decision rather than treating the headline result as settling it.</p>')

# ======================================= 9. re-biopsy "single mechanism"
h = must(h,
  '<p>This is the single mechanism by which transformation to blastoid or pleomorphic disease is detected. Treating a relapse on the biology of the original diagnostic sample means treating a disease the patient may no longer have.</p>',
  '<p>Clinical behaviour and imaging can raise the suspicion of transformation; histology is what confirms it. Treating a relapse on the biology of the original diagnostic sample means treating a disease the patient may no longer have.</p>')

# ======================================= 10. sonrotoclax erratum consistency
h = h.replace('with overall response 52.4% and median progression-free survival 6.5 months in the corrected report.',
              'with overall response 52.4% and median progression-free survival 6.5 months. <strong>An erratum has been published against that report and the corrected field could not be established from accessible metadata, so these figures are not finally verified.</strong>')
h = h.replace('<td>Phase I/II; erratum content unresolved. United States approved, no Great Britain licence.',
              '<td>Phase I/II. <strong>Figures not finally verified — an erratum is published and its content is unresolved.</strong> United States approved, no Great Britain licence.')
h = h.replace('A published erratum exists whose substantive correction has not been retrieved.',
              '<strong>A published erratum exists and the field corrected could not be established from accessible metadata. These results must not be treated as finally verified until the correction notice has been reviewed, and must not be used to rank sonrotoclax against other options.</strong>')

# ======================================= 11. company schemes — attestation label
h = h.replace('<strong>An AstraZeneca early access scheme is supplying this combination to United Kingdom patients, attested by the accountable owner on 30 July 2026</strong>',
              '<strong>OWNER-ATTESTED LOCAL OR NON-ROUTINE ROUTE — independent documentary verification pending.</strong> An AstraZeneca early access scheme is reported as supplying this combination to United Kingdom patients, attested by the accountable owner on 30 July 2026. This is not a demonstrated national access route')
h = h.replace('<strong>A Johnson &amp; Johnson scheme is supplying this regimen to United Kingdom patients, attested by the accountable owner on 30 July 2026</strong>',
              '<strong>OWNER-ATTESTED LOCAL OR NON-ROUTINE ROUTE — independent documentary verification pending.</strong> A Johnson &amp; Johnson scheme is reported as supplying this regimen to United Kingdom patients, attested by the accountable owner on 30 July 2026. This is not a demonstrated national access route')

h = must(h,
  '<p>This is recorded on the direct attestation of the accountable owner.',
  '<p><strong>Both are recorded as OWNER-ATTESTED, not as demonstrated national access routes, and must not be described as routine United Kingdom or NHS availability.</strong> Before ratification the private scheme documentation should be reviewed and bound to the candidate, recording: scheme document identity; date checked; applicable nations and trusts; exact eligibility; supply duration; closure and continuation provisions; the accountable private verifier; and a document hash or controlled evidence reference. If that documentation cannot be reviewed, these statements belong in a clearly non-authoritative local operational annex rather than in the public guideline.</p>'
  '<p>This is recorded on the direct attestation of the accountable owner.')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
