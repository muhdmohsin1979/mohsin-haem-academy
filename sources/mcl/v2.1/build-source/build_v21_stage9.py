#!/usr/bin/env python3
"""Stage 9: fertility, frailty, bridging and CAR-T referral, salvage ASCT,
tumour flare, supportive care detail, surveillance schedule, palliative care."""
import sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:170])
    return html.replace(needle, repl, n)


# ===================================================== §6 fertility counselling
h = must(h,
  'Confirm the current rituximab SmPC and local protocol before prescribing.</p>',
  """Confirm the current rituximab SmPC and local protocol before prescribing.</p>
    <div class="do"><strong>Before starting — fertility</strong>
      <p>Offer fertility counselling, and referral for preservation where appropriate, before any patient of reproductive age starts cytarabine-containing induction or proceeds to transplantation. BSH grades this <strong>1B</strong> (S42) — a strong recommendation.</p>
      <p>These are gonadotoxic regimens. The conversation has to happen before treatment starts, not at the point the patient asks about it afterwards. Record that it took place and what was decided, including where the patient declined.</p>
    </div>""")

# ================================================== §7 frail-patient pathway
h = must(h,
  '<h3>Two additions that the randomised evidence does not support</h3>',
  """<h3>The frail patient is a separate question</h3>
    <div class="do"><strong>In practice</strong>
      <p>Assess frailty with a <strong>formal tool</strong>, not an impression. Consider geriatrician review and pre-phase steroids. Where cytotoxic treatment is still appropriate, use an attenuated regimen rather than a full-dose one the patient cannot finish.</p>
    </div>
    <p>&ldquo;Older or transplant-ineligible&rdquo; and &ldquo;frail&rdquo; are not the same thing, and treating them as one category is how frail patients end up on regimens designed for fitter ones. Median age at diagnosis is around 70, so this is not a small subgroup.</p>
    <p>BSH advises that <q>formal frailty assessment tools are preferred over informal methods as they are more sensitive</q> (S42), and names three: the <strong>Geriatric 8</strong>, a three-to-five minute screen; the <strong>Cumulative Illness Rating Scale for Geriatrics</strong>; and the <strong>Geriatric Assessment in Haematology</strong>, developed specifically for haematological malignancy and taking ten to fifteen minutes.</p>
    <p>Two graded BSH recommendations follow, both 2B. Consider <q>review by a geriatrician and pre-phase steroids for frail patients with MCL</q>. And where cytotoxic therapy remains appropriate, consider <q>R-chlorambucil, R-CVP, attenuated R-bendamustine or attenuated R-CHOP</q>.</p>
    <p>Frailty is not a reason to withhold treatment, and it is not a reason to give full-dose treatment either. It is a reason to choose differently, and to say why in the notes.</p>
    <h3>Two additions that the randomised evidence does not support</h3>""")

