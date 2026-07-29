<!--
Independent report provenance: deleg_74e3562e/task-1
Cut-off: 28 July 2026
Status: working evidence input; not publication wording or release approval
Original source: Hermes independent delegation report retained outside the repository
-->

# MCL v2.0 clinical evidence ledger and claim-to-source matrix

**Cut-off:** 28 July 2026, 01:18 BST
**Review type:** targeted, independently verified clinical evidence update; not a formal systematic review.
**Evidence rule:** bibliographic identities were reconciled in live PubMed and Crossref. Numerical and clinical claims below are restricted to PubMed abstracts/records. No model-memory claim was accepted as evidence.

## 1. Scope and eligibility

**Included**

- Mantle cell lymphoma (MCL) diagnosis/risk stratification.
- Prospective or mature evidence for first-line treatment: TRIANGLE, ENRICH and ECHO.
- TP53-mutated or otherwise high-risk MCL.
- MRD-directed and fixed-duration approaches.
- Relapsed/refractory (R/R) disease after covalent BTK inhibitor (cBTKi) exposure.
- Pirtobrutinib, brexucabtagene autoleucel (brexu-cel), lisocabtagene maraleucel (liso-cel), glofitamab and sonrotoclax.
- Maintenance evidence and treatment-related infection/toxicity relevant to supportive care.
- Primary trials were prioritised; guidelines/reviews were retained only for scope or risk-recognition claims.

**Excluded from claim support**

- Conference abstracts without a matched full PubMed record.
- Protocols, laboratory studies, pharmacology papers, case reports, cost-effectiveness studies and indirect comparisons.
- Regulatory claims not established by the included clinical publication.
- Claims available only in inaccessible full text.

---

## 2. Reproducible search log

PubMed E-utilities searches were run live on 28 July 2026 without a date filter, thereby searching the indexed database as it stood at the cut-off. Counts are the live counts returned.

| Search block | Exact PubMed query | Count |
|---|---|---:|
| Diagnosis/risk | `("mantle cell lymphoma"[Title/Abstract]) AND (diagnos* OR risk OR MIPI OR TP53 OR minimal residual disease OR MRD)` | 3,263 |
| TRIANGLE | `("mantle cell lymphoma"[Title/Abstract]) AND (TRIANGLE OR ibrutinib) AND (random* OR phase 3 OR follow-up)` | 154 |
| ENRICH | `("mantle cell lymphoma"[Title/Abstract]) AND (ENRICH OR rituximab ibrutinib) AND (random* OR phase 2 OR phase 3)` | 55 |
| ECHO | `("mantle cell lymphoma"[Title/Abstract]) AND (ECHO OR acalabrutinib) AND (random* OR phase 3)` | 28 |
| TP53/high risk | `("mantle cell lymphoma"[Title/Abstract]) AND (TP53 OR high-risk OR blastoid OR pleomorphic) AND (trial OR cohort OR survival)` | 488 |
| MRD/fixed duration | `("mantle cell lymphoma"[Title/Abstract]) AND (MRD OR "minimal residual disease" OR fixed-duration OR time-limited)` | 209 |
| Post-cBTKi | `("mantle cell lymphoma"[Title/Abstract]) AND (pirtobrutinib OR "covalent BTK" OR "BTK inhibitor exposed" OR "BTK inhibitor failure")` | 92 |
| CAR-T | `("mantle cell lymphoma"[Title/Abstract]) AND (brexucabtagene OR lisocabtagene OR CAR-T OR chimeric antigen receptor)` | 339 |
| Glofitamab | `("mantle cell lymphoma"[Title/Abstract]) AND (glofitamab OR bispecific)` | 70 |
| Sonrotoclax | `("mantle cell lymphoma"[Title/Abstract]) AND (sonrotoclax OR BGB-11417)` | 6 |
| Maintenance/supportive | `("mantle cell lymphoma"[Title/Abstract]) AND (maintenance OR supportive OR infection OR prophylaxis OR vaccination)` | 3,148 |

Additional identity searches included:

- `TRIANGLE mantle cell lymphoma`
- `ENRICH mantle cell lymphoma`
- `ECHO acalabrutinib mantle cell lymphoma`
- `pirtobrutinib covalent BTK inhibitor pretreated mantle cell lymphoma`
- `brexucabtagene mantle cell lymphoma ZUMA-2`
- `lisocabtagene mantle cell lymphoma TRANSCEND`
- `glofitamab mantle cell lymphoma`
- `sonrotoclax mantle cell lymphoma`
- `TP53 mantle cell lymphoma trial`
- `minimal residual disease mantle cell lymphoma trial`
- `rituximab maintenance mantle cell lymphoma randomized`

