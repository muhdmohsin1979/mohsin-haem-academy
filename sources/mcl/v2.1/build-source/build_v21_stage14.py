#!/usr/bin/env python3
"""Stage 14: third-pass audit residuals."""
import re, sys, io

h = io.open('/home/claude/mcl-v2.1-draft.html', encoding='utf-8').read()
OUT = '/home/claude/mcl-v2.1-draft.html'


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:180])
    return html.replace(needle, repl, n)


def soft(html, needle, repl):
    return html.replace(needle, repl)


# =============================== 1. figure caption — scheme eligibility claim
h = soft(h, 'The split at transplant suitability governs both the clinical pathway and, because the two first-line marketing authorisations divide on exactly that line, which company scheme a patient can enter.',
            'The split at transplant suitability governs the clinical pathway, and the two first-line marketing authorisations divide at the same point. It does not by itself determine eligibility for any company scheme — those terms have not been independently verified here.')

# =============================== 2. section 17 — remove "cover the whole"
h = soft(h, 'Between them they cover the whole of first-line mantle cell lymphoma, split at exactly the point section 6 and section 7 already divide on.',
            'The two licensed populations are complementary and non-overlapping, dividing at the same point section 6 and section 7 do. That is a statement about the <em>licences</em>. It does not establish that the two reported schemes together make treatment available to every first-line patient, and it must not be read that way.')
h = soft(h, 'Between them they cover the whole of first-line mantle cell lymphoma',
            'The two licensed populations are complementary and non-overlapping')

# =============================== 3. status cards — "normal" implies corroboration
h = soft(h, 'it is not publicly listed, which is normal for a post-licence pre-reimbursement scheme.',
            'it is not publicly listed. Non-listing is common for this class of arrangement but is not corroboration, and the scheme has not been independently verified here.')

# =============================== 4. StiL erratum in the BR status card
h = soft(h, 'The StiL result was pooled across indolent lymphomas and MCL and has a published erratum whose substantive correction was not retrieved.',
            'The StiL result was pooled across indolent lymphomas and MCL. Its published erratum <strong>has been retrieved and read</strong>: it corrects the intermediate-risk FLIPI count in the bendamustine–rituximab group and the pooled R-CHOP overall-response count, and neither correction changes the trial&rsquo;s non-inferiority conclusion. No mantle cell-specific treatment effect is given, so pooled findings remain qualified.')

# =============================== 5. SYMPATICO correction surfaced everywhere
h = soft(h, 'median progression-free survival was 31.9 months versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia in 31% versus 11%.',
            'median progression-free survival was 31.9 months versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia in 31% versus 11%. <strong>CORRECTION_UNRESOLVED — a published correction exists against this report and its content has not been retrieved, so these figures are not finally verified.</strong>')
h = soft(h, 'median PFS 31.9 versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia 31% versus 11%.',
            'median PFS 31.9 versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia 31% versus 11%. <strong>CORRECTION_UNRESOLVED — a published correction exists and its content has not been retrieved.</strong>')
h = must(h, 'reported median progression-free survival 31.9 versus 22.1 months, hazard ratio 0.65 (95% CI 0.47&ndash;0.88), p=0.0052, with grade 3&ndash;4 neutropenia 31% versus 11%.'.replace('&ndash;', '–'),
            'reported median progression-free survival 31.9 versus 22.1 months, hazard ratio 0.65 (95% CI 0.47–0.88), p=0.0052, with grade 3–4 neutropenia 31% versus 11%. <strong>CORRECTION_UNRESOLVED &mdash; a published correction exists against this report (S38) and its content has not been retrieved, so these figures are not finally verified.</strong>')
h = soft(h, '<td>Randomised phase III benefit, hazard ratio 0.65.',
            '<td>Randomised phase III benefit, hazard ratio 0.65 — <strong>CORRECTION_UNRESOLVED</strong>.')
h = soft(h, 'Two corrections remain unresolved and are flagged at every point their figures are used: the sonrotoclax erratum',
            'Two corrections remain unresolved and are flagged at every point their figures are used: the sonrotoclax erratum')
