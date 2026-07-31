#!/usr/bin/env python3
"""Stage 7: close the cellular therapy gaps — allogeneic HCT, post-CAR-T
sequencing, ICANS, and the missing CAR-T evidence records."""
import sys, io
sys.path.insert(0, '/home/claude')

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:170])
    return html.replace(needle, repl, n)


# ============================== section 8: cellular therapy sequencing + allo
CELL = """<h3>Sequencing cellular therapy, and what happens when it fails</h3>
    <p>The EBMT practice harmonisation and guidelines committee published dedicated cellular therapy recommendations for mantle cell lymphoma on 9 July 2026 (S46), developed from an international expert meeting held in Berlin in September 2025 and covering autologous transplantation, allogeneic transplantation and CAR-T together. It is the most specific guidance available on sequencing these modalities and it fills a gap this guideline previously left open.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Setting</th><th scope="col">CAR-T</th><th scope="col">Allogeneic HCT</th></tr></thead>
        <tbody>
          <tr><td>First line</td><td>High-risk disease, <q>only in trials</q>. Standard risk, <q>no role</q>.</td><td><q>No role outside of clinical trials.</q></td></tr>
          <tr><td>Second line, BTK-inhibitor exposed</td><td><q>Clinical option, especially in those patients who progressed while still on BTKi, or within a clinical trial.</q></td><td>Consider as consolidation in salvage-sensitive patients who progressed on BTK-inhibitor-based first-line therapy, where CAR-T is unavailable.</td></tr>
          <tr><td>Beyond second line</td><td>CAR-T-naive: <q>standard of care</q>. CAR-T-exposed: <q>no role for repeat CD19 CART</q>.</td><td><q>Clinical option in salvage-sensitive patients.</q></td></tr>
        </tbody>
      </table>
    </div>
    <div class="changed"><strong>Allogeneic transplantation — the pathway has a terminus</strong>
      <p>Earlier revisions of this guideline stopped after cellular therapy and said nothing about what to do when it fails. That was an omission, and it matters, because allogeneic transplantation is the only remaining modality with curative intent.</p>
      <p>The evidence is thin and much of it is extrapolated. The largest series of allogeneic transplantation after CAR-T failure is in large B-cell lymphoma, not mantle cell lymphoma, and reports 1-year overall survival of 59%, progression-free survival 45% and non-relapse mortality 22% in 88 patients. A Japanese registry analysis of 155 patients transplanted for relapsed or refractory mantle cell lymphoma in the post-ibrutinib era (S51) found autologous and allogeneic transplantation gave comparable median overall survival at 28 and 27 months, with disease status at transplant the dominant predictor for the allogeneic group — relapsed or refractory status carried a hazard ratio of 4.10 and failure to achieve complete remission 3.53.</p>
      <p><strong>The practical instruction is about timing.</strong> Salvage sensitivity and remission status at transplant drive the outcome, so a transplant discussion belongs <em>before</em> CAR-T, at the point of covalent BTK-inhibitor progression, rather than as an afterthought once CAR-T has failed and the patient is out of options and out of fitness. Involve the transplant centre early.</p>
    </div>
    <p>Other options after CAR-T failure are limited. Repeat CD19-directed CAR-T is not recommended. Bispecific antibody therapy has been studied in a population that included prior CAR-T exposure — 26% of the 42 patients in the mosunetuzumab with polatuzumab vedotin study (S40) had received it — but that agent combination is not licensed for mantle cell lymphoma anywhere. Trial entry is frequently the most realistic route.</p>
    <h3>Cellular therapy toxicity and the attrition problem</h3>
    <p>Two toxicity syndromes define the early post-infusion period and both need naming explicitly. <strong>Cytokine release syndrome</strong> and <strong>immune effector cell-associated neurotoxicity syndrome (ICANS)</strong> are graded and managed under the treating centre's own protocols; this guideline does not reproduce them and is not a substitute for them.</p>
    <p>Their frequency in an older population is not trivial. In an EBMT registry analysis of 233 patients aged 70 or over treated with brexucabtagene autoleucel across 96 centres in 13 countries (S47), the 30-day cumulative incidence of any-grade cytokine release syndrome was 80%, grade 3 or higher 9%; for neurotoxicity the figures were 57% and 22%. One-year overall survival was 74%, progression-free survival 62% and non-relapse mortality 13%. Complete remission at day 100 was 78%.</p>
    <p>Two findings from that analysis are directly useful at referral. Patients over 75 had outcomes comparable to those aged 70 to 75. And on multivariable analysis <strong>performance status, not age, predicted outcome</strong> — ECOG 2 or worse carried a hazard ratio of 4.50 for overall survival, while age was not independently associated with it. Functional status should drive eligibility assessment rather than a birth date.</p>
    <p>Attrition between decision and infusion remains the practical constraint. United Kingdom intention-to-treat data record substantial loss between approval and infusion, most often from progressive disease. That is the argument for referring at progression rather than after a further line of therapy, and for planning bridging with the goal, in the EBMT formulation, of <q>symptom control and keeping the patient stable rather than achieving minimal tumour load prior to CART</q>.</p>
    <h3>Options with evidence but no routine England route</h3>"""