**Crossref strategy:** every included PubMed DOI was normalised and resolved through the Crossref REST API works endpoint, using the DOI as the path parameter. DOI, title, first author and year were reconciled. Crossref `relation` and `update-to` metadata were checked for corrections and retractions.

---

## 3. Verification summary

| Status | Records |
|---|---:|
| `V2-CONFIRMED` primary/guideline/review records | 23 |
| `V2-CONFIRMED` correction notices | 2 |
| `V1-PUBMED` | 0 |
| `V1-CROSSREF` | 0 |
| `CONFLICT` | 0 |
| Retractions found | 0 |
| Included records with a correction | 2 parent articles |

Two integrity qualifications matter:

1. **VALERIA:** corrected by PMID **39392649**, DOI **10.1182/bloodadvances.2024013955**. The recommended phase II lenalidomide dose is **15 mg**, not 20 mg. The uncorrected dose remains present in the PubMed abstract.
2. **Sonrotoclax:** corrected by PMID **42447415**, DOI **10.1200/JCO-26-01699**. PubMed and Crossref establish the correction relationship, but neither checked metadata record states what was corrected. Its abstract-derived efficacy numbers are therefore flagged as **qualified pending inspection of the correction text/corrected article**.

---

# 4. Clinical evidence synthesis

## 4.1 Diagnosis and risk

- The 2025 EHA–EU MCL Network guideline describes MCL as biologically and clinically heterogeneous and identifies proliferation rate and **TP53** mutation as important biological risk factors. Following independent-review challenge, its verified open full text (PMCID **PMC12541557**) was inspected. It supports the integrated diagnostic criteria, morphology/Ki-67/TP53 assessment, selected observation strategy, re-biopsy at relapse and long-term follow-up statements mapped to C23–C27 [S01].
- A contemporary high-risk review identifies high MIPI plus high Ki-67, blastoid/pleomorphic histology, progression within 24 months, multiple previous lines and molecular lesions including TP53 as high-risk features. This is secondary evidence rather than prospective validation [S02].
- In 183 younger trial patients, TP53 mutation was independently associated with OS (HR **6.2**) and time to relapse (HR **6.9**); median OS was **1.8 years** versus **12.7 years** without TP53 mutation. This was an observational molecular analysis of patients receiving intensive Nordic regimens—not a randomised comparison of TP53-directed strategies [S04].
- The 2026 MIPI53 development study used 143 newly diagnosed real-world patients and external validation in FIL-MCL0208. Reported 5-year PFS was **83.1%, 35.4% and 12.0%** in low-, intermediate- and high-risk groups; corresponding OS was **92.1%, 80.5% and 33.8%**. External OS c-index was **0.732**. It is a prognostic validation study, not evidence that MIPI53-guided treatment improves outcomes [S03].
- The July 2026 V-RBAC biomarker analysis found TP53 and KMT2D mutations in **23.5%** each among 132 evaluable patients. TP53 mutation, CDKN2A loss, CD36 mutation and single-hit ATM abnormalities retained independent PFS associations after adjustment for trial-defined high-risk features. The four-factor model was internally bootstrapped but not externally validated in the abstract [S05].

## 4.2 TRIANGLE: mature 4.5-year evidence

TRIANGLE randomly assigned 870 transplant-eligible patients aged 18–65 years [S06]:

- At median follow-up **54.9 months**, 4-year failure-free survival was:
  - ASCT plus ibrutinib (`A+I`): **82%**
  - Ibrutinib without ASCT (`I`): **81%**
  - Control ASCT (`A`): **70%**
- `A+I` was **not superior** to `I`: HR **0.86**, one-sided p=**0.21**.
- `A+I` remained superior to control: HR **0.63**, p=**0.0026**.
- Control was not superior to `I`: HR **1.45**, p=**0.99**.
- Four-year OS was **88%** (`A+I`), **90%** (`I`) and **81%** (control). Both ibrutinib groups had significantly better OS than control in the reported pairwise analyses.
- Grade 3–5 haematological events during maintenance/follow-up were **54%**, **28%** and **23%**, respectively; infections were **34%**, **26%** and **15%**.
- The abstract-supported conclusion is that adding ASCT to this ibrutinib-containing programme did not add efficacy and increased toxicity. This does not establish equivalence for other BTK inhibitors, induction backbones, ages or high-risk molecular subsets.

