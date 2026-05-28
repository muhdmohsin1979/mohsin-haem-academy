# Decisions Log

This file records technical and editorial decisions made during the project. Its purpose is to prevent the same ground being covered twice in future sessions.

## Format

Each entry uses the following structure:

```
---
Date: [YYYY-MM-DD]
Decision: [What was decided]
Context: [Why this decision was needed]
Options considered: [What alternatives were weighed]
Rationale: [Why this option was chosen]
Revisit trigger: [Under what circumstances this decision should be reconsidered, or "None"]
---
```

## Entries

---
Date: 2026-05-28
Decision: PENDING. Testing framework for Month 3.
Context: Month 3 (17 Jul to 16 Aug 2026) writes tests for the reversal calculator. The framework should be settled before the month starts so test-writing time is not spent on tooling decisions.
Options considered: Jest with React Testing Library (for HaemCalc, React); QUnit or vanilla JS assertions (for MHA, static HTML/JS).
Rationale: To be confirmed.
Revisit trigger: Confirm before Month 3 begins (17 Jul 2026).
Status: PENDING
---

---
Date: 2026-05-28
Decision: PENDING. Analytics platform for Month 6.
Context: Month 6 (17 Oct to 16 Nov 2026) sets up analytics. The platform choice should be settled before Month 5 SEO work ends so that any instrumentation (UTM parameters, event naming) is consistent.
Options considered: Plausible, Fathom, Google Analytics 4.
Rationale: To be confirmed.
Revisit trigger: Confirm before Month 5 ends (16 Oct 2026).
Status: PENDING
---