h = must(h, '<h3>Options with evidence but no routine England route</h3>', CELL)

# ==================================== section 5: EBMT auto-HCT and MRD position
h = must(h,
  '<p>Substitution of obinutuzumab for rituximab in a transplant-eligible pathway has been studied prospectively in LyMa-101',
  """<div class="uk"><strong>EBMT 2026 position on omitting autologous transplantation</strong>
      <p>The EBMT cellular therapy recommendations (S46) accept that consolidative autologous transplantation may be omitted where minimal residual disease is undetectable at the 10<sup>-6</sup> level after induction, and state that in standard-risk disease treated with a BTK inhibitor <q>omission of auto-HCT should be considered, especially if MRD-negative (10-6) after induction</q>. In high-risk disease treated with a BTK inhibitor, <q>auto-HCT consolidation should be considered, especially if MRD-positive</q>, and in TP53-mutated disease autologous transplantation is recommended <q>only in trials</q>.</p>
      <p>Two cautions before acting on this. It requires MRD assessment at a sensitivity of 10<sup>-6</sup>, which is not uniformly available, and section 9 of this guideline holds that MRD is not a validated universal surrogate. The same document recommends <q>rituximab maintenance (for 3 years) … after first-line consolidative auto-HCT for MCL, irrespective of concurrent BTKi maintenance</q>, which is consistent with the LYMA schedule recorded above.</p>
    </div>
    <p>Substitution of obinutuzumab for rituximab in a transplant-eligible pathway has been studied prospectively in LyMa-101""")

# ============================================== section 10 supportive care link
h = must(h,
  '<p>The MCL efficacy evidence records clinically important infection, cytopenia and treatment-related mortality signals but does not establish one universal prophylaxis schedule. CAR-T and bispecific pathways require their dedicated supportive-care and toxicity-management protocols.</p>',
  '<p>The MCL efficacy evidence records clinically important infection, cytopenia and treatment-related mortality signals but does not establish one universal prophylaxis schedule. CAR-T and bispecific pathways require their dedicated supportive-care and toxicity-management protocols, including graded management of cytokine release syndrome and immune effector cell-associated neurotoxicity syndrome, tocilizumab availability before infusion, and the monitoring and proximity requirements set out in each product SmPC. Section 8 records the observed frequency of both syndromes in an older population and the attrition between referral and infusion.</p>')

