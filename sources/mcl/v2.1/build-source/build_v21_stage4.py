#!/usr/bin/env python3
"""Stage 4: rewrite the company-access part of section 15 after the owner
attested to two live UK early access schemes. Adds SmPC-verified indications,
the AstraZeneca UK EAP precedent and the FoC-scheme literature."""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:160])
    return html.replace(needle, repl, n)


def cut(html, start_marker, end_marker, repl):
    i = html.find(start_marker)
    if i < 0:
        sys.exit('START NOT FOUND: %r' % start_marker[:100])
    j = html.find(end_marker, i)
    if j < 0:
        sys.exit('END NOT FOUND: %r' % end_marker[:100])
    return html[:i] + repl + html[j:]


# Replace everything from "What was found for each agent" up to the governance
# heading with a rewritten, owner-attested block.
NEW = """<h3>Company early access schemes in first-line disease</h3>
    <div class="uk"><strong>Attested by the accountable owner, 30 July 2026</strong>
      <p>Both first-line regimens recorded elsewhere in this guideline as having no routine commissioning route are reaching patients in the United Kingdom through company early access schemes, and the accountable owner has patients on both:</p>
      <ul>
        <li><strong>Acalabrutinib with bendamustine and rituximab</strong> — supplied by AstraZeneca through an early access scheme.</li>
        <li><strong>Ibrutinib in the TRIANGLE regimen</strong> — supplied by Johnson &amp; Johnson.</li>
      </ul>
      <p>This is recorded on the direct attestation of the accountable owner. Neither scheme is publicly listed, and the reason for that is set out below — it is a known and expected property of these arrangements rather than a reason to doubt them. Local scheme references, written agreements and pharmacy records are the definitive documentation and are held by the treating trust.</p>
    </div>
    <p>Both regimens hold a Great Britain marketing authorisation, and the two licensed populations are <strong>complementary and non-overlapping</strong>. Getting that distinction right is the single most important practical point in this section, because the schemes track the licences.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th scope="col">Regimen</th><th scope="col">Licensed population, verbatim from the current SmPC</th><th scope="col">SmPC revision</th><th scope="col">Marketing authorisation holder</th></tr></thead>
        <tbody>
          <tr><td>Acalabrutinib with bendamustine and rituximab</td><td><q>Calquence in combination with bendamustine and rituximab (BR) is indicated for the treatment of adult patients with previously untreated mantle cell lymphoma (MCL) who are <strong>not eligible</strong> for autologous stem cell transplant (ASCT).</q></td><td>11 March 2026</td><td>AstraZeneca UK Limited</td></tr>
          <tr><td>Ibrutinib, TRIANGLE regimen</td><td><q>IMBRUVICA in combination with rituximab, cyclophosphamide, doxorubicin, vincristine, and prednisolone (IMBRUVICA + R-CHOP) alternating with R-DHAP (or R-DHAOx) without IMBRUVICA, followed by IMBRUVICA monotherapy, is indicated for the treatment of adult patients with previously untreated mantle cell lymphoma (MCL) who <strong>would be eligible</strong> for autologous stem cell transplantation (ASCT).</q></td><td>26 May 2026</td><td>Janssen-Cilag Ltd</td></tr>
        </tbody>
      </table>
    </div>
    <div class="changed"><strong>Transplant eligibility is the selection criterion, and it runs opposite ways</strong>
      <p>Acalabrutinib with bendamustine–rituximab is licensed only for patients who are <strong>not</strong> eligible for autologous stem-cell transplantation. The TRIANGLE ibrutinib regimen is licensed only for patients who <strong>would be</strong> eligible. Between them they cover the whole of first-line mantle cell lymphoma, split at exactly the point section 5 and section 6 already divide on.</p>
      <p>The practical consequence: assessment and documentation of transplant eligibility determines which scheme a patient can enter, and using either regimen on the other side of that line is off-label against its Great Britain SmPC. Record the eligibility determination and its basis before approaching either company.</p>
    </div>
    <p>The mechanism here is a <strong>post-licence, pre-reimbursement company scheme</strong>. It is not compassionate use in the regulatory sense, not the MHRA Early Access to Medicines Scheme, and not an unlicensed supply. Both medicines are licensed for the population being treated; what is missing is the NICE recommendation and therefore the commissioned funding. That is precisely the gap the NHS England free-of-charge medicines policy exists to govern, and the governance requirements below apply in full.</p>
    <p>That AstraZeneca operates schemes of this kind in United Kingdom haematology is independently documented. The EPIC study — <q>A non-interventional, observational cohort study of Chronic Lymphocytic Leukaemia patients treated with acalabrutinib in the first-line setting through the UK Early Access Programme</q> (study code D8220R00033, NCT05557695) — was built specifically to follow up patients who <q>started treatment as part of the acalabrutinib Early Access Programme (EAP)</q>. That programme was in first-line chronic lymphocytic leukaemia rather than mantle cell lymphoma, but it establishes the named mechanism, the company and the country, and it shows the pattern these schemes follow: supply during the funding gap, with an observational study attached to generate the real-world evidence.</p>
    <h3>Why neither scheme appears in any public search</h3>
    <p>An earlier revision of this section reported that no published programme could be located for either regimen. That statement was accurate about the sources searched and <strong>misleading about what it implied</strong>. The sources were the wrong ones.</p>
    <p>ClinicalTrials.gov registers expanded access programmes, which is a United States regulatory construct; a United Kingdom post-licence company scheme is not an expanded access programme and does not belong there. European Medicines Agency compassionate use opinions under Article 83 are optional, and only six have ever been issued, none in oncology. Neither instrument would ever capture the schemes described above. Searching them and reporting a null result produced a false impression of absence.</p>
    <p>The published literature on these schemes explains the invisibility directly. A retrospective review of free-of-charge schemes evaluated between 2013 and 2019 by a single NHS trust and a regional drug and therapeutics committee (S45) found that <strong>90% were company schemes</strong> and only 10% were MHRA Early Access to Medicines Scheme arrangements reviewed locally, and that use of company schemes grew by an average of 50% per year while the MHRA scheme showed little growth. The authors concluded that <q>there is no standardisation of this practice and there is no regulatory oversight</q>, and that no standardised data collection framework exists. There is no national register to search. Approval sits with the integrated care system and the individual trust, under a written agreement between the company and that trust.</p>
    <div class="uk"><strong>The rule this guideline now follows</strong>
      <p>Where this document records that an option has no routine commissioning route, that is a statement about NHS commissioning only. It is <strong>not</strong> a statement that the option is unavailable, and it must never be read as one. A company early access or free-of-charge scheme may exist for any licensed medicine sitting in the gap between marketing authorisation and a NICE recommendation, and by the nature of those arrangements this guideline cannot enumerate them.</p>
      <p>Before concluding that a patient has no option, ask the company directly and ask your chief pharmacist what agreements the trust already holds.</p>
    </div>
    <h3>The other two agents</h3>
    <p>For completeness, the position found for the two relapsed-setting agents most often raised, on the same caveat that public sources are an unreliable guide:</p>
    <ul>
      <li><strong>Pirtobrutinib.</strong> A named individual-patient expanded access programme is registered — NCT05172700, sponsored by Loxo Oncology at Eli Lilly — explicitly covering mantle cell lymphoma previously treated with a covalent BTK inhibitor. No United Kingdom site is listed on the registry entry; requests outside the United States route through the local company office. Note the tension worth raising with the company: the same manufacturer declined to make an evidence submission to NICE, which is why the appraisal is suspended.</li>
      <li><strong>Glofitamab.</strong> The manufacturer's published compassionate use list covers diffuse large B-cell lymphoma, transformed follicular lymphoma and primary mediastinal B-cell lymphoma; mantle cell lymphoma is not on that list. The expired MHRA early-access opinion was also diffuse large B-cell lymphoma only. The documented United Kingdom route is the GLOBRYTE trial. If a local scheme exists it is not publicly recorded, and the same caveat applies.</li>
    </ul>
    """

