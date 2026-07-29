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
    const desktop = await browser.newPage({ viewport: { width: 1440, height: 600 }, deviceScaleFactor: 1 });
    await desktop.goto(`file://${target}`, { waitUntil: "load" });
    const desktopResult = await desktop.evaluate(() => {
      const anchor = document.querySelector(".anchor-nav");
      const sidebar = document.querySelector(".gl-sidebar");
      const layout = document.querySelector(".gl-layout");
      const siteNav = document.querySelector(".site-nav-shell");
      if (!anchor || !sidebar || !layout || !siteNav) return { missing: true };
      const pageScrollBefore = window.scrollY;
      sidebar.scrollTop = 120;
      return {
        missing: false,
        anchorPosition: getComputedStyle(anchor).position,
        anchorTopStyle: getComputedStyle(anchor).top,
        siteNavPosition: getComputedStyle(siteNav).position,
        siteNavTopStyle: getComputedStyle(siteNav).top,
        sidebarPosition: getComputedStyle(sidebar).position,
        sidebarOverflowY: getComputedStyle(sidebar).overflowY,
        sidebarClientHeight: sidebar.clientHeight,
        sidebarScrollHeight: sidebar.scrollHeight,
        sidebarScrollTop: sidebar.scrollTop,
        pageScrollUnchangedBySidebar: window.scrollY === pageScrollBefore,
        layoutColumns: getComputedStyle(layout).gridTemplateColumns,
      };
    });
    await desktop.evaluate(() => {
      document.documentElement.style.scrollBehavior = "auto";
      window.scrollTo(0, 1500);
    });
    await desktop.waitForTimeout(50);
    const stickyTop = await desktop.locator(".anchor-nav").evaluate((element) => element.getBoundingClientRect().top);
    await desktop.screenshot({ path: "/tmp/mcl-layout-desktop.png", fullPage: false });

    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await page.goto(`file://${target}`, { waitUntil: "load" });
    const result = await page.evaluate(() => {
      const object = document.querySelector(".algorithm-preview");
      const mobileLink = document.querySelector(".mobile-algorithm-link");
      const warning = document.querySelector("aside.warning");
      const sidebar = document.querySelector(".gl-sidebar");
      return {
        viewportWidth: window.innerWidth,
        clientWidth: document.documentElement.clientWidth,
        scrollWidth: document.documentElement.scrollWidth,
        objectDisplay: object ? getComputedStyle(object).display : null,
        mobileLinkDisplay: mobileLink ? getComputedStyle(mobileLink).display : null,
        warningRole: warning && warning.getAttribute("role"),
        sidebarDisplay: sidebar ? getComputedStyle(sidebar).display : null,
        sidebarPosition: sidebar ? getComputedStyle(sidebar).position : null,
        sidebarOverflowY: sidebar ? getComputedStyle(sidebar).overflowY : null,
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
    await page.screenshot({ path: "/tmp/mcl-layout-mobile.png", fullPage: false });
    const failures = [];
    if (desktopResult.missing) failures.push("desktop CLL-pattern navigation structure is missing");
    if (!desktopResult.missing && desktopResult.anchorPosition !== "sticky") failures.push(`anchor navigation is not sticky: ${desktopResult.anchorPosition}`);
    if (!desktopResult.missing && desktopResult.siteNavPosition !== "sticky") failures.push(`Academy navigation is not sticky: ${desktopResult.siteNavPosition}`);
    if (!desktopResult.missing && desktopResult.siteNavTopStyle !== "0px") failures.push(`Academy navigation top is not locked: ${desktopResult.siteNavTopStyle}`);
    if (!desktopResult.missing && desktopResult.anchorTopStyle !== "56px") failures.push(`anchor navigation does not follow CLL top offset: ${desktopResult.anchorTopStyle}`);
    if (!desktopResult.missing && Math.abs(stickyTop - 56) > 1) failures.push(`anchor navigation did not remain below the Academy nav after scroll: ${stickyTop}`);
    if (!desktopResult.missing && desktopResult.sidebarPosition !== "sticky") failures.push(`sidebar is not sticky: ${desktopResult.sidebarPosition}`);
    if (!desktopResult.missing && desktopResult.sidebarOverflowY !== "auto") failures.push(`sidebar does not scroll independently: ${desktopResult.sidebarOverflowY}`);
    if (!desktopResult.missing && desktopResult.sidebarScrollHeight <= desktopResult.sidebarClientHeight) failures.push("sidebar content does not create an independent scroll region");
    if (!desktopResult.missing && desktopResult.sidebarScrollTop <= 0) failures.push("sidebar scroll position did not change independently");
    if (!desktopResult.missing && !desktopResult.pageScrollUnchangedBySidebar) failures.push("sidebar scroll changed the document scroll position");
    if (!desktopResult.missing && desktopResult.layoutColumns.split(" ").length < 2) failures.push(`desktop layout is not two-column: ${desktopResult.layoutColumns}`);
    if (result.viewportWidth !== 390 || result.clientWidth !== 390 || result.scrollWidth > 390) {
      failures.push(`horizontal overflow: viewport=${result.viewportWidth} client=${result.clientWidth} scroll=${result.scrollWidth} offenders=${JSON.stringify(result.overflowElements)}`);
    }
    if (result.objectDisplay !== "none") failures.push("embedded long algorithm remains visible at 390px");
    if (result.mobileLinkDisplay === "none" || result.mobileLinkDisplay === null) failures.push("full-size mobile algorithm link is hidden");
    if (result.warningRole !== "note") failures.push("publication notice role changed");
    if (result.sidebarDisplay === "none") failures.push("CLL-pattern sidebar disappeared on mobile instead of becoming an in-flow card");
    if (result.sidebarPosition !== "static") failures.push(`mobile sidebar does not follow CLL static pattern: ${result.sidebarPosition}`);
    if (result.sidebarOverflowY !== "visible") failures.push(`mobile sidebar retains an independent scroll region: ${result.sidebarOverflowY}`);
    if (result.robots !== "index, follow") failures.push(`production robots directive is incorrect: ${result.robots}`);
    for (const phrase of ["PUBLISHED 29 JULY 2026", "Published specialist guideline", "Publication authority", "TRUE — 29 JULY 2026"]) {
      if (!result.visibleText.includes(phrase)) failures.push(`missing visible phrase: ${phrase}`);
    }
    for (const phrase of ["WORKING PREVIEW", "NOT FOR CLINICAL USE", "no publication authority"]) {
      if (result.visibleText.includes(phrase)) failures.push(`stale preview phrase: ${phrase}`);
    }
    if (failures.length) throw new Error(failures.join("\n"));
    console.log(`MCL production browser audit: PASS desktop=sticky+independent-sidebar mobile=${result.viewportWidth}px scroll=${result.scrollWidth} algorithm=${result.objectDisplay}`);
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