# ================================================ new evidence records S46-S51
NEW = """<li class="evidence-reference" id="reference-S46"><strong>S46:</strong> Dreger P, Iacoboni G, Robinson S et al. Cellular therapy in mantle cell lymphoma: recommendations from the EBMT practice harmonisation and guidelines committee. Bone Marrow Transplant. 2026. DOI 10.1038/s41409-026-02963-5<br><strong>Design/population:</strong> International expert consensus recommendations covering autologous HCT, allogeneic HCT and CAR-T; expert meeting held in Berlin 29–30 September 2025; published 9 July 2026<br><strong>Verified extraction:</strong> Sequencing positions for each modality by line of therapy, including no role for repeat CD19-directed CAR-T once CAR-T-exposed, allogeneic HCT as a clinical option in salvage-sensitive patients, and omission of autologous consolidation where MRD is undetectable at 10⁻⁶<br><strong>Integrity:</strong> V2.1; recommendation wording taken from the publisher page on 30 July 2026 and not yet checked against the typeset full text; consensus guidance, not primary trial evidence; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S47"><strong>S47:</strong> Santoro N, Mooyaart J, Novak U et al. Outcomes of patients over 70 years treated with brexu-cel for R/R mantle cell lymphoma: a study from the CTIWP of EBMT. Blood Adv. 2026;10(9):3135–3142. DOI 10.1182/bloodadvances.2025019367<br><strong>Design/population:</strong> Retrospective EBMT registry analysis; N=233 aged 70 or over from 96 centres in 13 countries, 2020–2024; median age at infusion 74.6 years, 44% over 75; 62% prior BTK-inhibitor exposure<br><strong>Verified extraction:</strong> Day-100 complete remission 78% and partial remission 13%; 30-day cumulative incidence any-grade cytokine release syndrome 80% (grade ≥3, 9%) and neurotoxicity 57% (grade ≥3, 22%); 1-year overall survival 74%, progression-free survival 62%, relapse or progression 25%, non-relapse mortality 13%; outcomes in those over 75 comparable to 70–75; ECOG ≥2 strongest predictor of inferior overall survival (HR 4.50) and progression-free survival (HR 3.10), age not independently associated<br><strong>Integrity:</strong> V2.1; abstract-level; retrospective registry, not randomised; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S48"><strong>S48:</strong> Minson A, Hamad N, Cheah CY et al. CAR T cells and time-limited ibrutinib as treatment for relapsed/refractory mantle cell lymphoma: the phase 2 TARMAC study. Blood. 2024;143(8):673–684. DOI 10.1182/blood.2023021306<br><strong>Design/population:</strong> Phase II, NCT04234061; N=20; median 2 prior lines; 50% previously BTK-inhibitor exposed; ibrutinib started before leukapheresis and continued through manufacture and for at least 6 months after infusion<br><strong>Verified extraction:</strong> Primary endpoint met with complete response 80% at 4 months; MRD negativity 70% by flow cytometry and 40% by molecular methods; at median follow-up 13 months estimated 12-month progression-free survival 75% and overall survival 100%; cytokine release syndrome 75% (grade 3 in 20%); reversible grade 1–2 neurotoxicity 10%; efficacy preserved irrespective of prior BTK-inhibitor exposure or TP53 mutation<br><strong>Integrity:</strong> V2.1; abstract-level; small single-arm study; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S49"><strong>S49:</strong> Shah NN, Colina A, Johnson BD et al. Phase I/II study of adaptive manufactured lentiviral anti-CD20/anti-CD19 chimeric antigen receptor T cells for relapsed, refractory mantle cell lymphoma. J Clin Oncol. 2025;43(20):2285–2295. DOI 10.1200/JCO-24-02158<br><strong>Design/population:</strong> Phase I/II, NCT04186520; N=17 infused at 2.5 × 10⁶ cells/kg; on-site manufacture over 8–12 days<br><strong>Verified extraction:</strong> Best overall response 100% (complete response 88%, partial response 12%); phase II day-90 complete response threshold exceeded; two relapses at data cutoff and neither median progression-free nor overall survival reached at median follow-up 15.8 months; cytokine release syndrome 94%, all grade 1–2; neurotoxicity 18%, two reversible grade 3; three non-relapse mortality events, all in the setting of ongoing B-cell aplasia<br><strong>Integrity:</strong> V2.1; abstract-level; very small single-centre cohort; dual-target product not licensed anywhere; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S50"><strong>S50:</strong> Xie Y, Zhou K, Li L et al. Phase 2 study of relmacabtagene autoleucel (CD19 CAR-T) for relapsed/refractory mantle cell lymphoma in Chinese adults. Blood Adv. 2026;10(4):1134–1144. DOI 10.1182/bloodadvances.2024015763<br><strong>Design/population:</strong> Open-label single-arm multicentre phase II, NCT04718883; 70 enrolled, 59 infused at 100 × 10⁶ CAR-positive T cells; 1–9 prior therapies<br><strong>Verified extraction:</strong> 3-month overall response 71.19% (95% CI 57.92–82.24), complete response 59.32% (45.75–71.93); at median follow-up 13.3 months median duration of response 18.1 months, progression-free survival 15.5 months, overall survival 19.5 months; grade ≥3 neutropenia 76.3%, leukopenia 69.5%, lymphopenia 47.5%; severe cytokine release syndrome and neurotoxicity 6.8% each, all resolved; no fatal events<br><strong>Integrity:</strong> V2.1; abstract-level; product not licensed in Great Britain; Chinese population, applicability to United Kingdom practice not established; NEW IN v2.1</li>
<li class="evidence-reference" id="reference-S51"><strong>S51:</strong> Yamasaki S, Shimazu Y, Misaki Y et al. Retrospective analysis of clinical outcomes and risk factors in hematopoietic cell transplantation for relapsed or refractory mantle cell lymphoma in the post-ibrutinib era. Sci Rep. 2026;16(1). DOI 10.1038/s41598-026-47347-3<br><strong>Design/population:</strong> Japanese retrospective registry analysis 2017–2023; N=155 with relapsed or refractory disease; autologous HCT n=105, allogeneic HCT n=50<br><strong>Verified extraction:</strong> Comparable median overall survival, 28 months autologous versus 27 months allogeneic; for autologous HCT age over 60 predicted worse overall survival (HR 2.73); for allogeneic HCT a diagnosis-to-transplant interval of 24 months or less with relapsed or refractory status at transplant (HR 4.10) and non-complete remission (HR 3.53) predicted poorer outcome; no transplant-related mortality among the 10 allogeneic patients receiving ibrutinib<br><strong>Integrity:</strong> V2.1; abstract-level; retrospective and non-randomised; Japanese population; NEW IN v2.1</li>
"""
idx = h.find('id="reference-S45"')
close_ol = h.find('</ol>', idx)
h = h[:close_ol] + NEW + h[close_ol:]

