# MCL regimen / dose / schedule evidence package

> **REPORT ONLY — NOT PHARMACY VERIFIED.** This is a source extraction, not a prescribing protocol. A human oncology/haematology pharmacist must verify the live SmPCs, all combination-agent SmPCs, local protocols, interactions, organ-function adjustments, supportive care and monitoring before clinical use.

- Package: `MHA-MCL-PHARMACY-EVIDENCE-2026-07-28`
- Created/cut-off: `2026-07-28`
- Scope: Exact extraction from the current official MHRA SmPC PDFs listed in sources/mcl/status-matrix-v2.0.json for treatments with a current GB MCL indication. Intended for later human pharmacy verification.
- Machine-readable controlling index: [`evidence.json`](evidence.json)
- Packaged official source PDFs: [`pdfs/`](pdfs/)
- Page-marked text extractions: [`extracted-text/`](extracted-text/)
- Quote validator: `python3 validate_quotes.py`
- Package validator: `python3 validate_package.py`

## Coverage

Included: 10 licensed-MCL treatment records resolving to 8 unique MHRA SmPC PDFs. Excluded from dose extraction because the status matrix records no current GB MCL indication: ibrutinib–venetoclax, glofitamab and epcoritamab.

## Source documents

- **bortezomib-velcade** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/3eba06edb83ab9304ba520d874a7861e875a8237)
  - SHA-256: `920941d75df20a391b9b52d91ba80963a3806522304dae83592a0177f1291ed8`
  - PDF: [`pdfs/bortezomib.pdf`](pdfs/bortezomib.pdf)
  - text: [`extracted-text/bortezomib.txt`](extracted-text/bortezomib.txt)
- **ibrutinib-imbruvica** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/9af68f2ddbce960e0e1f33927adff48693412b18)
  - SHA-256: `210757e1fe2df26904647a9fb6db58050672403c08b1aed7343543d7983f17ec`
  - PDF: [`pdfs/ibrutinib.pdf`](pdfs/ibrutinib.pdf)
  - text: [`extracted-text/ibrutinib.txt`](extracted-text/ibrutinib.txt)
- **zanubrutinib-brukinsa** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/0660d09b59bb52f7204c3e4df1ff51083a38b21d)
  - SHA-256: `3fc77752aceec428fb0fbecee3614ce9ecea9b1c4efbbacf743f3cc85985920a`
  - PDF: [`pdfs/zanubrutinib.pdf`](pdfs/zanubrutinib.pdf)
  - text: [`extracted-text/zanubrutinib.txt`](extracted-text/zanubrutinib.txt)
- **brexucabtagene-autoleucel-tecartus** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/cd6be42f02be6ec2bd92569340aedaf6f1179f16)
  - SHA-256: `c1e2029a8311a32690c48d5d82997b0309e6c692b8829710112b1ee5983275dc`
  - PDF: [`pdfs/brexucabtagene-autoleucel.pdf`](pdfs/brexucabtagene-autoleucel.pdf)
  - text: [`extracted-text/brexucabtagene-autoleucel.txt`](extracted-text/brexucabtagene-autoleucel.txt)
- **acalabrutinib-calquence** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/24b093c3ac16e4ad56f01258dbfa998647538a16)
  - SHA-256: `e1b9fa76c8808b8b575d20c14c61b3386a0731d1124ab1a994791d4f9f5b1fc2`
  - PDF: [`pdfs/acalabrutinib.pdf`](pdfs/acalabrutinib.pdf)
  - text: [`extracted-text/acalabrutinib.txt`](extracted-text/acalabrutinib.txt)
- **pirtobrutinib-jaypirca** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/1d71deb47f55d9284beab5786752e8368d37d284)
  - SHA-256: `7d77a3a24eb0b38cf9841fdf79cecf6a1d59adf5a9f77260af1743d6d8b81cbd`
  - PDF: [`pdfs/pirtobrutinib.pdf`](pdfs/pirtobrutinib.pdf)
  - text: [`extracted-text/pirtobrutinib.txt`](extracted-text/pirtobrutinib.txt)
