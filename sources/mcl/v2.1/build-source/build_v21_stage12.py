#!/usr/bin/env python3
"""Stage 12: residual defects from the second audit pass."""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:180])
    return html.replace(needle, repl, n)


def soft(html, needle, repl):
    return html.replace(needle, repl)


# =================================== 1. residual brexu-cel wording
h = soft(h, 'In England the position is the unresolved TA677 review described above',
            'In England, TA677 managed access remains live while the post-managed-access review remains unresolved following a partly upheld appeal and remittal to committee, as described above')
h = soft(h, 'Given the unresolved appeal, confirm the live commissioning position before referral',
            'Given the unresolved post-managed-access review following remittal, confirm the live commissioning position before referral')
h = soft(h, 'and that route is unresolved — the review was remitted to committee after a part-upheld appeal',
            'TA677 managed access remains live, while the post-managed-access review remains unresolved following remittal')
h = soft(h, 'the cellular-therapy route carries an unresolved access position that must be confirmed before referral',
            'the post-managed-access review for the cellular-therapy route remains unresolved following remittal to committee, and the live position must be confirmed before referral')

# =================================== 2. SMC2351 — restore, my withdrawal was wrong
h = re.sub(
  r'<p><strong>Devolved nations:</strong> <strong>The reference &ldquo;SMC2351&rdquo; carried in v2\.0 could not be located.*?endorsed in Northern Ireland in March 2021\.</p>',
  '<p><strong>Devolved nations:</strong> <strong>Corrected 30 July 2026 — an earlier revision wrongly withdrew SMC2351. It exists.</strong> SMC2351, published 9 August 2021, is the Scottish advice for KTE-X19 / Tecartus (brexucabtagene autoleucel) in adults with relapsed or refractory mantle cell lymphoma after two or more systemic therapies including a BTK inhibitor. Check the live advice and any associated restrictions or commercial conditions when determining NHSScotland access. <strong>SMC2548 concerns B-cell precursor acute lymphoblastic leukaemia and must not be substituted for SMC2351.</strong> In Wales the AWTTC record is marked excluded due to NICE appraisal, so TA677 applies; TA677 was endorsed in Northern Ireland in March 2021.</p>',
  h, count=1, flags=re.S)

# =================================== 3. pirtobrutinib — "remittal" misuse
h = soft(h, 'No — one in progress after remittal to the work programme, one awaiting development',
            'No — one appraisal currently displays &ldquo;In progress&rdquo; after being scheduled back into the work programme; a second is awaiting development')
h = soft(h, 'one in progress after remittal to the work programme, one awaiting development',
            'one displays &ldquo;In progress&rdquo; after being scheduled back into the work programme, one awaiting development')

# =================================== 4. TRIANGLE in the jurisdiction table
h = soft(h, '<td>No — appraisal unfinished</td>',
            '<td>No final recommendation — negative draft guidance dated 30 June 2026</td>')

# =================================== 5. lisocabtagene NICE record
h = soft(h, '<p><strong>NICE:</strong> GID-TA11930 is awaiting development; the live page displays conflicting identifiers ID6695 and 12299.</p>',
            '<p><strong>NICE:</strong> GID-TA11930 / ID12299 is awaiting development. A project note dated 3 July 2026 states that appraisal timelines will be available in due course. No NICE recommendation has been issued.</p>')

# =================================== 6. viral monitoring — seropositive only
h = must(h, '<tr><td>Viral monitoring</td><td>CMV, EBV and hepatitis B every 3 months for the first 24 months</td></tr>',
            '<tr><td>Viral monitoring</td><td>In patients <strong>known to be seropositive</strong>, monitor the relevant CMV, EBV or hepatitis B marker every 3 months for the first 24 months. Increase monitoring per the treating centre&rsquo;s protocol if viral levels become detectable. This is not a blanket schedule for every recipient.</td></tr>')

# =================================== 7. antibacterial / antifungal conflation
h = must(h, '<tr><td>Antibacterial and antifungal</td><td>Fluoroquinolone and fluconazole, or a mould-active azole, where neutropenia is prolonged or the patient is on steroids or a BTK inhibitor</td></tr>',
            '<tr><td>Antibacterial</td><td>For prolonged neutropenia, particularly beyond 30 days, and/or long-term corticosteroid treatment, consider antibacterial prophylaxis according to local policy.</td></tr>'
            '<tr><td>Antifungal</td><td>Consider fluconazole or a mould-active azole <strong>only where fungal risk is high</strong>, taking account of severe or prolonged neutropenia, recent transplantation, prolonged corticosteroid exposure and BTK-inhibitor treatment. BTK-inhibitor exposure alone does not trigger prophylaxis. Check drug interactions before prescribing — azoles are CYP3A4 inhibitors and the BTK-inhibitor SmPCs carry specific dose reductions.</td></tr>')