A July 2026 non-randomised secondary TRIANGLE analysis compared rituximab maintenance according to national/centre practice [S23]:

- Four-year PFS with versus without maintenance was **85% versus 73%** in arm `I` and **90% versus 75%** in `A+I`.
- Grade 3–5 infections were also higher: **34% versus 11%** in `I` and **41% versus 18%** in `A+I`.
- Because maintenance allocation was not randomised, inverse-probability weighting reduces but does not eliminate confounding. This is supportive—not definitive randomised—evidence for adding rituximab maintenance to an ibrutinib-containing regimen.

## 4.3 ENRICH and ECHO

**ENRICH** randomised 397 untreated patients aged ≥60 years to ibrutinib–rituximab or investigator-preselected R-CHOP/bendamustine–rituximab, followed by rituximab maintenance in responders [S07]:

- Median age: **74 years**.
- Median follow-up: **47.9 months**.
- PFS favoured ibrutinib–rituximab: adjusted HR **0.69** (95% CI 0.52–0.90), p=**0.0034**.
- By preselected comparator, HR was **0.37** against R-CHOP and **0.91** against bendamustine–rituximab. The abstract does not report a treatment-by-backbone interaction test; the subgroup values should not be treated as proof of superiority over bendamustine–rituximab.
- Grade ≥3 adverse events were **67% versus 70%**.
- Ibrutinib continued until progression/toxicity, so this was not a fixed-duration chemotherapy-free strategy.

**ECHO** randomised 598 untreated patients aged ≥65 years to acalabrutinib or placebo plus bendamustine–rituximab, followed by rituximab maintenance [S08]:

- Median PFS: **66.4 versus 49.6 months**; HR **0.73** (95% CI 0.57–0.94), p=**0.0160**.
- ORR/CR: **91.0%/66.6%** versus **88.0%/53.5%**.
- OS was not significantly different: HR **0.86**, p=**0.27**.
- Grade ≥3 adverse events: **88.9% versus 88.2%**.
- Crossover at progression and continuous acalabrutinib complicate OS interpretation.

## 4.4 TP53-mutated/high-risk and fixed-duration approaches

- In the single-arm BOVen phase II study of 25 untreated TP53-mutated patients, ORR was **96%**, CR **88%**, and cycle-13 uMRD was **95% at 10⁻⁵** and **84% at 10⁻⁶**. At 28.2 months’ median follow-up, 2-year PFS, disease-specific survival and OS were **72%, 91% and 76%**. Patients in CR/uMRD after 24 cycles could stop treatment. Promising activity is not comparative proof that BOVen overcomes TP53 risk [S09].
- FIL_V-RBAC enrolled 140 older/less-fit patients, including 54 with high-risk disease; high-risk patients received four RBAC cycles followed by 24 months of venetoclax consolidation/maintenance. Two-year PFS was **60%**, median PFS **37 months**, and one treatment-related tumour-lysis death occurred during RBAC. The control was historical/implicit rather than randomised [S10].
- Front-line ALR/ALO was a small phase II MRD-driven study. For ALR, ORR was **100%**, CR **83%**, molecular CR after 12 cycles **67%**, and 4-year PFS/OS **76%/91%**. ALO had 90% ORR/CR/molecular CR after induction and 2-year PFS/OS of 100%, but the abstract does not state cohort denominators. Treatment discontinuation was permitted only after deep response; this remains feasibility evidence [S11].
- In R/R VALERIA, 59 patients received venetoclax–lenalidomide–rituximab with treatment cessation after confirmed molecular remission. Six-month ORR was **63%** overall and **40%** after prior BTKi failure; median PFS and OS were **21 and 31 months**. Twenty-eight patients stopped in molecular remission and 25 remained MRD-negative after median **17.4 months**. Grade 3–4 neutropenia and thrombocytopenia occurred in **88%** and **36%**. The corrected phase II lenalidomide dose is **15 mg**, not the 20 mg printed in the PubMed abstract [S12–S12C].
- MRD is prognostic but does not yet justify de-escalating established maintenance. In the European MCL Elderly analysis, rituximab maintenance benefited MRD-negative patients after induction (PFS HR **0.38**; OS HR **0.37**). In MRD-positive patients the PFS CI crossed 1 (HR **0.51**, 95% CI 0.26–1.02). The authors explicitly discouraged de-escalation solely because a patient was MRD-negative [S13].