- **lisocabtagene-maraleucel-breyanzi** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/ad49533cc5d81176e83f3082da1669b3a9e543ce)
  - SHA-256: `823db046d7dfc6b19294dea44aba3f121dca87f56995faddb98b4b64ef13092c`
  - PDF: [`pdfs/lisocabtagene-maraleucel.pdf`](pdfs/lisocabtagene-maraleucel.pdf)
  - text: [`extracted-text/lisocabtagene-maraleucel.txt`](extracted-text/lisocabtagene-maraleucel.txt)
- **lenalidomide-revlimid** — [official MHRA SmPC](https://mhraproducts4853.blob.core.windows.net/docs/4eee1eaeac146ee6d44f54c544a0a61d13407294)
  - SHA-256: `f612e26fe53bf5796b2611833b2d3907e08e463d87465ce6c4e760e53a95aced`
  - PDF: [`pdfs/lenalidomide.pdf`](pdfs/lenalidomide.pdf)
  - text: [`extracted-text/lenalidomide.txt`](extracted-text/lenalidomide.txt)
## 1. Bortezomib with rituximab, cyclophosphamide, doxorubicin and prednisone (VcR-CAP / VR-CAP)

- Status-matrix ID(s): `vr-cap-first-line`
- Official source: [bortezomib-velcade](https://mhraproducts4853.blob.core.windows.net/docs/3eba06edb83ab9304ba520d874a7861e875a8237)
- PDF SHA-256: `920941d75df20a391b9b52d91ba80963a3806522304dae83592a0177f1291ed8`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> VELCADE in combination with rituximab, cyclophosphamide, doxorubicin and prednisone is indicated for the treatment of adult patients with previously untreated mantle cell lymphoma who are unsuitable for haematopoietic stem cell transplantation.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF pages 6-7

> VELCADE 3.5 mg powder for solution for injection is administered via intravenous or subcutaneous injection at the recommended dose of 1.3 mg/m2 body surface area twice weekly for two weeks on days 1, 4, 8, and 11, followed by a 10-day rest period on days 12-21. This 3-week period is considered a treatment cycle. Six VELCADE cycles are recommended, although for patients with a response first documented at cycle 6, two additional VELCADE cycles may be given. At least 72 hours should elapse between consecutive doses of VELCADE.

> The following medicinal products are administered on day 1 of each VELCADE 3 week treatment cycle as intravenous infusions: rituximab at 375 mg/m2, cyclophosphamide at 750 mg/m2 and doxorubicin at 50 mg/m2.

> Prednisone is administered orally at 100 mg/m2 on days 1, 2, 3, 4 and 5 of each VELCADE treatment cycle.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF pages 9-10

> VELCADE 3.5 mg powder for solution for injection is available for intravenous or subcutaneous administration.

> VELCADE should not be given by other routes. Intrathecal administration has resulted in death.

> VELCADE 3.5 mg reconstituted solution is administered as a 3-5 second bolus intravenous injection through a peripheral or central intravenous catheter followed by a flush with sodium chloride 9 mg/ml (0.9%) solution for injection. At least 72 hours should elapse between consecutive doses of VELCADE.

> VELCADE 3.5 mg reconstituted solution is administered subcutaneously through the thighs (right or left) or abdomen (right or left). The solution should be injected subcutaneously, at a 45-90° angle. Injection sites should be rotated for successive injections.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 7-8 and 11

> Platelet counts should be ≥ 100,000 cells/μL and the absolute neutrophils count (ANC) should be ≥ 1,500 cells/μL

> Platelet counts should be ≥ 75,000 cells/μL in patients with bone marrow infiltration or splenic sequestration

> Haemoglobin ≥ 8 g/dL

> Non-haematological toxicities should have resolved to Grade 1 or baseline.

> VELCADE treatment must be withheld at the onset of any ≥ Grade 3 VELCADE-related non-haematological toxicities (excluding neuropathy) or ≥ Grade 3 haematological toxicities (see also section 4.4). For dose adjustments, see Table 5 below.

> VELCADE therapy should be withheld for up to 2 weeks until the patient has an ANC ≥ 750 cells/μL and a platelet count ≥ 25,000 cells/μL.

> In addition, when VELCADE is given in combination with other chemotherapeutic medicinal products, appropriate dose reductions for these medicinal products should be considered in the event of toxicities, according to the recommendations in the respective Summary of Product Characteristics.

> Therefore, platelet counts should be monitored prior to each dose of VELCADE.

> Complete blood counts (CBC) with differential and including platelet counts should be frequently monitored throughout treatment with VELCADE.

## 2. Ibrutinib monotherapy for relapsed or refractory MCL

- Status-matrix ID(s): `ibrutinib-rr-one-line`
- Official source: [ibrutinib-imbruvica](https://mhraproducts4853.blob.core.windows.net/docs/9af68f2ddbce960e0e1f33927adff48693412b18)
- PDF SHA-256: `210757e1fe2df26904647a9fb6db58050672403c08b1aed7343543d7983f17ec`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF pages 1-2

> IMBRUVICA as a single agent is indicated for the treatment of adult patients with relapsed or refractory MCL.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF pages 2-3

> The recommended dose for the treatment of previously treated MCL is ibrutinib 560 mg once daily as a single agent. Treatment with IMBRUVICA as a single agent should continue until disease progression or no longer tolerated by the patient.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF page 5

> IMBRUVICA should be administered orally once daily with a glass of water approximately at the same time each day. The tablets should be swallowed whole with water and should not be broken or chewed. IMBRUVICA must not be taken with grapefruit juice or Seville oranges (see section 4.5).

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 3-8

> The dose of ibrutinib should be reduced to 280 mg once daily when used concomitantly with moderate CYP3A4 inhibitors. The dose of ibrutinib should be reduced to 140 mg once daily or withheld for up to 7 days when it is used concomitantly with strong CYP3A4 inhibitors.

> IMBRUVICA therapy should be withheld for any new onset or worsening grade 2 cardiac failure, grade 3 cardiac arrhythmias, grade ≥3 non-haematological toxicity, grade 3 or greater neutropenia with infection or fever, or grade 4 haematological toxicities.

> Monitor complete blood counts monthly.

> Appropriate clinical evaluation of cardiac history and function should be performed prior to initiating IMBRUVICA. Patients should be carefully monitored during treatment for signs of clinical deterioration of cardiac function and clinically managed.

> Regularly monitor blood pressure in patients treated with IMBRUVICA and initiate or adjust antihypertensive medication throughout treatment with IMBRUVICA as appropriate.

## 3. Ibrutinib with R-CHOP alternating with R-DHAP/R-DHAOx, followed by ibrutinib monotherapy

- Status-matrix ID(s): `triangle-ibrutinib-first-line`
- Official source: [ibrutinib-imbruvica](https://mhraproducts4853.blob.core.windows.net/docs/9af68f2ddbce960e0e1f33927adff48693412b18)
- PDF SHA-256: `210757e1fe2df26904647a9fb6db58050672403c08b1aed7343543d7983f17ec`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 1

> IMBRUVICA in combination with rituximab, cyclophosphamide, doxorubicin, vincristine, and prednisolone (IMBRUVICA + R-CHOP) alternating with R-DHAP (or R-DHAOx) without IMBRUVICA, followed by IMBRUVICA monotherapy, is indicated for the treatment of adult patients with previously untreated mantle cell lymphoma (MCL) who would be eligible for autologous stem cell transplantation (ASCT).

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 2, Table 1

> The recommended dose for the treatment of previously untreated MCL is ibrutinib 560 mg once daily (see Table 1).

**Non Inference Note:** No R-CHOP, R-DHAP or R-DHAOx component doses are supplied here because this ibrutinib SmPC explicitly redirects to each component SmPC.

**Verbatim Table Transcription:**

- **cycles 1 3 5:** IMBRUVICA in combination with R-CHOP; On days 1-19
- **cycles 2 4 6:** R-DHAP; Without IMBRUVICA
- **part i footnote:** 6 cycles; each cycle is 21 days.
- **part ii:** IMBRUVICA; Daily for 24 Months
- **r dhap footnote:** Interchangeable with R-DHAOx (rituximab, dexamethasone, cytarabine, oxaliplatin).

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF pages 2 and 5

> Treatment should start after recovery of peripheral blood counts. Rituximab may be added as per national treatment guidelines.

> IMBRUVICA should be administered orally once daily with a glass of water approximately at the same time each day. The tablets should be swallowed whole with water and should not be broken or chewed.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 3-8

**Note:** The SmPC MCL dose-modification and monitoring constraints apply to ibrutinib; combination-agent modifications require the respective live SmPCs and protocol verification.

## 4. Zanubrutinib monotherapy

- Status-matrix ID(s): `zanubrutinib-rr-one-line`
- Official source: [zanubrutinib-brukinsa](https://mhraproducts4853.blob.core.windows.net/docs/0660d09b59bb52f7204c3e4df1ff51083a38b21d)
- PDF SHA-256: `3fc77752aceec428fb0fbecee3614ce9ecea9b1c4efbbacf743f3cc85985920a`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF pages 1-2

> BRUKINSA as monotherapy is indicated for the treatment of adult patients with mantle cell lymphoma (MCL) who have received at least one prior therapy.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 2

> The recommended total daily dose of zanubrutinib is 320 mg. The daily dose may be taken either once daily (two 160 mg tablets) or divided into two doses of 160 mg twice daily (one 160 mg tablet). Treatment with BRUKINSA should be continued until disease progression or unacceptable toxicity.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF page 5

> BRUKINSA is for oral use. The film-coated tablets can be taken with or without food. Patients should be instructed to swallow the tablets whole with water, not to chew or crush the tablets. The tablet can be divided into two equal halves when advised by the healthcare provider.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 2-7

> Patients with severe renal impairment (CrCl <30 mL/min) or on dialysis should be monitored for adverse reactions (see section 5.2).

> Monitor complete blood counts monthly during treatment (see section 4.2).

**Verbatim Table Transcription:**

- **qualifying events:** ≥ Grade 3 non-haematological toxicities; ≥ Grade 3 febrile neutropenia; Grade 3 thrombocytopenia with significant bleeding; Grade 4 neutropenia (lasting >10 consecutive days); Grade 4 thrombocytopenia (lasting >10 consecutive days)
- **first:** Interrupt BRUKINSA; once toxicity has resolved to ≤Grade 1 or baseline, resume at 320 mg once daily or 160 mg twice daily
- **second:** Interrupt BRUKINSA; once toxicity has resolved to ≤Grade 1 or baseline, resume at 160 mg once daily or 80 mg twice daily
- **third:** Interrupt BRUKINSA; once toxicity has resolved to ≤Grade 1 or baseline, resume at 80 mg once daily
- **fourth:** Discontinue BRUKINSA
- **strong cyp3a inhibitor:** 80 mg once daily
- **moderate cyp3a inhibitor:** 160 mg once daily or 80 mg twice daily
- **strong or moderate cyp3a inducer:** Avoid concomitant use; consider alternative agents with less CYP3A induction

## 5. Brexucabtagene autoleucel

- Status-matrix ID(s): `brexu-cel-managed-access`
- Official source: [brexucabtagene-autoleucel-tecartus](https://mhraproducts4853.blob.core.windows.net/docs/cd6be42f02be6ec2bd92569340aedaf6f1179f16)
- PDF SHA-256: `c1e2029a8311a32690c48d5d82997b0309e6c692b8829710112b1ee5983275dc`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> Tecartus is indicated for the treatment of adult patients with relapsed or refractory mantle cell lymphoma (MCL) after two or more lines of systemic therapy including a Bruton’s tyrosine kinase (BTK) inhibitor.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 3

> Treatment consists of a single dose for infusion containing a dispersion for infusion of CAR-positive viable T cells in one infusion bag. The target dose is 2 × 106 CAR-positive viable T cells per kg of body weight (range: 1 x 106–2 x 106 cells/kg), with a maximum of 2 × 108 CAR-positive viable T cells for patients 100 kg and above.

> Tecartus is recommended to be infused 3 to 14 days after completion of the lymphodepleting chemotherapy for MCL patients.

> A lymphodepleting chemotherapy regimen consisting of cyclophosphamide 500 mg/m² intravenously and fludarabine 30 mg/m² intravenously must be administered prior to infusing Tecartus. The recommended days are on the 5th, 4th, and 3rd day before infusion of Tecartus.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF pages 3-5

> Tecartus must be administered in a qualified treatment centre by a physician with experience in the treatment of haematological malignancies and trained for administration and management of patients treated with Tecartus.

> At least 1 dose of tocilizumab for use in the event of cytokine release syndrome (CRS) and emergency equipment must be available prior to infusion.

> Tecartus is intended for autologous use only (see section 4.4).

> To minimise potential acute infusion reactions, it is recommended that patients be pre-medicated with paracetamol 500 to 1,000 mg given orally and diphenhydramine 12.5 to 25 mg intravenously or orally (or equivalent medicinal products) approximately 1 hour before the infusion of Tecartus.

> Prophylactic use of systemic corticosteroids is not recommended (see section 4.5).

> Tecartus is for intravenous use only. Tecartus must not be irradiated. Do NOT use a leukodepleting filter.

> Once tubing has been primed, infuse the entire content of the Tecartus infusion bag within 30 minutes by either gravity or a peristaltic pump.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 4-8

> Patients must be monitored daily for the first 7 days following infusion for signs and symptoms of potential CRS, neurologic events and other toxicities.

> Patients must remain within proximity of a qualified treatment centre for at least 4 weeks following infusion.

> Unresolved serious adverse reactions (especially pulmonary reactions, cardiac reactions, or hypotension) including from preceding chemotherapies.

> Active uncontrolled infection or inflammatory disease.

> Active graft-versus-host disease (GvHD).

> If the infusion is delayed for more than 2 weeks after the patient has received the lymphodepleting chemotherapy, lymphodepleting chemotherapy regimen must be administered again (see section 4.2)

> Patient blood counts must be monitored after Tecartus infusion.

> Immunoglobulin levels should be monitored after treatment with Tecartus and managed using infection precautions, antibiotic prophylaxis, and immunoglobulin replacement in case of recurrent infections and must be taken according to standard guidelines.

> Patients must be monitored life-long for secondary malignancies.

## 6. Acalabrutinib plus bendamustine and rituximab

- Status-matrix ID(s): `acalabrutinib-br-first-line`
- Official source: [acalabrutinib-calquence](https://mhraproducts4853.blob.core.windows.net/docs/24b093c3ac16e4ad56f01258dbfa998647538a16)
- PDF SHA-256: `e1b9fa76c8808b8b575d20c14c61b3386a0731d1124ab1a994791d4f9f5b1fc2`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> Calquence in combination with bendamustine and rituximab (BR) is indicated for the treatment of adult patients with previously untreated mantle cell lymphoma (MCL) who are not eligible for autologous stem cell transplant (ASCT).

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 2, Table 1

> The recommended dose of Calquence in monotherapy or in combination with other medicinal products is 100 mg acalabrutinib twice daily (equivalent to a total daily dose of 200 mg).

> Calquence dose interval is approximately 12 hours.

> Calquence should be administered from Day 1 on Cycle 1 (each cycle is 28 days) continuously until disease progression or unacceptable toxicity.

> Bendamustine should be administered at 90 mg/m2 on Days 1 and 2 of each cycle for a total of 6 cycles. Rituximab should be administered at 375 mg/m2 on Day 1 each cycle for a total of 6 cycles.

> Patients achieving a response (partial response [PR] or complete response [CR]) after the first 6 cycles, may receive maintenance rituximab at 375 mg/m2 on Day 1 of every other cycle for a maximum of 12 additional doses, starting on Cycle 8 up to Cycle 30.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF pages 2 and 7

> For the combination regimens, refer to the prescribing information of each of the medicinal products for their dosing information (for details of the combination regimens, see section 5.1).

> Calquence is for oral use. The tablets should be swallowed whole with water at approximately the same time each day, with or without food (see section 4.5). The tablets should not be chewed, crushed, dissolved or divided.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 3-9

> Recommended dose modifications for Grade ≥ 3 adverse reactions in patients receiving Calquence in combination with bendamustine and rituximab are provided in Table 2.

> Refer to the prescribing information of each of the medicinal products used in combination with Calquence for additional information for management of toxicities.

> If these inhibitors will be used short-term (such as anti-infectives for up to seven days), interrupt Calquence.

> No dose adjustment. Monitor patients closely for adverse reactions if taking moderate CYP3A inhibitors.

> Avoid concomitant use.

> Hydration should be maintained, and serum creatinine levels monitored periodically.

> Monitor complete blood counts as medically indicated (see section 4.8).

**Combination Agent Boundary:** Bendamustine and rituximab modification rules are not inferred; verify their live SmPCs and the local regimen protocol.

## 7. Acalabrutinib monotherapy for relapsed or refractory MCL

- Status-matrix ID(s): `acalabrutinib-rr-monotherapy`
- Official source: [acalabrutinib-calquence](https://mhraproducts4853.blob.core.windows.net/docs/24b093c3ac16e4ad56f01258dbfa998647538a16)
- PDF SHA-256: `e1b9fa76c8808b8b575d20c14c61b3386a0731d1124ab1a994791d4f9f5b1fc2`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> Calquence as monotherapy is indicated for the treatment of adult patients with relapsed or refractory mantle cell lymphoma (MCL) not previously treated with a BTK inhibitor.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 2

> The recommended dose of Calquence in monotherapy or in combination with other medicinal products is 100 mg acalabrutinib twice daily (equivalent to a total daily dose of 200 mg).

> Calquence dose interval is approximately 12 hours.

> Treatment with Calquence in monotherapy or in combination with obinutuzumab should be continued until disease progression or unacceptable toxicity.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF page 7

> Calquence is for oral use. The tablets should be swallowed whole with water at approximately the same time each day, with or without food (see section 4.5). The tablets should not be chewed, crushed, dissolved or divided.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 3-9

**Note:** Use the acalabrutinib-specific dose modification and monitoring constraints; no combination-agent rules apply to this monotherapy record.

## 8. Pirtobrutinib monotherapy

- Status-matrix ID(s): `pirtobrutinib-post-btki`
- Official source: [pirtobrutinib-jaypirca](https://mhraproducts4853.blob.core.windows.net/docs/1d71deb47f55d9284beab5786752e8368d37d284)
- PDF SHA-256: `7d77a3a24eb0b38cf9841fdf79cecf6a1d59adf5a9f77260af1743d6d8b81cbd`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> Jaypirca as monotherapy is indicated for the treatment of adult patients with relapsed or refractory mantle cell lymphoma (MCL) who have been previously treated with a Bruton’s tyrosine kinase (BTK) inhibitor.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 2

> The recommended dose is 200 mg pirtobrutinib once daily (QD).

> Treatment should be continued until disease progression or unacceptable toxicity.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF page 5

> The tablet should be swallowed whole with a glass of water to ensure consistent performance (patients should not chew, crush, or split tablets before swallowing) and can be taken with or without food. Patients should take the dose at approximately the same time every day.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 2-6

> Jaypirca dosing should be interrupted until recovery to Grade 1 or baseline when the patient experiences the following event:

> Grade 3 neutropenia with fever and/or infection

> Grade 4 neutropenia lasting ≥ 7 days

> Grade 3 thrombocytopenia with bleeding

> Grade 4 thrombocytopenia

> Grade 3 or 4 non-haematologic toxicity

> No dose adjustment is required for patients with mild, moderate or severe renal impairment. There are no data in patients on dialysis (see section 5.2).

> No dose adjustment is required for patients with mild, moderate, or severe hepatic impairment (see section 5.2).

> Complete blood counts should be monitored in patients during treatment as medically indicated.

> Patients should be monitored for signs and symptoms of bleeding.

> Evaluate bilirubin and transaminases at baseline and throughout treatment with Jaypirca.

## 9. Lisocabtagene maraleucel

- Status-matrix ID(s): `liso-cel-post-btki`
- Official source: [lisocabtagene-maraleucel-breyanzi](https://mhraproducts4853.blob.core.windows.net/docs/ad49533cc5d81176e83f3082da1669b3a9e543ce)
- PDF SHA-256: `823db046d7dfc6b19294dea44aba3f121dca87f56995faddb98b4b64ef13092c`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> Breyanzi is indicated for the treatment of adult patients with relapsed or refractory mantle cell lymphoma (MCL) after at least two lines of systemic therapy including a Bruton’s tyrosine kinase (BTK) inhibitor.

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF pages 3-4

> Breyanzi is intended for autologous use (see section 4.4).

> Treatment consists of a single dose for infusion containing a dispersion for infusion of CAR-positive viable T-cells in one or more vials.

> The target dose is 100 × 106 CAR-positive viable Tcells (consisting of a target 1:1 ratio of CD4+ and CD8+ cell components) within a range of 44-120 × 106 CAR-positive viable T-cells. See the accompanying release for infusion certificate (RfIC) for additional information pertaining to dose.

> Lymphodepleting chemotherapy consisting of cyclophosphamide 300 mg/m2/day and fludarabine 30 mg/m2/day, administered intravenously for three days. See the prescribing information for fludarabine and cyclophosphamide for information on dose adjustment in renal impairment.

> Breyanzi is to be administered 2 to 7 days after completion of lymphodepleting chemotherapy.

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF pages 3-5

> Breyanzi must be administered in a qualified treatment centre.

> At least 1 dose of tocilizumab for use in the event of cytokine release syndrome (CRS) and emergency equipment must be available per patient prior to infusion of Breyanzi.

> It is recommended that premedication with paracetamol and diphenhydramine (25-50 mg, intravenously or orally) or another H1-antihistamine, be administered 30 to 60 minutes before the infusion of Breyanzi to reduce the possibility of an infusion reaction.

> Prophylactic use of systemic corticosteroids should be avoided, as the use may interfere with the activity of Breyanzi (see section 4.4).

> Do NOT use a leukodepleting filter.

> Once Breyanzi components have been drawn into syringes, proceed with administration as soon as possible. The total time from removal from frozen storage to patient administration should not exceed 2 hours.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 4-8

> Patients should be monitored 2-3 times during the first week following infusion, for signs and symptoms of potential CRS, neurologic events and other toxicities.

> Frequency of monitoring after the first week should be carried out at the physician’s discretion and should be continued for at least 2 weeks after infusion.

> Patients should be instructed to remain within proximity of a qualified treatment centre for at least 2 weeks following infusion.

> Unresolved serious adverse events (especially pulmonary events, cardiac events, or hypotension), including those after preceding chemotherapies.

> Active uncontrolled infections, or inflammatory disorders.

> Active graft-versus-host disease (GVHD).

> Blood counts should be monitored prior to and after Breyanzi administration.

> Immunoglobulin levels should be monitored after treatment and managed per clinical guidelines including infection precautions, antibiotic prophylaxis and/or immunoglobulin replacement.

> Patients should be monitored life-long for secondary malignancies.

## 10. Lenalidomide monotherapy

- Status-matrix ID(s): `lenalidomide-rr`
- Official source: [lenalidomide-revlimid](https://mhraproducts4853.blob.core.windows.net/docs/4eee1eaeac146ee6d44f54c544a0a61d13407294)
- PDF SHA-256: `f612e26fe53bf5796b2611833b2d3907e08e463d87465ce6c4e760e53a95aced`

### Section 4.1 indication

**Anchor:** SmPC section 4.1, PDF page 2

> Revlimid as monotherapy is indicated for the treatment of adult patients with relapsed or refractory mantle cell lymphoma (see sections 4.4 and 5.1).

### Section 4.2 dose, schedule and duration

**Anchor:** SmPC section 4.2, PDF page 8

> The recommended starting dose of lenalidomide is 25 mg orally once daily on days 1 to 21 of repeated 28-day cycles.

**Duration Boundary:** No MCL-specific treatment duration statement was identified in section 4.2; none is inferred in this package.

**Verbatim Dose Level Transcription:**

- Starting dose: 25 mg once daily on days 1 to 21, every 28 days
- Dose Level -1: 20 mg once daily on days 1 to 21, every 28 days
- Dose Level -2: 15 mg once daily on days 1 to 21, every 28 days
- Dose Level -3: 10 mg once daily on days 1 to 21, every 28 days
- Dose Level -4: 5 mg once daily on days 1 to 21, every 28 days
- Dose Level -5: 2.5 mg once daily on days 1 to 21, every 28 days (in countries where the 2.5 mg capsule is available); 5 mg every other day on days 1 to 21, every 28 days

### Administration boundaries

**Anchor:** SmPC section 4.2, PDF page 13

> Revlimid capsules should be taken orally at about the same time on the scheduled days. The capsules should not be opened, broken or chewed. The capsules should be swallowed whole, preferably with water, either with or without food.

### High-level modification / monitoring constraints

**Anchor:** SmPC sections 4.2 and 4.4, PDF pages 5-17

> Dose is modified based upon clinical and laboratory findings (see section 4.4).

> Dose adjustments, during treatment and restart of treatment, are recommended to manage Grade 3 or 4 thrombocytopenia, neutropenia, or other Grade 3 or 4 toxicity judged to be related to lenalidomide.

> All patients should receive TLS prophylaxis (allopurinol, rasburicase or equivalent as per institutional guidelines) and be well hydrated (orally) during the first week of the first cycle or for a longer period if clinically indicated.

> To monitor for TLS, patients should have a chemistry panel drawn weekly during the first cycle and as clinically indicated.

> Patients with high tumour burden should therefore be closely monitored for adverse reactions (see Section 4.8) including signs of tumour flare reaction (TFR). Please refer to section 4.2 for dose adjustments for TFR.

> The conditions of the Pregnancy Prevention Programme must be fulfilled for all patients unless there is reliable evidence that the patient does not have childbearing potential.

> Healthcare professionals and caregivers should wear disposable gloves when handling the blister or capsule.

**Table Boundary Note:** The complete MCL thrombocytopenia, neutropenia and tumour-flare dose-modification tables remain in section 4.2 of the source PDF and require line-by-line human pharmacy verification before protocol use.

## Human pharmacy verification checklist

- [ ] Confirm each PDF SHA-256 against the packaged copy and redownload from the official URL if the live document has changed.
- [ ] Verify all section 4.1 indications and section 4.2 doses/schedules against the live SmPC at the time of review.
- [ ] For combinations, verify every component against its own current SmPC and the approved local regimen; do not infer omitted component doses.
- [ ] Verify full dose-modification tables, organ-function adjustments, interactions, contraindications, supportive care and monitoring in sections 4.2-4.5.
- [ ] Verify CAR-T centre qualification, chain of identity, product availability, lymphodepletion, premedication, CRS/ICANS readiness and follow-up requirements.
- [ ] Record pharmacist name, role, date, source versions checked, discrepancies and disposition in a controlled verification record; do not relabel this extraction as pharmacy verified without that record.

## Interpretation boundaries

- This package is not a prescribing protocol, does not establish commissioning/access, and has not been pharmacy verified. Verify every dose, schedule, interaction, organ-function adjustment, supportive-care requirement and combination-agent SmPC against the live SmPC and local protocol before clinical use.
- Exact quoted passages are whitespace-normalised from the packaged page-marked text and checked by `validate_quotes.py`. Table transcriptions are labelled separately because PDF table extraction does not preserve a simple reading order.
- The PDFs, not the text extraction or this report, are controlling sources.
- No missing combination-agent dose has been inferred. Where the SmPC redirects to another product SmPC, this package preserves that boundary.
