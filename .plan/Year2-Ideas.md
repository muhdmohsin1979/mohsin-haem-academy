# Year 2 Ideas

Out-of-plan ideas spotted during the Year 1 maintenance plan. Logged here, not actioned. Consolidated into the Year 2 plan at the Month 12 review.

Logging an idea here is not the same as actioning it. Where an entry's field 6 says "Yes", that two-check requirement applies when the idea is implemented, not to the act of logging it.

## Field format

Each entry uses the following fields:

0. Date spotted
1. Issue identified
2. Why it matters
3. Urgency
4. Proposed action
5. Year 2 candidate (Y/N)
6. Two confirmations needed (Y/N)

If an existing entry predates this format and has no recorded date, the value is `[date unknown]`.

---

## Entry 1: HaemCalc SPA indexability

0. **Date spotted:** 28 May 2026
1. **Issue identified:** HaemCalc is a React single-page application. Individual calculator pages do not have unique, indexable URLs. Search engines cannot index individual calculators as distinct pages.
2. **Why it matters:** This is a significant organic search gap. Users searching for specific haematology calculators by name cannot find them directly via Google. As the site grows, this limits discoverability and undermines any SEO investment made elsewhere.
3. **Urgency:** Low (does not affect current users; affects growth ceiling)
4. **Proposed action:** Evaluate React Router hash-based vs history-based routing. Consider server-side rendering (SSR) or static site generation (SSG) for calculator pages. Assess Cloudflare Pages compatibility with SSR options. Full architectural decision required.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** Yes (touches architecture, which may affect locked Month 10 scope)

---

## Entry 2: Open Graph and Twitter Card tags on HaemCalc

0. **Date spotted:** 28 May 2026
1. **Issue identified:** HaemCalc has no Open Graph or Twitter Card metadata. When links are shared on social media or messaging platforms, no preview card is generated.
2. **Why it matters:** HaemCalc tools are likely to be shared by clinicians peer-to-peer. Without OG tags, shared links appear as plain URLs with no context, reducing click-through and credibility.
3. **Urgency:** Low to medium (low effort, moderate impact on shareability)
4. **Proposed action:** Add OG and Twitter Card meta tags to the HaemCalc head. Requires per-page dynamic meta generation given the SPA architecture, so may depend on Entry 1 (SPA indexability) being resolved first.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** No (does not touch locked items; deferred because it depends on SPA architecture decisions)

---

## Entry 3: Cookie consent upgrade on MHA

0. **Date spotted:** 28 May 2026
1. **Issue identified:** The current cookie consent implementation on mohsinhaemacademy.com does not offer granular accept/reject controls. Under UK GDPR, users must be able to reject non-essential cookies as easily as they can accept them.
2. **Why it matters:** This is a compliance gap. While enforcement risk for a small educational site is low, the principle of data minimisation and informed consent is important, particularly for a clinical professional's site.
3. **Urgency:** Medium (compliance; low enforcement risk but a matter of principle)
4. **Proposed action:** Replace or upgrade the existing consent banner with a solution that provides clearly labelled accept/reject options per cookie category (analytics, functional). Options include a lightweight custom solution or a free tier of a consent management platform such as Cookiebot or Osano.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** No (does not touch locked items)

---

## Entry 4: Pricing and access model clarification on HaemCalc

0. **Date spotted:** 28 May 2026
1. **Issue identified:** The HaemCalc About page does not explain the pricing or access model to new visitors. It is unclear whether the site is free, freemium, or subscription-based.
2. **Why it matters:** Confused visitors do not convert. A clinician landing on HaemCalc for the first time needs to understand within seconds what they can access and on what terms. Lack of clarity erodes trust.
3. **Urgency:** Medium (affects conversion and user trust)
4. **Proposed action:** Add a clear, plain-English access/pricing section to the HaemCalc About page. Include what is free, what requires registration or payment, and what the rationale is.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** No (does not touch locked items; content change only)

---

## Entry 5: MHA About page biographical depth

0. **Date spotted:** 28 May 2026
1. **Issue identified:** The mohsinhaemacademy.com About page lacks qualifications, publications, and institutional affiliation. For a site aimed at trainees and clinicians, the author's credentials are part of the content's credibility.
2. **Why it matters:** Medical education content carries implicit trust requirements. A trainee deciding whether to rely on MHA content will weigh the author's credibility. A thin About page undermines that trust regardless of content quality.
3. **Urgency:** Low to medium (trust and credibility; low technical effort)
4. **Proposed action:** Expand the MHA About page to include GMC-registered specialty, hospital or trust affiliation if comfortable disclosing, relevant publications or presentations, professional memberships (BSH, RCPath etc.), and a brief statement of the site's educational intent and scope.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** No (does not touch locked items; content change only)

---

## Entry 6: Schema.org structured data on HaemCalc

0. **Date spotted:** 28 May 2026
1. **Issue identified:** HaemCalc has no Schema.org structured data. Relevant schema types include MedicalWebPage and SoftwareApplication.
2. **Why it matters:** Structured data helps search engines understand what HaemCalc pages are and what they do. This gap compounds the SPA indexability issue (Entry 1).
3. **Urgency:** Low (depends on Entry 1 being resolved; structured data on non-indexable pages has limited value)
4. **Proposed action:** Once SPA routing is resolved (Entry 1), add JSON-LD structured data blocks to each calculator page. Use MedicalWebPage and SoftwareApplication at minimum.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** No (does not touch locked items; depends on Entry 1)

---

## Entry 7: Start Here user flow and single primary CTA (both sites)

0. **Date spotted:** 28 May 2026
1. **Issue identified:** Neither site has a guided first-visit journey. Visitors land on both sites without a clear indication of where to begin. Multiple options compete for attention on the same page with no single dominant call to action.
2. **Why it matters:** This reflects direct UX feedback from a trusted peer which Dr Mohsin has agreed with. Both sites currently leave first-time visitors to figure it out themselves, affecting conversion, session depth, and professional impression.
3. **Urgency:** Medium (affects first impressions on both sites; agreed priority)
4. **Proposed action:** For each site, define the single most valuable action a first-time visitor should take. Add a "New here? Start with this" section or banner to each homepage. Reduce competing CTAs to one primary and one secondary per page. Apply the patient-journey design principle: guide, do not present options.
5. **Year 2 candidate:** Yes
6. **Two confirmations needed:** No (does not touch locked items; design and content change)