## 4.5 R/R MCL after covalent BTKi

### Pirtobrutinib

In the single-arm BRUIN primary MCL cohort of 90 cBTKi-pretreated patients [S14]:

- **82.2%** had discontinued cBTKi because of progression.
- ORR was **57.8%** (95% CI 46.9–68.1), including **20.0% CR**.
- Median response duration was **21.6 months** at 12 months’ median follow-up.
- In the 164-patient safety cohort, grade ≥3 haemorrhage was **3.7%** and atrial fibrillation/flutter **1.2%**; **3%** discontinued for a treatment-related adverse event.
- Because there was no concurrent comparator, cross-trial ranking against CAR-T, bispecific antibody or BCL2 inhibition is unsupported.

### CAR-T

**Brexu-cel, ZUMA-2 five-year follow-up** [S15]:

- ZUMA-2 cohort 1: **N=68**, median follow-up **67.8 months**.
- Original ORR/CR in treated efficacy patients: **93%/67%**.
- Median response duration: **36.5 months**; median OS: **46.5 months**.
- Among responders, 5-year cumulative relapse and non-relapse mortality were **40%** and **22%**.
- No new grade 5 CRS/neurological events or subsequent T-cell malignancies were reported. The analysis is mature but remains single-arm.

**Liso-cel, TRANSCEND NHL 001** [S16]:

- 104 underwent leukapheresis; **88 were infused**, illustrating pre-infusion attrition.
- In 83 efficacy-evaluable patients, ORR was **83.1%**, CR **72.3%**, median response duration **15.7 months**, and median PFS **15.3 months**.
- CRS occurred in **61%** (grade 3–4: **1%**); neurological events in **31%** (grade 3–4: **9%**); grade ≥3 infections in **15%**; prolonged cytopenia in **40%**.
- Phase I, single-arm design and shorter follow-up prevent direct comparison with brexu-cel.

**External validity and access attrition**

- CIBMTR prospective registry data for 476 brexu-cel recipients showed ORR **91%**, CR **82%**, 1-year OS **76%**, PFS **63%**, and non-relapse mortality **8%** [S17].
- The UK intention-to-treat series approved 119 patients, but only **83 received infusion**. Infused ORR/CR was **87%/81%**; 12-month PFS **62%**. Non-relapse mortality rose to **25% at 24 months**, mostly from infection. This demonstrates that infused-patient response rates do not capture manufacturing/progression attrition or all real-world mortality [S18].

### Glofitamab

In 60 evaluable R/R MCL patients treated for a fixed 12 cycles [S19]:

- CR was **78.3%** and ORR **85.0%**.
- Among 31 previously treated with BTKi, CR was **71.0%** and ORR **74.2%**.
- CRS occurred in **70.0%**; grade ≥2 CRS was lower after 2,000 mg versus 1,000 mg obinutuzumab pretreatment (**22.7% versus 62.5%**).
- Four withdrawals were caused by infections.
- These are early-phase, non-randomised data; the abstract does not supply mature PFS/OS.

### Sonrotoclax

The corrected-status phase I/II record reports, in 103 efficacy-evaluable patients [S20]:

- ORR **52.4%**, CR **15.5%**.
- Reported response in TP53-mutated patients: **59.1%**.
- Median response duration **15.8 months**; median PFS **6.5 months**.
- TLS **7.0%**, all reported as resolving without sequelae.
- Grade ≥3 neutropenia **19.1%**, thrombocytopenia **9.6%**, anaemia **7.8%**.

**Important:** an erratum was published on 14 July 2026 [S20C], but its content was not stated in the checked PubMed/Crossref metadata. These numerical values reproduce the currently retrieved PubMed abstract and should remain **qualified**, not treated as final corrected values.

## 4.6 Maintenance and supportive-care findings

- Mature randomised evidence supports rituximab maintenance after R-CHOP in older responders: median PFS **5.4 versus 1.9 years** and OS **9.8 versus 7.1 years** compared with interferon maintenance. Toxicity was low after R-CHOP but substantially worse after R-FC, including grade 3–4 leukopenia up to **40%** and infection up to **15%** [S21].
- SHINE improved median PFS with continuous ibrutinib added to bendamustine–rituximab (**80.6 versus 52.9 months**; HR **0.75**) but not OS, while grade 3–4 adverse events were **81.5% versus 77.3%** [S22].
- TRIANGLE, CAR-T and glofitamab all show clinically important infection burdens. The UK brexu-cel series is particularly cautionary because 24-month non-relapse mortality reached 25%, mostly due to infection [S06, S16, S18, S19, S23].
- No MCL-specific randomised evidence for a particular antimicrobial prophylaxis, immunoglobulin replacement or vaccination schedule was identified in this targeted set. Detailed supportive-care prescriptions should therefore come from separate CAR-T/bispecific/BTKi supportive-care guidelines, not be inferred from these MCL efficacy abstracts.