# =================================== 8. elderly CAR-T conclusion
h = must(h,
  '<p>Two findings from that analysis are directly useful at referral. Patients over 75 had outcomes comparable to those aged 70 to 75. And on multivariable analysis <strong>performance status, not age, predicted outcome</strong> — ECOG 2 or worse carried a hazard ratio of 4.50 for overall survival, while age was not independently associated with it. Functional status should drive eligibility assessment rather than a birth date.</p>',
  '<p>Two findings from that analysis are useful at referral, with an important limit on both. Patients over 75 had outcomes comparable to those aged 70 to 75. On multivariable analysis, ECOG performance status of 2 or worse carried a hazard ratio of 4.50 for overall survival, while chronological age within the studied range was not independently associated with outcome.</p>'
  '<p><strong>That does not make age irrelevant to eligibility.</strong> This was a selected cohort of patients aged 70 or over who had already been chosen for brexucabtagene autoleucel, so it cannot answer whether age should influence selection in the first place. Assess age, performance status, comorbidity, disease status and patient preference together, without applying a rigid age cut-off in either direction.</p>')

# =================================== 9. TP53 / SYMPATICO categorical wording
h = must(h,
  '<p>Prospective data continue to show that TP53 mutation remains adverse under targeted therapy rather than being neutralised by it.',
  '<p>Descriptive subgroup outcomes in a small, open-label, non-randomised cohort were poorer in patients with TP53 mutation despite high response rates, which suggests the regimen may not eliminate TP53-associated risk. The analysis does not establish an independent prognostic effect or a comparative treatment benefit, and it should not be read as one.')

h = soft(h, '<td>TP53 mutation remains adverse under BTK inhibitor plus BCL2 inhibitor</td>',
            '<td>TP53-associated risk appears not to be eliminated by BTK plus BCL2 inhibition</td>')
h = soft(h, '<td>High response rate with markedly shorter disease control; median progression-free survival 22.0 months if aged ≥65, 15.4 months if younger.</td>',
            '<td>Descriptive subgroup outcomes only, from a small non-randomised cohort. High response rate with markedly shorter disease control: median progression-free survival 22.0 months if aged ≥65, 15.4 months if younger. No independent prognostic effect established.</td>')

# =================================== 10. bortezomib salvage effect
h = must(h,
  '<li><strong>Bortezomib added to rituximab, high-dose cytarabine and dexamethasone</strong> was tested in a randomised open-label phase III trial of the European MCL Network in 128 patients, improving median time to treatment failure from 2.6 to 12 months with greater grade 3 or higher haematological toxicity. It has no regimen-specific technology appraisal in this setting.</li>',
  '<li><strong>Bortezomib added to rituximab, high-dose cytarabine and dexamethasone</strong> was tested in a randomised open-label phase III trial of the European MCL Network in 128 patients. Median time to treatment failure was 12 versus 2.6 months with a nominal p=0.045, but the MIPI-adjusted hazard ratio was 0.69 (95% CI 0.47–1.02), crossing the null. <strong>The trial was under-recruited: it suggests activity but retains material statistical uncertainty.</strong> Greater grade 3 or higher haematological toxicity. No regimen-specific technology appraisal in this setting.</li>')

h = soft(h, '<td>Randomised phase III, n=128; time to treatment failure 12 versus 2.6 months. No regimen-specific appraisal in this setting.</td>',
            '<td>Randomised phase III, n=128, under-recruited. Time to treatment failure 12 versus 2.6 months, nominal p=0.045, but MIPI-adjusted HR 0.69 (95% CI 0.47–1.02) crosses the null. No regimen-specific appraisal in this setting.</td>')

h = soft(h, 'Median time to treatment failure 12 versus 2.6 months (p=0.045); overall response 63% versus 45% (p=0.049); complete response 42% versus 19% (p=0.0062); greater grade 3 or higher haematological toxicity',
            'Median time to treatment failure 12 versus 2.6 months with nominal p=0.045, but the MIPI-adjusted hazard ratio was 0.69 (95% CI 0.47–1.02), crossing the null; overall response 63% versus 45% (p=0.049); complete response 42% versus 19% (p=0.0062); greater grade 3 or higher haematological toxicity; the trial was under-recruited')

