#!/usr/bin/env node
/** Run offline axe-core against the exact MCL v2.1 reviewed web preview. */

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const modules = process.env.MCL_AXE_NODE_MODULES;
if (!modules) throw new Error('MCL_AXE_NODE_MODULES must point to an isolated node_modules directory');
const requireFromModules = createRequire(path.join(modules, 'package.json'));
const { chromium } = requireFromModules('playwright-core');
const axePath = requireFromModules.resolve('axe-core/axe.min.js');
const axeSource = fs.readFileSync(axePath, 'utf8');
const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!fs.existsSync(chrome)) throw new Error(`Chrome not found: ${chrome}`);

const target = path.join(root, 'docs/mcl-v2.1/web-preview/index.html');
const browser = await chromium.launch({ executablePath: chrome, headless: true });
const report = { target: pathToFileURL(target).href, axeVersion: null, viewports: {} };
try {
  for (const width of [1280, 375]) {
    const page = await browser.newPage({ viewport: { width, height: 1000 } });
    await page.goto(pathToFileURL(target).href, { waitUntil: 'load' });
    await page.addScriptTag({ content: axeSource });
    const result = await page.evaluate(async () => {
      const run = await globalThis.axe.run(document, {
        runOnly: {
          type: 'tag',
          values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'],
        },
      });
      return {
        version: globalThis.axe.version,
        passes: run.passes.length,
        violations: run.violations.map((item) => ({
          id: item.id,
          impact: item.impact,
          help: item.help,
          targets: item.nodes.map((node) => node.target.join(' ')),
          failureSummaries: item.nodes.map((node) => node.failureSummary),
        })),
        incomplete: run.incomplete.map((item) => ({ id: item.id, nodes: item.nodes.length })),
      };
    });
    report.axeVersion = result.version;
    report.viewports[String(width)] = result;
    await page.close();
  }
} finally {
  await browser.close();
}

const output = path.join(root, 'docs/mcl-v2.1/web-preview/axe-report.json');
fs.writeFileSync(output, `${JSON.stringify(report, null, 2)}\n`);
const violations = Object.values(report.viewports).flatMap((item) => item.violations);
if (violations.length) {
  console.error(JSON.stringify(report, null, 2));
  throw new Error(`MCL v2.1 axe violations: ${violations.length}`);
}
console.log(`MCL v2.1 offline Axe: PASS axe=${report.axeVersion} widths=1280,375 violations=0 report=${output}`);