# ========================== §9 bridging, referral timetable, flare, salvage ASCT
h = must(h,
  '<h3>Sequencing cellular therapy, and what happens when it fails</h3>',
  """<h3>Getting a patient to cellular therapy</h3>
    <div class="do"><strong>In practice</strong>
      <p>Discuss high-risk patients with a CAR-T centre at <strong>first relapse</strong>, not later. Review them at least <strong>four-weekly, face to face, for the first three months</strong>. Image at <strong>8 to 12 weeks</strong>. Do not stop a covalent BTK inhibitor abruptly. Avoid bendamustine if cellular therapy is a realistic plan.</p>
    </div>
    <p>The commonest reason a patient does not receive CAR-T is that the disease progresses while arrangements are being made. The operational steps below are the ones that change that, and they come from BSH (S42) and the EBMT cellular therapy guidance (S46).</p>
    <p><strong>Referral and review.</strong> BSH advises that <q>high-risk patients should be discussed with a CAR T-cell centre at first relapse and followed closely: at least 4-weekly face-to-face appointments in the first 3 months</q>. Patients with significant constitutional symptoms not improving after four weeks of a BTK inhibitor should have early re-imaging. All high-risk patients should have a first imaging response assessment <q>as early as 8 weeks but no later than 12 weeks</q>.</p>
    <p><strong>Do not stop a BTK inhibitor abruptly.</strong> BSH warns that <q>abrupt cessation of ibrutinib at this stage should be avoided due to risk of tumour flare</q>. EBMT advises maintaining BTK inhibition through leukapheresis where the patient is still responding. If you are planning to switch, plan the overlap.</p>
    <p><strong>Choose bridging with the right goal.</strong> EBMT states the aim plainly: <q>treatment goal of holding/bridging is symptom control and keeping the patient stable rather than achieving minimal tumour load prior to CART</q>. Trying to debulk aggressively before infusion is not the objective and may cost more than it gains.</p>
    <p><strong>Avoid bendamustine where you can.</strong> BSH notes it should be avoided <q>due to its potential impact on T-cell fitness</q>. This matters at the point you are choosing a bridging regimen, and it is a reason to think about the eventual CAR-T plan earlier in the disease course than feels necessary.</p>
    <div class="uk"><strong>Predicting how long a second-line BTK inhibitor will last</strong>
      <p>The EHA–EU guideline describes a <strong>BTKi-MIPI</strong> to estimate treatment duration on a second-line covalent BTK inhibitor (S01). Its purpose is practical: identify in advance the patients likely to need something else within a short period, so that the next step can be arranged rather than improvised, and so that the BTK inhibitor is not stopped abruptly with the flare risk that carries.</p>
    </div>
    <h3>Autologous transplantation at relapse</h3>
    <p>Autologous transplantation is not only a first-line consolidation question. The EHA–EU guideline records that it <q>may be considered among standard-risk MCL patients (e.g., those lacking a TP53 mutation or biallelic deletion) who have not undergone ASCT in first remission, and in patients with a chemosensitive lymphoma</q> (S01).</p>
    <p>Two conditions do the work in that sentence: standard risk, and chemosensitive disease. It is not an option for TP53-mutated disease, and it is not an option for disease that has not responded to salvage.</p>
    <h3>Sequencing cellular therapy, and what happens when it fails</h3>""")

# ======================================= §12 supportive care operational detail
h = must(h,
  '<p>Before treatment, complete regimen-specific infection, vaccination, viral screening, drug-interaction, bleeding, cardiac, renal and tumour-lysis assessment. Use current local and national supportive-care policies for antimicrobial prophylaxis, immunoglobulin replacement, growth-factor support and vaccination.</p>',
  """<p>Before treatment, complete regimen-specific infection, vaccination, viral screening, drug-interaction, bleeding, cardiac, renal and tumour-lysis assessment. Use current local and national supportive-care policies for antimicrobial prophylaxis, immunoglobulin replacement, growth-factor support and vaccination.</p>
    <div class="do"><strong>Before a BTK inhibitor or an anthracycline</strong>
      <p>Arrange <strong>cardiac evaluation</strong> before starting either (S01). Check renal function. Review anticoagulation and antiplatelet therapy, and review interacting medicines — the BTK-inhibitor SmPCs carry specific dose reductions for concomitant CYP3A4 inhibitors, and those are in the treatment cards.</p>
    </div>
    <h3>After cellular therapy — what the societies specify</h3>
    <p>Your treating centre's protocol governs. The figures below are recorded so that a referring team knows what to expect and can check nothing has been missed at handover. They come from the EHA–EU guideline (S01) unless stated.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Measure</th><th scope="col">What is specified</th></tr></thead>
        <tbody>
          <tr><td>Immunoglobulin replacement</td><td>Where IgG is below 400 mg/dL: <q>400–500 mg/kg IVIG q 3–4 weeks or 100–200 mg/kg q 1–2 weeks subcutaneous</q>. Note EBMT (S46) is more cautious, holding that <q>current evidence is still insufficient to support prophylactic immunoglobulin administration policies</q></td></tr>
          <tr><td>Antiviral prophylaxis</td><td><q>acyclovir 200–400 mg orally twice a day or valaciclovir 500 mg orally twice a day</q></td></tr>
          <tr><td>Pneumocystis prophylaxis</td><td>Co-trimoxazole two to three times weekly</td></tr>
          <tr><td>Duration of antiviral and PJP cover</td><td><strong>See the note below — the societies differ</strong></td></tr>
          <tr><td>Vaccination restart</td><td>COVID-19 and influenza at 3 months; other inactivated vaccines at 6 months; live vaccines not before 1 year</td></tr>
          <tr><td>Viral monitoring</td><td>CMV, EBV and hepatitis B every 3 months for the first 24 months</td></tr>
          <tr><td>Growth factor</td><td>G-CSF until neutrophils exceed 0.5 × 10⁹/L; GM-CSF is not recommended early</td></tr>
          <tr><td>Antibacterial and antifungal</td><td>Fluoroquinolone and fluconazole, or a mould-active azole, where neutropenia is prolonged or the patient is on steroids or a BTK inhibitor</td></tr>
        </tbody>
      </table>
    </div>
    <div class="split"><strong>Where the societies differ — prophylaxis duration</strong>
      <p>EHA specifies pneumocystis prophylaxis <q>for a minimum of 6 months and until CD4 count &gt;200 cells/ml</q>. BSH specifies antiviral and anti-pneumocystis prophylaxis <q>for at least 1 year and until CD4 count &gt;0.2 × 10⁹/L</q>. The CD4 threshold is the same; the minimum duration is not.</p>
      <p><strong>This guideline follows BSH: continue for at least 12 months and until CD4 recovery.</strong> Where a local protocol stops at 6 months, that is defensible against EHA — but record which position was applied rather than leaving it unstated.</p>
    </div>""")