# =================================== 11. StiL S25 integrity contradiction
h = soft(h, 'V2-CORRECTED PubMed/Crossref; published erratum DOI 10.1016/S0140-6736(13)60801-6 identified but substantive correction not retrieved; keep pooled findings qualified',
            'V2.1-CORRECTED; published erratum DOI 10.1016/S0140-6736(13)60801-6 <strong>retrieved and read</strong> — it corrects the intermediate-risk FLIPI count in the bendamustine–rituximab group and the pooled R-CHOP overall-response count; neither correction changes the trial&rsquo;s non-inferiority conclusion. Keep pooled findings qualified because no mantle cell-specific effect is given')

# =================================== 12. re-biopsy absolute in the action box
h = must(h, '<strong>Re-biopsy at every new line of treatment.</strong>',
            '<strong>Re-biopsy whenever possible when a new line of treatment is required</strong>, repeating Ki-67 and TP53 assessment on the new sample.')

# =================================== 13. hepatitis B precision
h = must(h,
  'A positive hepatitis B result changes management — it requires antiviral cover to prevent reactivation. BSH grades this 1C (S42); the EHA–EU guideline makes the same point.</p>',
  'BSH grades screening 1C (S42) and the EHA–EU guideline makes the same point.</p>'
  '<p><strong>What a positive result means depends on which marker is positive.</strong> HBsAg positivity, or evidence of previous exposure including anti-HBc positivity, requires formal reactivation-risk assessment and an antiviral prophylaxis or monitoring plan appropriate to the intended regimen. <strong>Isolated anti-HBs positivity — including vaccine-derived immunity — does not by itself require antiviral treatment.</strong> This requires pharmacy and hepatology verification before ratification.</p>')

# =================================== 14. company-scheme surrounding text
h = soft(h, 'Neither scheme is publicly listed, and the reason for that is set out below — it is a known and expected property of these arrangements rather than a reason to doubt them. Local scheme references, written agreements and pharmacy records are the definitive documentation and are held by the treating trust.',
            'Neither scheme is publicly listed. Public invisibility is a known property of this class of arrangement, but it is not corroboration: the existence, scope, eligibility, duration and continuation terms of these two schemes have <strong>not</strong> been independently verified in this candidate. Any local scheme reference, written agreement or pharmacy record would be the definitive documentation, and none has been reviewed here.')
h = soft(h, 'Between them they cover the whole of first-line mantle cell lymphoma, split at exactly the point section 6 and section 7 already divide on.',
            'The two licensed populations are complementary and non-overlapping, dividing at the same point section 6 and section 7 do. That describes the <em>licences</em>; it does not establish that the two schemes together make treatment available to every first-line patient.')
h = soft(h, 'Equivalent arrangements almost certainly exist elsewhere without leaving a public trace.',
            'Equivalent arrangements may exist elsewhere without leaving a public trace, and this list should not be read as complete.')
h = soft(h, 'A company early access or free-of-charge scheme may exist for any licensed medicine sitting in the gap between marketing authorisation and a NICE recommendation, and by the nature of those arrangements this guideline cannot enumerate them.',
            'A company early access or free-of-charge scheme may exist for a licensed medicine sitting in the gap between marketing authorisation and a NICE recommendation. This guideline cannot enumerate them, and does not assert that any particular one exists.')
h = soft(h, 'A clinician reporting local access to acalabrutinib–bendamustine–rituximab or to a TRIANGLE-derived regimen on a compassionate or free-of-charge basis is <strong>entirely consistent</strong> with the null findings recorded above.',
            'A clinician reporting local access on a compassionate or free-of-charge basis is not contradicted by the null findings recorded above — but neither is such a report corroborated by them.')

h = must(h,
  '<p><strong>Both are recorded as OWNER-ATTESTED, not as demonstrated national access routes,',
  '<p><strong>These are owner-reported local or non-routine arrangements. Their existence, scope, eligibility, duration and continuation terms have not been independently verified in this candidate. They must not be presented as national access routes. Confirm the current written agreement with the relevant company and chief pharmacist before discussing availability with a patient.</strong></p>'
  '<p><strong>Both are recorded as OWNER-ATTESTED, not as demonstrated national access routes,')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
