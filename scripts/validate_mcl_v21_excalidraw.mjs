#!/usr/bin/env node
/**
 * Official Excalidraw render gate for the MCL v2.1 editable scenes.
 *
 * Gate id: OFFICIAL_EXCALIDRAW_RENDER_NOT_VERIFIED
 *
 * Every scene must restore through the official @excalidraw/excalidraw library,
 * export through the official exportToSvg, carry every text string that the
 * canonical C5 SVG carries, keep all text inside the exported bounds, avoid
 * text-to-text collisions, and stay semantically equal to the C5 SVG.
 *
 * Three things were wrong with the previous revision of this script and are
 * fixed here, because each of them turned a real failure into a silent one:
 *
 *   1. esbuild ran at logLevel 'silent' and the injected bundle's runtime
 *      errors were never captured, so a bundle that threw on load presented
 *      as "globalThis.ExcalOfficial is undefined" with no cause. Page errors
 *      and console errors are now collected and reported.
 *   2. process.env.NODE_ENV was left undefined. The Excalidraw production
 *      entry reads it at module scope; in a bare page that throws before the
 *      global is assigned. It is now defined at build time.
 *   3. The toolchain was resolved from an ad-hoc directory passed by
 *      environment variable, with no pinned versions, so the gate was not
 *      reproducible. It now resolves from tools/excalidraw-validator, whose
 *      package-lock.json pins every version. The environment variable is still
 *      honoured as an override.
 *
 * Semantic equality is defined, and deliberately not overstated:
 *   - the ordered sequence of text strings must be identical;
 *   - measured in SVG user units, each text box's offset from the first text
 *     box must match the C5 SVG within MAX_DY vertically and MAX_DX
 *     horizontally. Horizontal tolerance is the looser of the two because the
 *     scene generator estimates text width as len * fontSize * 0.58 while the
 *     renderer uses real font metrics; that estimate only shifts centre-
 *     anchored labels, of which there are three or four per diagram.
 *
 * Both documents are measured after dividing client pixels by the rendered
 * scale factor. The C5 SVGs carry a viewBox and no width, so a browser
 * stretches them to the container; comparing raw client pixels against the
 * Excalidraw export, which carries an explicit width, compares two different
 * scales and produces a spurious failure that grows with line number.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const names = ['first-line', 'high-risk', 'relapsed', 'access-route'];
const MAX_DY = 1.5;
const MAX_DX = 12.0;

const pinned = path.join(root, 'tools', 'excalidraw-validator', 'node_modules');
const modules = process.env.MCL_AXE_NODE_MODULES || pinned;
if (!fs.existsSync(modules)) {
  throw new Error(
    `Excalidraw validator toolchain missing at ${modules}.\n` +
    'Run: npm ci --prefix tools/excalidraw-validator\n' +
    'Versions are pinned in tools/excalidraw-validator/package-lock.json.',
  );
}
const requireFromModules = createRequire(path.join(modules, 'package.json'));
const esbuild = requireFromModules('esbuild');
const { chromium } = requireFromModules('playwright-core');

const excalidrawVersion = JSON.parse(
  fs.readFileSync(path.join(modules, '@excalidraw', 'excalidraw', 'package.json'), 'utf8'),
).version;

function resolveChrome() {
  if (process.env.MCL_CHROME_PATH) return process.env.MCL_CHROME_PATH;
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    '/usr/bin/chromium',
    '/usr/bin/google-chrome',
  ];
  for (const candidate of candidates) if (fs.existsSync(candidate)) return candidate;
  throw new Error('No Chrome or Chromium found. Set MCL_CHROME_PATH.');
}

const measure = `(() => {
  const svg = document.querySelector('svg');
  const box = svg.getBoundingClientRect();
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const k = vb && vb.width ? box.width / vb.width : 1;
  return [...svg.querySelectorAll('text')]
    .map((node) => {
      const r = node.getBoundingClientRect();
      return {
        text: (node.textContent || '').trim(),
        x: (r.left - box.left) / k,
        y: (r.top - box.top) / k,
        right: (r.right - box.left) / k,
        bottom: (r.bottom - box.top) / k,
        w: box.width / k,
        h: box.height / k,
      };
    })
    .filter((item) => item.text);
})()`;

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'mcl-v21-excalidraw-'));
const bundle = path.join(temp, 'excalidraw.js');
const failures = [];

try {
  await esbuild.build({
    stdin: {
      contents:
        "import { restore, exportToSvg } from '@excalidraw/excalidraw';" +
        'globalThis.ExcalOfficial = { restore, exportToSvg };',
      resolveDir: path.dirname(modules),
      sourcefile: 'mcl-v21-excalidraw-entry.js',
    },
    bundle: true,
    format: 'iife',
    platform: 'browser',
    define: {
      'process.env.NODE_ENV': '"production"',
      'process.env.IS_PREACT': '"false"',
    },
    conditions: ['browser', 'module', 'default'],
    outfile: bundle,
    logLevel: 'warning',
  });

  const browser = await chromium.launch({ executablePath: resolveChrome(), headless: true });
  try {
    for (const name of names) {
      const scenePath = path.join(root, `docs/mcl-v2.1/web-preview/${name}.excalidraw`);
      const svgPath = path.join(root, `docs/mcl-v2.1/web-preview/${name}.svg`);
      const rawScene = JSON.parse(fs.readFileSync(scenePath, 'utf8'));
      const sourceSvg = fs.readFileSync(svgPath, 'utf8');

      // --- reference: the canonical C5 SVG, measured in its own user units
      const refPage = await browser.newPage({ viewport: { width: 1400, height: 2200 } });
      await refPage.setContent(
        '<!doctype html><meta charset="utf-8"><style>html,body{margin:0}svg{display:block}</style>' + sourceSvg,
      );
      const reference = await refPage.evaluate(measure);
      await refPage.close();

      // --- candidate: the editable scene through the official library
      const page = await browser.newPage({ viewport: { width: 1400, height: 2200 } });
      const pageErrors = [];
      page.on('pageerror', (error) => pageErrors.push(`pageerror: ${error.message}`));
      page.on('console', (message) => {
        if (message.type() === 'error') pageErrors.push(`console: ${message.text()}`);
      });
      await page.setContent(
        '<!doctype html><meta charset="utf-8"><style>html,body{margin:0}svg{display:block}</style>',
      );
      await page.addScriptTag({ path: bundle });

      const wired = await page.evaluate(() => typeof globalThis.ExcalOfficial);
      if (wired !== 'object') {
        await page.close();
        throw new Error(
          `official Excalidraw bundle did not expose globalThis.ExcalOfficial (typeof ${wired}).\n` +
          (pageErrors.length ? pageErrors.join('\n') : 'no page error was reported'),
        );
      }

      const rendered = await page.evaluate(async ({ rawScene, measureSource }) => {
        const restored = window.ExcalOfficial.restore(rawScene, null, null, {
          refreshDimensions: false,
          repairBindings: true,
        });
        const output = {
          type: 'excalidraw',
          version: 2,
          source: 'https://excalidraw.com',
          elements: restored.elements,
          appState: restored.appState,
          files: restored.files,
        };
        const svg = await window.ExcalOfficial.exportToSvg(output);
        document.body.appendChild(svg);
        await document.fonts.ready;
        // eslint-disable-next-line no-eval
        return { boxes: eval(measureSource), elementCount: restored.elements.length };
      }, { rawScene, measureSource: measure });
      await page.close();

      const boxes = rendered.boxes;
      const problems = [];

      const missing = reference
        .map((item) => item.text)
        .filter((text) => !boxes.some((box) => box.text === text));
      if (missing.length) problems.push(`missing text: ${JSON.stringify(missing.slice(0, 5))}`);

      const outside = boxes
        .filter((box) => box.x < -1 || box.y < -1 || box.right > box.w + 1 || box.bottom > box.h + 1)
        .map((box) => box.text);
      if (outside.length) problems.push(`text outside bounds: ${JSON.stringify(outside.slice(0, 5))}`);

      const overlaps = [];
      for (let i = 0; i < boxes.length; i += 1) {
        for (let j = i + 1; j < boxes.length; j += 1) {
          const a = boxes[i];
          const b = boxes[j];
          if (
            Math.min(a.right, b.right) - Math.max(a.x, b.x) > 1 &&
            Math.min(a.bottom, b.bottom) - Math.max(a.y, b.y) > 1
          ) {
            overlaps.push(`${a.text.slice(0, 40)} <> ${b.text.slice(0, 40)}`);
          }
        }
      }
      if (overlaps.length) problems.push(`text collisions: ${JSON.stringify(overlaps.slice(0, 5))}`);

      let maxDx = 0;
      let maxDy = 0;
      if (reference.length !== boxes.length) {
        problems.push(`text count ${boxes.length} does not match C5 SVG ${reference.length}`);
      } else {
        const order = reference.map((item, index) => item.text === boxes[index].text);
        const firstBad = order.indexOf(false);
        if (firstBad !== -1) {
          problems.push(
            `text sequence diverges at index ${firstBad}: ` +
            `${JSON.stringify(reference[firstBad].text)} vs ${JSON.stringify(boxes[firstBad].text)}`,
          );
        } else {
          for (let i = 0; i < reference.length; i += 1) {
            maxDx = Math.max(maxDx, Math.abs((reference[i].x - reference[0].x) - (boxes[i].x - boxes[0].x)));
            maxDy = Math.max(maxDy, Math.abs((reference[i].y - reference[0].y) - (boxes[i].y - boxes[0].y)));
          }
          if (maxDy > MAX_DY) problems.push(`vertical divergence ${maxDy.toFixed(2)} exceeds ${MAX_DY}`);
          if (maxDx > MAX_DX) problems.push(`horizontal divergence ${maxDx.toFixed(2)} exceeds ${MAX_DX}`);
        }
      }

      if (pageErrors.length) problems.push(`page errors: ${JSON.stringify(pageErrors.slice(0, 3))}`);

      if (problems.length) {
        failures.push(`${name}: ${problems.join(' | ')}`);
        console.log(`official MCL v2.1 Excalidraw: FAIL ${name} — ${problems.join(' | ')}`);
      } else {
        console.log(
          `official MCL v2.1 Excalidraw: PASS ${name} ` +
          `elements=${rendered.elementCount} texts=${boxes.length} ` +
          `maxDx=${maxDx.toFixed(2)} maxDy=${maxDy.toFixed(2)}`,
        );
      }
    }
  } finally {
    await browser.close();
  }
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}

if (failures.length) {
  console.error('OFFICIAL_EXCALIDRAW_RENDER_NOT_VERIFIED');
  for (const failure of failures) console.error(`  ${failure}`);
  process.exit(1);
}
console.log(
  `official MCL v2.1 Excalidraw: all four scenes verified ` +
  `(@excalidraw/excalidraw ${excalidrawVersion}, tolerance dy<=${MAX_DY} dx<=${MAX_DX})`,
);