h = cut(h, '<h3>What was found for each agent</h3>',
           '<h3>Governance for a free-of-charge scheme</h3>', NEW)

# ------------------------------- soften the closing limitations box wording
h = must(h,
  '<p>An arrangement made directly between a treating consultant and a company\'s medical affairs team is therefore invisible to every source searched for this section. A clinician reporting local access to acalabrutinib–bendamustine–rituximab or to a TRIANGLE-derived regimen on a compassionate or free-of-charge basis is <strong>entirely consistent</strong> with the null findings recorded above. This guideline states what is publicly documented; it does not assert that undocumented arrangements do not exist. Confirm the position locally with pharmacy and with the company before concluding that a patient has no option.</p>',
  '<p>An arrangement made directly between a treating consultant and a company\'s medical affairs team is invisible to every public source. The two first-line schemes recorded above are attested by the accountable owner and are not publicly listed; that is the normal state of affairs for this class of arrangement, not an exception. <strong>A null result in a public search is not evidence that a scheme does not exist, and this guideline does not treat it as such.</strong> Confirm the position locally with pharmacy and with the company before concluding that a patient has no option.</p>')

h = must(h,
  '<p>Absence of a public record does not mean a scheme does not exist. Only programmes intended for groups of patients are reliably registered; individual named-patient and single-patient free-of-charge supply is almost never registered anywhere.',
  '<p>Absence of a public record does not mean a scheme does not exist, and this section should not be read as a complete list. Only programmes intended for groups of patients in the United States are reliably registered; United Kingdom post-licence company schemes and individual named-patient supply are almost never registered anywhere.')

