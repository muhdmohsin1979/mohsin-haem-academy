import { chromium } from 'playwright';
import fs from 'fs';
const axeSrc = fs.readFileSync('/home/claude/mcl/node_modules/axe-core/axe.min.js','utf8');
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const out = {};
for (const w of [1280, 375]) {
  const p = await b.newPage({viewport:{width:w,height:1000}});
  await p.goto('file:///home/claude/mcl-v2.1-draft-c5.html',{waitUntil:'load'});
  await p.addScriptTag({content: axeSrc});
  const r = await p.evaluate(async()=>{
    const x = await axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});
    return {
      v: x.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,
            help:v.help, targets:v.nodes.slice(0,4).map(n=>n.target.join(' ')), fail:v.nodes.slice(0,2).map(n=>n.failureSummary)})),
      passes: x.passes.length, incomplete: x.incomplete.map(i=>({id:i.id,n:i.nodes.length})),
      version: axe.version
    };
  });
  out[w] = r;
  await p.close();
}
await b.close();
fs.writeFileSync('/home/claude/mcl/axe-c4.json', JSON.stringify(out,null,1));
for (const [w,r] of Object.entries(out)) {
  console.log('=== '+w+'px  axe-core '+r.version+'  passes='+r.passes+' ===');
  if(!r.v.length) console.log('  VIOLATIONS: NONE');
  for (const v of r.v) console.log('  ['+v.impact+'] '+v.id+' x'+v.n+' — '+v.help+'\n     '+v.targets.join(' | '));
  console.log('  incomplete:', r.incomplete.map(i=>i.id+' x'+i.n).join(', ')||'none');
}