h = must(h,
  '<p><strong>Still unresolved.</strong> The sonrotoclax erratum (S20C, PMID 42447415, DOI 10.1200/JCO-26-01699)',
  '<p><strong>Still unresolved — two of them.</strong> A published correction also exists against S38 (SYMPATICO, Lancet Oncol 2025; correction DOI 10.1016/S1470-2045(25)00210-4, PMID 40318652) and its content has not been retrieved. Every figure drawn from S38 is therefore marked CORRECTION_UNRESOLVED at the point of use, on the same basis as sonrotoclax: the prose in section 9, the relapsed algorithm, the evidence-to-recommendation row in section 15 and the status card in section 18. The first-line SYMPATICO cohort figures are reported separately in S36, against which no editorial notice was found, and are not marked. The sonrotoclax erratum (S20C, PMID 42447415, DOI 10.1200/JCO-26-01699)')

# =============================== 6. evidence tiers reconciled with definitions
h = soft(h, '<tr><td>Trial referral in TP53-mutated disease</td><td><span class="tier a">A</span></td>',
            '<tr><td>Trial referral in TP53-mutated disease</td><td><span class="tier g">G</span></td>')
h = soft(h, '<tr><td>Repeat CD19-directed CAR-T after CAR-T failure</td><td><span class="tier e">E</span></td>',
            '<tr><td>Repeat CD19-directed CAR-T after CAR-T failure</td><td><span class="tier g">G</span></td>')
h = soft(h, '<tr><td>Allogeneic HCT after CAR-T failure</td><td><span class="tier d">D</span></td><td>S46, S51</td>',
            '<tr><td>Allogeneic HCT after CAR-T failure</td><td><span class="tier g">G</span></td><td>S46, S51</td>')
h = soft(h, '<tr><td>Cross-trial ranking of post-BTKi options</td><td><span class="tier e">E</span></td>',
            '<tr><td>Cross-trial ranking of post-BTKi options</td><td>—</td>')
h = soft(h, '<td>No head-to-head randomised comparison exists between pirtobrutinib, cellular therapy, bispecific antibodies and BCL2 inhibition. Unadjusted response rates must not be used to rank them.</td>',
            '<td><strong>No evidence tier applies — this is a prohibition resting on the absence of evidence.</strong> No head-to-head randomised comparison exists between pirtobrutinib, cellular therapy, bispecific antibodies and BCL2 inhibition. Unadjusted response rates must not be used to rank them.</td>')

h = must(h,
  '<li><span class="tier g">G</span> Adopted from a society guideline recommendation,',
  '<li><strong>&mdash;</strong> No tier applies. Used where a recommendation is a prohibition resting on the <em>absence</em> of evidence rather than on any study, so no design can be graded.</li>\n'
  '      <li><span class="tier g">G</span> Adopted from a society guideline or expert-consensus recommendation,')
h = soft(h, 'where this document has <strong>not</strong> independently verified the trial evidence underneath it. Sections 5 and 10 rest largely on this tier.',
            'where this document has <strong>not</strong> independently verified the trial evidence underneath it. <strong>This applies to consensus statements as well as graded guideline recommendations</strong>, so an EBMT or EHA position adopted here is tier G however strongly it is worded, unless its underlying evidence has been read at source and independently meets another tier. Sections 5 and 10 rest largely on this tier.')

# =============================== 7. sidebar note — points at the wrong section
h = soft(h, "Each line quotes that treatment's own entry in section 15.",
            "Each line quotes that treatment&rsquo;s own entry in section 18.")
h = soft(h, 'Each line quotes that treatment&rsquo;s own entry in section 15.',
            'Each line quotes that treatment&rsquo;s own entry in section 18.')

# =============================== 8. sonrotoclax into the England-access sidebar
h = must(h,
  '<a href="#status-epcoritamab-rr">',
  '<a href="#status-sonrotoclax">Sonrotoclax</a><span class="detail">Approved in the United States after at least two lines including a BTK inhibitor; no Great Britain licence and no national route, so United Kingdom access is through a trial only.</span></span></li>\n          <li><span class="access-dot red"></span><span class="label"><a href="#status-epcoritamab-rr">')
# =============================== 9. skip link lands before the draft warning
h = must(h, '<a class="skip-link" href="#main-content">Skip to main content</a>',
            '<a class="skip-link" href="#draft-warning-heading">Skip to the draft status warning</a>\n'
            '<a class="skip-link" href="#main-content">Skip to main content</a>')

# =============================== 10. mobile: stop hiding global links outright
h = must(h, '      .site-brand-copy small,.site-links a:not(.active) { display:none; }',
            '      .site-brand-copy small { display:none; }\n'
            '      .site-links { flex-wrap:wrap; gap:2px; justify-content:flex-end; }\n'
            '      .site-links a { padding:5px 7px; font-size:.72rem; }')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d' % (OUT, len(h)))