# ---------------------------------------- evidence model: add allo and CAR-T rows
h = must(h,
  '<tr><td>Cross-trial ranking of post-BTKi options</td>',
  '<tr><td>Allogeneic HCT after CAR-T failure</td><td><span class="tier d">D</span></td><td>S46, S51</td><td>R3</td><td><span class="pri">P3</span></td><td>Only remaining modality with curative intent. Largest post-CAR-T series is in large B-cell lymphoma, not mantle cell lymphoma. Salvage sensitivity and remission status at transplant dominate outcome — refer before CAR-T, not after it fails.</td></tr>\n'
  '          <tr><td>Repeat CD19-directed CAR-T after CAR-T failure</td><td><span class="tier e">E</span></td><td>S46</td><td>—</td><td><span class="pri">P4</span></td><td>EBMT 2026: <q>no role for repeat CD19 CART</q> once CAR-T-exposed.</td></tr>\n'
  '          <tr><td>Cross-trial ranking of post-BTKi options</td>')

# ------------------------------------------- quick reference: allo row
h = must(h,
  '<tr><td>Sonrotoclax — CELESTIAL-RRMCL trial</td><td><span class="tier c">C</span></td><td>R5 trial only</td><td><span class="pri">P4</span></td></tr>',
  '<tr><td>Sonrotoclax — CELESTIAL-RRMCL trial</td><td><span class="tier c">C</span></td><td>R5 trial only</td><td><span class="pri">P4</span></td></tr>\n'
  '          <tr><td>Allogeneic HCT after CAR-T failure</td><td><span class="tier g">G</span></td><td>R3 specialist decision</td><td><span class="pri">P3</span></td></tr>')

h = must(h,
  '<p>Brexucabtagene autoleucel is the only cellular therapy with an England route, and that route is currently under challenge at appeal. Confirm before you promise.</p>',
  '<p>Brexucabtagene autoleucel is the only cellular therapy with an England route, and that route is currently under challenge at appeal. Confirm before you promise.</p>\n      <p>Discuss allogeneic transplantation <em>before</em> CAR-T, at covalent BTK-inhibitor progression. Remission status at transplant drives the outcome, and a patient who has already failed CAR-T is usually neither in remission nor fit enough.</p>')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
