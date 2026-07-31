#!/usr/bin/env python3
"""Stage 15: release-control status conversion under recorded owner attestation.

This stage changes NOTHING about the clinical or regulatory content. It converts
the two review-gate labels from PENDING to their attested state, propagates that
to the per-drug pharmacy fields so the document does not contradict itself, and
adds an attestation record that states exactly where the attestation came from
and what it does not establish.

Publication authority stays FALSE. The draft banner, the unratified state and
the robots noindex directive stay in place: those belong to later gates.
"""
import sys, io

SRC = '/home/claude/mcl-v2.1-draft.html'
OUT = '/home/claude/mcl-v2.1-draft.html'
h = io.open(SRC, encoding='utf-8').read()


def must(html, needle, repl, n=1):
    if needle not in html:
        sys.exit('NEEDLE NOT FOUND: %r' % needle[:180])
    return html.replace(needle, repl, n)


C4 = 'f16545565f7cb0c3619aa2ccff87f1fecd2ecc5718d4dae4d0960a09e9f77957'
C5 = '3b073bcaa8887018702cb2af53d4e655c59b82e7c7e2333548feb14d3bb4fba2'

# =========================================================== 1. draft banner
h = must(h,
  'This is a revision candidate prepared for the accountable owner. Independent clinical review is <strong>PENDING</strong> and pharmacy verification is <strong>PENDING</strong> for all material added since v2.0. It carries no publication authority and must not be used to make a treatment or funding decision. The published guideline remains v2.0.',
  'This is a controlled preview candidate. Independent clinical review is recorded as <strong>PASS</strong> and pharmacy verification as <strong>COMPLETE</strong> on the accountable owner&rsquo;s attestation of 31 July 2026, with verifier identities retained privately at the owner&rsquo;s instruction. Those two gates are cleared; the remaining ones are not. The document still carries <strong>no publication authority</strong>, remains unratified, and must not be used to make a treatment or funding decision. The published guideline remains v2.0.')

# =========================================================== 2. audit paragraph
h = must(h,
  'Those corrections do <strong>not</strong> change the release state: this remains unratified, clinical review and pharmacy verification remain pending, and publication authority remains false.',
  'Those corrections did <strong>not</strong> of themselves change the release state. The clinical-review and pharmacy gates were cleared separately, by owner attestation on 31 July 2026, and not because factual corrections had been made. This document remains unratified and publication authority remains false.')

# =========================================================== 3. release-control table
h = must(h,
  '<tr><th scope="row">Owner scope approval</th><td>PENDING — owner scope approval for v2.1 not yet given</td></tr>\n'
  '<tr><th scope="row">Independent clinical review</th><td>PENDING — not yet performed for v2.1 content</td></tr>\n'
  '<tr><th scope="row">Pharmacy verification</th><td>PENDING — v2.0 verification does not extend to v2.1 additions</td></tr>\n'
  '<tr><th scope="row">Publication authority</th><td>FALSE — no publication authority</td></tr>',
  '<tr><th scope="row">Owner scope approval</th><td>CONFIRMED — 31 July 2026</td></tr>\n'
  '<tr><th scope="row">Independent clinical review</th><td>PASS — recorded on owner attestation, 31 July 2026</td></tr>\n'
  '<tr><th scope="row">Pharmacy verification</th><td>COMPLETE — recorded on owner attestation, 31 July 2026; verifier identity retained privately</td></tr>\n'
  '<tr><th scope="row">Publication authority</th><td>FALSE — no publication authority</td></tr>\n'
  '<tr><th scope="row">Reviewed substantive candidate</th><td>SHA-256 <code style="word-break:break-all;">' + C4 + '</code></td></tr>\n'
  '<tr><th scope="row">Accessibility correction</th><td>SHA-256 <code style="word-break:break-all;">' + C5 + '</code> — one colour token in the diagrams, no content change</td></tr>\n'
  '<tr><th scope="row">Change from the reviewed candidate</th><td>Release-control presentation only</td></tr>')

# =========================================================== 4. attestation record
h = must(h,
  '      </tbody>\n    </table>\n  </section>\n    </main>',
  '      </tbody>\n    </table>\n'
  '    <h3>Attestation record</h3>\n'
  '    <p>The clinical-review and pharmacy gates were cleared by the accountable owner on 31 July 2026. '
  'The attestation was recorded in the drafting session; verifier identities are retained privately at the '
  'owner&rsquo;s instruction and appear in no file, manifest or commit. Anyone relying on this record should '
  'understand three things about its limits.</p>\n'
  '    <ul>\n'
  '      <li>The build did not witness either review. It records what the owner attested, on the owner&rsquo;s '
  'authority, and has not independently corroborated it.</li>\n'
  '      <li>The attestation binds to the substantive candidate <code style="word-break:break-all;">' + C4 + '</code>. '
  'The present file differs from it in two respects only: one diagram colour token changed to meet a contrast '
  'threshold, and this release-control text. No clinical statement, evidence tier, access class, figure or '
  'section reference differs.</li>\n'
  '      <li>Clearing these two gates does not make the document publishable. It remains unratified, carries '
  'no publication authority, is served with a robots noindex directive, and the two unresolved literature '
  'corrections recorded in section 19 are still unresolved.</li>\n'
  '    </ul>\n'
  '  </section>\n    </main>')

# =========================================================== 5. per-drug pharmacy fields
n1 = h.count('REPORT_ONLY_NOT_PHARMACY_VERIFIED — exact MHRA SmPC quotations validated; human pharmacy verification pending.')
h = h.replace(
  'REPORT_ONLY_NOT_PHARMACY_VERIFIED — exact MHRA SmPC quotations validated; human pharmacy verification pending.',
  'PHARMACY_VERIFIED — exact MHRA SmPC quotations validated; human pharmacy verification recorded 31 July 2026 on owner attestation, verifier identity retained privately.')
n2 = h.count('REPORT_ONLY_TRIAL_AND_GUIDELINE_SCHEDULE_NOT_PHARMACY_VERIFIED')
h = h.replace('REPORT_ONLY_TRIAL_AND_GUIDELINE_SCHEDULE_NOT_PHARMACY_VERIFIED',
              'PHARMACY_VERIFIED_TRIAL_AND_GUIDELINE_SCHEDULE — recorded 31 July 2026 on owner attestation')
n3 = h.count('REPORT_ONLY_TRIAL_SCHEDULE_NOT_PHARMACY_VERIFIED')
h = h.replace('REPORT_ONLY_TRIAL_SCHEDULE_NOT_PHARMACY_VERIFIED',
              'PHARMACY_VERIFIED_TRIAL_SCHEDULE — recorded 31 July 2026 on owner attestation')
if (n1, n2, n3) != (10, 1, 1):
    sys.exit('UNEXPECTED PHARMACY FIELD COUNTS: %r' % ((n1, n2, n3),))

# =========================================================== 6. document code
h = h.replace('MHA-MCL-2026-v2.1-DRAFT', 'MHA-MCL-2026-v2.1-PREVIEW-RC1')

io.open(OUT, 'w', encoding='utf-8').write(h)
print('WROTE %s bytes=%d pharmacy_fields=%d' % (OUT, len(h), n1 + n2 + n3))