# =========================================== §13 surveillance schedule + no PET
h = must(h,
  '<p>After first-line systemic treatment, continue long-term follow-up with history, examination and laboratory assessment every 3–6 months initially. Document disease status, treatment exposure, response, toxicity, infection, patient priorities and the planned trigger for re-imaging or treatment. Routine surveillance imaging should be clinically directed. Suspected transformation or an unexpectedly aggressive relapse requires prompt re-staging and tissue confirmation where feasible.</p>',
  """<p>After first-line systemic treatment, continue long-term follow-up with history, examination and laboratory assessment. Document disease status, treatment exposure, response, toxicity, infection, patient priorities and the planned trigger for re-imaging or treatment. Suspected transformation or an unexpectedly aggressive relapse requires prompt re-staging and tissue confirmation where feasible.</p>
    <div class="do"><strong>Do not use PET-CT for surveillance</strong>
      <p>The EHA–EU guideline is explicit: <q>PET-CT should not be used for surveillance</q> (S01). Use it to answer a question, not to look for one.</p>
    </div>
    <h3>Surveillance schedule</h3>
    <p>The schedule below is the EHA–EU one (S01). Local practice varies and this is not a mandate, but a stated schedule is easier to audit than &ldquo;clinically directed&rdquo;.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Period after treatment</th><th scope="col">Clinical and laboratory review</th><th scope="col">Imaging</th></tr></thead>
        <tbody>
          <tr><td>First 2 years</td><td>Every 3 to 4 months — history, examination, blood count and differential, chemistry including LDH</td><td>Optional CT or ultrasound every 3 to 6 months</td></tr>
          <tr><td>Years 3 to 5</td><td>Every 6 months</td><td>Optional CT or ultrasound every 6 to 12 months</td></tr>
          <tr><td>Beyond 5 years</td><td>Annually</td><td>Only where progression is suspected</td></tr>
        </tbody>
      </table>
    </div>
    <p>Patients on observation rather than treatment are reviewed every 3 months initially, then every 3 to 6 months, with imaging as clinically required (S01, graded V, B). Where the neck has been irradiated, check thyroid function annually.</p>
    <h3>When treatment is no longer the right answer</h3>
    <p>Some patients will prioritise how they feel over how long they live, and that is a legitimate choice rather than a failure of the pathway. BSH puts it directly: <q>In many cases, patients may prioritise quality of life and symptom relief over prolonging life… best supportive/palliative care (including radiotherapy) may be appropriate, either alongside or instead of systemic anti-cancer therapy</q> (S42).</p>
    <p>Two practical points. Palliative radiotherapy at 2 Gy given twice is effective for symptom control and does not require fitness for systemic treatment — see the limited-stage section. And involving palliative care alongside active treatment is not the same as stopping treatment; saying so plainly to the patient usually helps.</p>""")

# ===================================================== §11 response criteria
h = must(h,
  '<p>Use a pre-specified response-assessment plan appropriate to the regimen and disease sites.',
  '<p>Assess response using the Lugano criteria unless a trial protocol specifies otherwise, and record which criteria were applied. Use a pre-specified response-assessment plan appropriate to the regimen and disease sites.')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
