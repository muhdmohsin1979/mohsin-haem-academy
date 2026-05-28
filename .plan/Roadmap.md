# Roadmap (planning awareness)

Mirror of the locked Track A month order, plus a dependency map and planning notes. This file is for planning awareness only. It does not change the locked month order or task list. Any conflict between this file and the locked plan is resolved in favour of the locked plan.

## Track A month table

| Month | Dates | Focus | Site | Hours |
|-------|-------|-------|------|-------|
| 1 | 17 May to 16 Jun 2026 | Audit and tidy (observation only) | Both | 2 |
| 2 | 17 Jun to 16 Jul 2026 | Shared header, footer, CSS variables | MHA primarily | 3 |
| 3 | 17 Jul to 16 Aug 2026 | Tests for reversal calculator | haemcalc/reversal | 2 |
| 4 | 17 Aug to 16 Sep 2026 | Accessibility basics | Both | 2 |
| 5 | 17 Sep to 16 Oct 2026 | SEO basics | Both | 2 |
| 6 | 17 Oct to 16 Nov 2026 | Analytics (Plausible or Umami) | Both | 1 |
| 7 | 17 Nov to 16 Dec 2026 | PWA manifest | HaemCalc | 2 |
| 8 | 17 Dec 2026 to 16 Jan 2027 | Feedback mechanism | Both | 1 |
| 9 | 17 Jan to 16 Feb 2027 | Citation audit (top 10 calculators) | HaemCalc | 3 |
| 10 | 17 Feb to 16 Mar 2027 | Architecture notes | Both | 1 |
| 11 | 17 Mar to 16 Apr 2027 | Accessibility pass 2 (WCAG 2.1 AA) | Both | 2 |
| 12 | 17 Apr to 16 May 2027 | Year review and Year 2 planning | Both | 1 |

## Dependency Map

| Month | Depends on | Notes |
|-------|-----------|-------|
| 6 (Analytics) | 5 (SEO) | Analytics platform choice should be confirmed during Month 5 |
| 7 (PWA) | 6 (Analytics) | PWA install events and engagement metrics require analytics baseline |
| 9 (Citation audit) | 6 (Analytics) | Prioritise audit by traffic data collected since Month 6 |
| 11 (Accessibility pass 2) | 4 (Accessibility) | Pass 2 reviews and extends the work done in Month 4 |
| 12 (Year review) | All months | Requires completed Quarterly-Reviews.md entries and Decisions.md |

This map is for planning awareness only. It does not change the month order, which is locked.

## Planning notes by month

These are notes, not tasks. They do not add to, remove from, or reorder the locked task list. They are recorded here (rather than in the locked plan document) so the locked document is not edited mid-year.

**Month 3 (Tests), testing framework:** Before writing tests in Month 3, decide on the approach. For HaemCalc (React), Jest with React Testing Library is the standard choice. For MHA (static HTML/JS), vanilla JS assertions or a lightweight runner such as QUnit are appropriate. Document the decision in Decisions.md so it is not revisited.

**Month 6 (Analytics), platform decision:** Before beginning Month 6 analytics work, confirm which platform will be used (Plausible, Fathom, or Google Analytics 4) so that any instrumentation from Month 5 SEO work (UTM parameters, event naming) is consistent with the analytics implementation.

**Month 9 (Citation audit), dependency:** Month 9 citation audit will be more effective if analytics data from Month 6 onwards is available. Prioritise auditing the highest-traffic pages and calculators first.