---

# 5. Claim-to-source matrix

| Claim | Atomic statement | Sources | Location/type | Status |
|---|---|---|---|---|
| C01 | TP53 mutation is a major adverse prognostic factor under intensive chemoimmunotherapy. | S04 | PubMed abstract; cohort molecular analysis | **Supported** |
| C02 | MIPI53 separates newly diagnosed patients into markedly different survival groups. | S03 | PubMed abstract; development/external validation | **Supported; not treatment-predictive** |
| C03 | Other molecular lesions may refine risk beyond TP53/Ki-67/blastoid status. | S05 | PubMed abstract; internally validated model | **Qualified** |
| C04 | At 4.5 years, adding ASCT to the TRIANGLE ibrutinib regimen did not improve failure-free survival. | S06 | PubMed abstract; randomised phase III | **Supported** |
| C05 | TRIANGLE’s ibrutinib-containing arms improved OS versus control but increased infections. | S06 | PubMed abstract | **Supported** |
| C06 | Ibrutinib–rituximab improved PFS over the pooled ENRICH immunochemotherapy control. | S07 | PubMed abstract; randomised phase II/III | **Supported** |
| C07 | ENRICH proves superiority over bendamustine–rituximab specifically. | S07 | Subgroup HR 0.91; no interaction reported | **Unsupported** |
| C08 | ECHO improved PFS but had not demonstrated an OS advantage. | S08 | PubMed abstract; randomised phase III | **Supported** |
| C09 | BOVen is active in untreated TP53-mutated MCL and permits MRD-based cessation. | S09 | PubMed abstract; single-arm phase II | **Supported as feasibility/activity; comparative superiority unproven** |
| C10 | FIL_V-RBAC proves venetoclax overcomes high-risk biology. | S10 | Single-arm phase II | **Unsupported as causal claim** |
| C11 | MRD-guided treatment cessation is feasible in selected frontline and R/R cohorts. | S09, S11, S12 | PubMed abstracts; single-arm studies | **Qualified** |
| C12 | MRD negativity justifies omission of rituximab maintenance. | S13 | PubMed abstract | **Contradicted by available evidence** |
| C13 | Pirtobrutinib has meaningful activity after cBTKi exposure. | S14 | PubMed abstract; phase I/II | **Supported** |
| C14 | At median follow-up of 67.8 months in ZUMA-2 cohort 1, median duration of response was 36.5 months. | S15 | PubMed abstract; mature single-arm follow-up | **Supported** |
| C15 | Liso-cel is active after BTKi exposure with low grade ≥3 CRS but material neurological toxicity/cytopenia. | S16 | PubMed abstract; phase I | **Supported** |
| C16 | Real-world CAR-T effectiveness resembles trials, but intention-to-treat attrition and infection-related mortality are important. | S17, S18 | Registry and UK ITT abstracts | **Supported** |
| C17 | Fixed-duration glofitamab is active after prior BTKi. | S19 | PubMed abstract; phase I/II | **Supported** |
| C18 | Sonrotoclax’s published numerical outcomes are final and unaffected by correction. | S20, S20C | Parent record plus erratum | **Unresolved/qualified** |
| C19 | Rituximab maintenance benefits older responders after R-CHOP. | S21, S13 | Randomised trial follow-up/MRD analysis | **Supported** |
| C20 | Rituximab maintenance added to TRIANGLE’s ibrutinib arms improves PFS without additional risk. | S23 | Non-randomised secondary analysis | **Partly supported; infection risk increased** |
| C21 | Unadjusted cross-trial response rates establish a preferred sequence among pirtobrutinib, cellular therapy, bispecific antibodies and investigational BCL2 inhibition. | S14–S20 | Heterogeneous single-arm studies | **Unsupported** |
| C22 | MCL-specific prophylaxis schedules can be derived from these efficacy abstracts. | S06, S16, S18, S19, S21–S23 | Toxicity reporting only | **Unsupported** |
| C23 | MCL diagnosis requires a mature B-cell phenotype with cyclin D1 expression and/or CCND1 rearrangement; additional parameters are required for uncommon cyclin D1-negative disease. | S01 | Verified guideline full text; diagnosis section | **Supported** |
| C24 | Morphology, Ki-67 and TP53 mutational status should be assessed for risk definition, with TP53 analysis at diagnosis and repeat assessment at relapse where feasible. | S01 | Verified guideline full text; diagnosis and risk sections | **Supported** |
| C25 | Selected asymptomatic patients with low-risk or indolent MCL may be observed with 3–6-month clinical/laboratory review and clinically directed imaging. | S01 | Verified guideline full text; indolent presentation section | **Supported** |
| C26 | Long-term follow-up should continue after first-line systemic treatment, with history, examination and laboratory assessment every 3–6 months initially. | S01 | Verified guideline full text; follow-up section | **Supported** |
| C27 | Surveillance imaging should be clinically directed and re-biopsy at relapse is recommended when feasible. | S01 | Verified guideline full text; diagnosis and follow-up sections | **Supported** |

