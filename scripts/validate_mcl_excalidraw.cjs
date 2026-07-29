#!/usr/bin/env node
"use strict";

/* Render the exact saved MCL scene through the pinned official Excalidraw package. */
const fs = require("fs");
const os = require("os");
const path = require("path");
const esbuild = require("esbuild");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const scenePath = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(root, "docs", "mcl-v2", "preview", "algorithm-working.excalidraw");
const scene = JSON.parse(fs.readFileSync(scenePath, "utf8"));
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "mcl-excalidraw-audit-"));
const bundle = path.join(temp, "excalidraw.js");

async function main() {
  await esbuild.build({
    stdin: {
      contents: "import * as E from '@excalidraw/excalidraw'; window.ExcalOfficial = E;",
      resolveDir: process.env.MCL_EXCAL_NODE_ROOT || process.cwd(),
      sourcefile: "mcl-excalidraw-entry.js",
    },
    bundle: true,
    format: "iife",
    platform: "browser",
    outfile: bundle,
    logLevel: "silent",
  });

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1040, height: 2100 } });
    await page.setContent("<!doctype html><meta charset='utf-8'><style>html,body{margin:0}svg{display:block}</style>");
    await page.addScriptTag({ path: bundle });
    const audit = await page.evaluate(async (rawScene) => {
      const restored = window.ExcalOfficial.restore(rawScene, null, null, {
        refreshDimensions: true,
        repairBindings: true,
      });
      const output = {
        type: "excalidraw",
        version: 2,
        source: "https://excalidraw.com",
        elements: restored.elements,
        appState: restored.appState,
        files: restored.files,
      };
      const svg = await window.ExcalOfficial.exportToSvg(output);
      document.body.appendChild(svg);
      await document.fonts.ready;

      const failures = [];
      const svgRect = svg.getBoundingClientRect();
      const boxes = [...svg.querySelectorAll("text")].map((node) => ({
        text: (node.textContent || "").trim(),
        rect: node.getBoundingClientRect(),
      })).filter((item) => item.text);

      for (const item of boxes) {
        const rect = item.rect;
        if (rect.left < svgRect.left - 1 || rect.top < svgRect.top - 1 ||
            rect.right > svgRect.right + 1 || rect.bottom > svgRect.bottom + 1) {
          failures.push(`Text outside SVG bounds: ${item.text}`);
        }
      }
      for (let i = 0; i < boxes.length; i += 1) {
        for (let j = i + 1; j < boxes.length; j += 1) {
          const a = boxes[i].rect;
          const b = boxes[j].rect;
          const width = Math.min(a.right, b.right) - Math.max(a.left, b.left);
          const height = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
          if (width > 1 && height > 1) {
            failures.push(`Overlapping text: ${boxes[i].text} <> ${boxes[j].text}`);
          }
        }
      }

      const fullText = svg.textContent || "";
      const required = [
        "MANTLE CELL LYMPHOMA", "WORKING PREVIEW", "NOT FOR CLINICAL USE",
        "YOUNGER / TREATMENT-FIT", "TP53-MUTATED / HIGH RISK",
        "EXACTLY ONE PREVIOUS LINE", "COVALENT-BTKi INTOLERANCE",
        "COVALENT-BTKi PROGRESSION", "TA677 CDF MANAGED ACCESS",
        "TRIAL / EARLY / EXCEPTIONAL ROUTES", "PHARMACY AND SUPPORTIVE-CARE HOLD POINT",
      ];
      for (const phrase of required) {
        if (!fullText.includes(phrase)) failures.push(`Rendered SVG missing: ${phrase}`);
      }
      for (const forbidden of ["AUTHORISED FOR PUBLICATION", "PUBLISHED v2.0"]) {
        if (fullText.includes(forbidden)) failures.push(`Rendered SVG has forbidden status: ${forbidden}`);
      }

      const stateTitles = new Set([
        "EXACTLY ONE PREVIOUS LINE", "COVALENT-BTKi INTOLERANCE", "COVALENT-BTKi PROGRESSION",
      ]);
      const states = restored.elements.filter((element) =>
        element.type === "text" && stateTitles.has(element.text));
      if (states.length !== 3) failures.push(`Expected three independent R/R states; found ${states.length}`);
      const stateJoiningArrows = restored.elements.filter((element) => {
        if (element.type !== "arrow") return false;
        const ys = (element.points || []).map((point) => element.y + point[1]);
        return ys.length && Math.min(...ys) >= 1075 && Math.max(...ys) <= 1395;
      });
      if (stateJoiningArrows.length) failures.push("Arrow detected between independent R/R classification states");

      return { failures, textNodeCount: boxes.length, stateCount: states.length };
    }, scene);

    if (audit.failures.length) throw new Error(audit.failures.join("\n"));
    console.log(`official MCL Excalidraw render audit: PASS (${audit.textNodeCount} text lines; ${audit.stateCount} independent states)`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(`official MCL Excalidraw render audit: FAIL\n${error.stack || error}`);
  process.exitCode = 1;
}).finally(() => {
  fs.rmSync(temp, { recursive: true, force: true });
});