# --------------------------------------------------- card updates
h = must(h,
 '<p><strong>England access:</strong> No final recommendation or demonstrated national MCL Blueteq route. No published expanded access or company scheme for this combination was located; a general manufacturer early-access request route exists. Interim NHS funding does not apply because it requires <em>positive</em> draft guidance. See section 15.</p>',
 '<p><strong>England access:</strong> No final NICE recommendation and no national MCL Blueteq route. <strong>An AstraZeneca early access scheme is supplying this combination to United Kingdom patients, attested by the accountable owner on 30 July 2026</strong>; it is not publicly listed, which is normal for a post-licence pre-reimbursement scheme. Interim NHS funding does not apply because that requires <em>positive</em> draft guidance. Note the licence is restricted to patients <strong>not eligible</strong> for ASCT. See section 15.</p>')

h = must(h,
 '<p><strong>England access:</strong> No final NICE entitlement or demonstrated national commissioning route at the cut-off. Note that first-line ibrutinib was separately available in England from March 2020 under the NHS England COVID-19 interim treatment options, which was NHS commissioning rather than compassionate supply and generated a 149-patient national cohort (S44). That scheme must not be cited as evidence of a current route. See section 15.</p>',
 '<p><strong>England access:</strong> No final NICE entitlement and no national commissioning route at the cut-off. <strong>A Johnson &amp; Johnson scheme is supplying this regimen to United Kingdom patients, attested by the accountable owner on 30 July 2026</strong>; it is not publicly listed, which is normal for a post-licence pre-reimbursement scheme. The licence covers patients who <strong>would be eligible</strong> for ASCT. Separately, first-line ibrutinib was available in England from March 2020 under the NHS England COVID-19 interim treatment options — NHS commissioning, not company supply, generating a 149-patient national cohort (S44); that historic scheme must not be cited as a current route. See section 15.</p>')

# --------------------------------------------------- new evidence record
S45 = """<li class="evidence-reference" id="reference-S45"><strong>S45:</strong> O'Callaghan S, Ferner RE, Barron A. Free-of-charge medicine schemes in the NHS: a local and regional drug and therapeutic committee's experience. Br J Clin Pharmacol. 88(6):2571–2580; published online 30 October 2021. DOI 10.1111/bcp.15094<br><strong>Design/population:</strong> Retrospective review of free-of-charge medicine schemes evaluated between 2013 and 2019 by a single NHS trust and a regional drug and therapeutics committee<br><strong>Verified extraction:</strong> 90% were company free-of-charge schemes and 10% were MHRA Early Access to Medicines Scheme arrangements reviewed locally; phase III data were available for 44% of schemes, phase II for 37%, and 19% were supported only by phase I, retrospective observational or preclinical data; use of company schemes increased on average by 50% per year while the MHRA scheme showed little growth; the authors record that <q>there is no standardisation of this practice and there is no regulatory oversight</q> and that no standardised data collection framework exists<br><strong>Integrity:</strong> V2.1; abstract-level; single-centre and single-region experience, not a national census; supports the governance and visibility statements in section 15 and no clinical recommendation; NEW IN v2.1</li>
"""
idx = h.find('id="reference-S44"')
close_ol = h.find('</ol>', idx)
h = h[:close_ol] + S45 + h[close_ol:]

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