---

# 6. Verified evidence ledger

Scientific extraction was **abstract-only** except for the verified S01 full text and the PubMed-linked VALERIA correction notice.

| ID | Bibliographic identity | Design/population | Abstract-supported result | Verification/integrity |
|---|---|---|---|---|
| S01 | Jerkeman M et al. *EHA–EU MCL network guidelines for diagnosis and treatment of mantle cell lymphoma.* **HemaSphere. 2025.** PMID **41132246**; DOI **10.1002/hem3.70233** | Clinical guideline | Verified full text supports integrated diagnosis, morphology/Ki-67/TP53 assessment, observation, re-biopsy at relapse and long-term follow-up | `V2-CONFIRMED`; PMCID **PMC12541557** full text checked; no correction/retraction found |
| S02 | Jain P et al. *High-risk MCL: recognition and treatment.* **Blood. 2025.** PMID **39786418**; DOI **10.1182/blood.2023022354** | Review | High-risk clinical, pathological and molecular features | `V2`; secondary evidence |
| S03 | Bastos-Boente M et al. *Development and validation of a novel prognostic index for mantle cell lymphoma integrating TP53 mutations (MIPI53).* **Br J Haematol. 2026.** PMID **42134850**; DOI **10.1111/bjh.70535** | Development/validation; N=143 plus external cohort | 5-year PFS 83.1%/35.4%/12.0%; external c-index 0.732 | `V2`; no issue found |
| S04 | Eskelund CW et al. *TP53 mutations identify younger mantle cell lymphoma patients who do not benefit from intensive chemoimmunotherapy.* **Blood. 2017.** PMID **28819011**; DOI **10.1182/blood-2017-04-779736** | Molecular cohort; N=183 | TP53 OS HR 6.2; median OS 1.8 vs 12.7 years | `V2`; comment linked, no correction/retraction |
| S05 | Moia R et al. *Molecular biomarkers as key determinants of outcome in mantle cell lymphoma: results from the FIL V-RBAC trial.* **Blood Adv. 2026.** PMID **42498280**; DOI **10.1182/bloodadvances.2026020780** | Biomarker analysis; N=132 | Four independently associated molecular variables/model | `V2`; newly indexed 24 July 2026 |
| S06 | Dreyling M et al. *Addition of autologous stem-cell transplantation to an ibrutinib-containing first-line treatment… (TRIANGLE): 4·5-year follow-up…* **Lancet. 2026.** PMID **42134356**; DOI **10.1016/S0140-6736(26)00362-4** | Randomised phase III; N=870 | 4-year FFS 82%/81%/70%; no added ASCT benefit; both ibrutinib arms improved OS versus control; grade 3–5 infections 34%/26%/15% | `V2`; no issue found |
| S07 | Lewis DJ et al. *Ibrutinib and rituximab versus immunochemotherapy… (ENRICH).* **Lancet. 2025.** PMID **41052510**; DOI **10.1016/S0140-6736(25)01432-1** | Randomised phase II/III; N=397 | PFS HR 0.69 | `V2`; no issue found |
| S08 | Wang M et al. *Acalabrutinib Plus Bendamustine-Rituximab in Untreated Mantle Cell Lymphoma.* **J Clin Oncol. 2025.** PMID **40311141**; DOI **10.1200/JCO-25-00690** | ECHO, randomised phase III; N=598 | PFS 66.4 vs 49.6 months; OS NS | `V2`; no issue found |
| S09 | Kumar A et al. *Zanubrutinib, obinutuzumab, and venetoclax for first-line treatment of mantle cell lymphoma with a TP53 mutation.* **Blood. 2025.** PMID **39437708**; DOI **10.1182/blood.2024025563** | BOVen phase II; N=25 | ORR 96%; CR 88%; 2-year PFS 72% | `V2`; no issue found |
| S10 | Visco C et al. *Rituximab, bendamustine, and cytarabine followed by venetoclax… (FIL_V-RBAC).* **Lancet Haematol. 2025.** PMID **40975105**; DOI **10.1016/S2352-3026(25)00252-2** | Single-arm phase II; N=140, high-risk n=54 | High-risk 2-year PFS 60% | `V2`; no issue found |
| S11 | Ruan J et al. *MRD-driven initial therapy of acalabrutinib and lenalidomide plus rituximab or obinutuzumab for mantle cell lymphoma.* **Blood Adv. 2026.** PMID **41289154**; DOI **10.1182/bloodadvances.2025017760** | Phase II | ALR ORR 100%; molecular CR 67% after 12 cycles | `V2`; cohort denominators incomplete in abstract |
| S12 | Jerkeman M et al. *MRD-driven treatment with venetoclax-R2… MCL7 VALERIA trial.* **Blood Adv. 2024.** PMID **38113470**; DOI **10.1182/bloodadvances.2023011920** | Phase Ib/II; N=59 | ORR 63%; PFS 21 months; 28 stopped in molecular remission | `V2-CORRECTED` |
| S12C | *Erratum: Jerkeman M… VALERIA trial.* **Blood Adv. 2024.** PMID **39392649**; DOI **10.1182/bloodadvances.2024013955** | Published erratum | Correct lenalidomide phase II dose: 15 mg, not 20 mg | `V2-CONFIRMED CORRECTION` |
| S13 | Hoster E et al. *Predictive Value of Minimal Residual Disease for Efficacy of Rituximab Maintenance…* **J Clin Oncol. 2024.** PMID **37992261**; DOI **10.1200/JCO.23.00899** | Prospective planned trial analysis | MRD-negative PFS HR 0.38 with maintenance | `V2`; no issue found |
| S14 | Wang ML et al. *Pirtobrutinib in Covalent Bruton Tyrosine Kinase Inhibitor Pretreated Mantle-Cell Lymphoma.* **J Clin Oncol. 2023.** PMID **37192437**; DOI **10.1200/JCO.23.00562** | BRUIN phase I/II; efficacy n=90 | ORR 57.8%; CR 20%; DOR 21.6 months | `V2`; no issue found |
| S15 | Muñoz J et al. *Five-year follow-up… ZUMA-2, Cohorts 1 and 2.* **J Hematol Oncol. 2026.** PMID **42036693**; DOI **10.1186/s13045-026-01797-4** | Five-year single-arm follow-up; cohort 1 N=68 | At median follow-up 67.8 months, median DOR was 36.5 months and median OS was 46.5 months | `V2`; no issue found |
| S16 | Wang M et al. *Lisocabtagene Maraleucel in Relapsed/Refractory Mantle Cell Lymphoma… TRANSCEND NHL 001.* **J Clin Oncol. 2024.** PMID **38072625**; DOI **10.1200/JCO.23.02214** | Phase I; 104 leukapheresed, 88 infused | ORR 83.1%; CR 72.3%; PFS 15.3 months | `V2`; no issue found |
| S17 | Ahmed N et al. *Real-world outcomes of brexucabtagene autoleucel… a CIBMTR analysis.* **Blood Adv. 2025.** PMID **40706035**; DOI **10.1182/bloodadvances.2024015014** | Prospective registry; N=476 | ORR 91%; CR 82%; 1-year PFS 63% | `V2`; observational |
| S18 | O’Reilly MA et al. *Brexucabtagene autoleucel… in the United Kingdom: A real-world intention-to-treat analysis.* **HemaSphere. 2024.** PMID **38873532**; DOI **10.1002/hem3.87** | UK ITT; 119 approved, 83 infused | Infused ORR 87%; 24-month NRM 25%, mainly infection | `V2`; observational |
| S19 | Phillips TJ et al. *Glofitamab in Relapsed/Refractory Mantle Cell Lymphoma: Results From a Phase I/II Study.* **J Clin Oncol. 2025.** PMID **39365960**; DOI **10.1200/JCO.23.02470** | Phase I/II; evaluable n=60 | ORR 85%; CR 78.3%; prior-BTKi ORR 74.2% | `V2`; no issue found |
| S20 | Eyre TA et al. *Phase I/II Study of Sonrotoclax (BGB-11417) Monotherapy…* **J Clin Oncol. 2026.** PMID **42385124**; DOI **10.1200/JCO-26-00550** | Phase I/II; efficacy n=103 | Abstract reports ORR 52.4%; PFS 6.5 months | `V2-CORRECTED`; correction content unresolved |
| S20C | Eyre TA et al. *Erratum: Phase I/II Study of Sonrotoclax…* **J Clin Oncol. 2026.** PMID **42447415**; DOI **10.1200/JCO-26-01699** | Published erratum | Correction relationship established; corrected field not available in checked metadata | `V2-CONFIRMED CORRECTION` |
| S21 | Kluin-Nelemans HC et al. *Treatment of Older Patients With Mantle Cell Lymphoma: Long-Term Follow-Up of the Randomized European MCL Elderly Trial.* **J Clin Oncol. 2020.** PMID **31804876**; DOI **10.1200/JCO.19.01294** | Randomised phase III | After R-CHOP, maintenance PFS 5.4 vs 1.9 years | `V2`; no issue found |
| S22 | Wang ML et al. *Ibrutinib plus Bendamustine and Rituximab in Untreated Mantle-Cell Lymphoma.* **N Engl J Med. 2022.** PMID **35657079**; DOI **10.1056/NEJMoa2201817** | SHINE randomised; N=523 | PFS 80.6 vs 52.9 months; OS similar | `V2`; comments linked, no correction/retraction |
| S23 | Ladetto M et al. *Rituximab Maintenance Added to Ibrutinib-Containing Therapy in Younger, Untreated Patients With Mantle Cell Lymphoma: Results From the TRIANGLE Trial.* **J Clin Oncol. 2026.** PMID **42447409**; DOI **10.1200/JCO-26-00705** | Non-randomised secondary TRIANGLE analysis | Higher 4-year PFS and grade 3–5 infections with maintenance | `V2`; residual confounding |

