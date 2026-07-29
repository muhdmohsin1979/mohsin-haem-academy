#!/usr/bin/env node
"use strict";

const { chromium } = require("playwright");
const path = require("path");

const root = path.resolve(__dirname, "..");
const target = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(root, "guidelines", "mcl", "index.html");

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await page.goto(`file://${target}`, { waitUntil: "load" });
    const result = await page.evaluate(() => {
      const object = document.querySelector(".algorithm-preview");
      const mobileLink = document.querySelector(".mobile-algorithm-link");
      const warning = document.querySelector("aside.warning");
      return {
        viewportWidth: window.innerWidth,
        clientWidth: document.documentElement.clientWidth,
        scrollWidth: document.documentElement.scrollWidth,
        objectDisplay: object ? getComputedStyle(object).display : null,
        mobileLinkDisplay: mobileLink ? getComputedStyle(mobileLink).display : null,
        warningRole: warning && warning.getAttribute("role"),
        robots: document.querySelector('meta[name="robots"]')?.content,
        visibleText: document.body.innerText,
        overflowElements: [...document.querySelectorAll("body *")].filter((element) => {
          const rect = element.getBoundingClientRect();
          return rect.right > document.documentElement.clientWidth + 1 || rect.left < -1 || element.scrollWidth > element.clientWidth + 1;
        }).slice(0, 20).map((element) => ({
          tag: element.tagName,
          id: element.id,
          className: String(element.className || ""),
          left: element.getBoundingClientRect().left,
          right: element.getBoundingClientRect().right,
          clientWidth: element.clientWidth,
          scrollWidth: element.scrollWidth,
        })),
      };
    });
    const failures = [];
    if (result.viewportWidth !== 390 || result.clientWidth !== 390 || result.scrollWidth > 390) {
      failures.push(`horizontal overflow: viewport=${result.viewportWidth} client=${result.clientWidth} scroll=${result.scrollWidth} offenders=${JSON.stringify(result.overflowElements)}`);
    }
    if (result.objectDisplay !== "none") failures.push("embedded long algorithm remains visible at 390px");
    if (result.mobileLinkDisplay === "none" || result.mobileLinkDisplay === null) failures.push("full-size mobile algorithm link is hidden");
    if (result.warningRole !== "note") failures.push("publication notice role changed");
    if (result.robots !== "index, follow") failures.push(`production robots directive is incorrect: ${result.robots}`);
    for (const phrase of ["PUBLISHED 29 JULY 2026", "Published specialist guideline", "Publication authority", "TRUE — 29 JULY 2026"]) {
      if (!result.visibleText.includes(phrase)) failures.push(`missing visible phrase: ${phrase}`);
    }
    for (const phrase of ["WORKING PREVIEW", "NOT FOR CLINICAL USE", "no publication authority"]) {
      if (result.visibleText.includes(phrase)) failures.push(`stale preview phrase: ${phrase}`);
    }
    if (failures.length) throw new Error(failures.join("\n"));
    console.log(`MCL production mobile browser audit: PASS viewport=${result.viewportWidth} client=${result.clientWidth} scroll=${result.scrollWidth} algorithm=${result.objectDisplay} mobileLink=${result.mobileLinkDisplay}`);
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