---

## 7. Main conclusions and unresolved issues

1. **Front line:** mature TRIANGLE supports an ibrutinib-containing, non-ASCT strategy in fit younger patients; ENRICH and ECHO establish PFS gains from first-line BTK-based strategies in older patients, but treatment duration, chemotherapy exposure and toxicity differ substantially.
2. **High-risk disease:** TP53 mutation remains strongly adverse. BOVen, V-RBAC and MRD-driven regimens are promising, but none yet supplies randomised proof that a novel strategy neutralises TP53 risk.
3. **MRD:** MRD is prognostic and response-adapted cessation is feasible in small studies. It is not yet a universally validated surrogate or sufficient reason to omit effective maintenance.
4. **After cBTKi:** pirtobrutinib, CAR-T, glofitamab and sonrotoclax all have activity, but their studies differ in eligibility, prior therapy, denominator, follow-up and endpoint assessment. Unadjusted cross-trial response-rate ranking is invalid.
5. **CAR-T:** durable remission is possible, but leukapheresis-to-infusion attrition, prolonged cytopenias, neurological toxicity and infection-related non-relapse mortality must be represented alongside response rates.
6. **Maintenance/support:** rituximab maintenance has mature evidence after R-CHOP. Its addition to TRIANGLE’s ibrutinib arms is supported only by a non-randomised secondary analysis and materially increased serious infections.
7. **Integrity exception:** sonrotoclax’s July 2026 erratum must be examined before its abstract numbers are used in a definitive clinical document.

## 8. Audit statement

Bibliographic identity was cross-checked in PubMed and Crossref on **28 July 2026**. All 25 ledger records resolved concordantly by PMID, DOI, title and first author. Publication types and correction/retraction links were checked. No retraction was identified. Following independent-review challenge, S01 full text was checked through PMCID **PMC12541557** and S06/S15 abstract extractions were reconciled against live PubMed XML. Other scientific extraction remained abstract-only, except that the PubMed-linked VALERIA correction notice was inspected to establish the corrected lenalidomide dose. The principal unresolved item is the substantive content of the sonrotoclax erratum.

**Provenance note:** the original delegated audit was report-only. This controlled copy was subsequently amended after independent-review challenge to record the live S01 full-text and S06/S15 PubMed XML checks described above.
