import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
for (const w of [1200,901,900,600,375]) {
  const p = await b.newPage({ viewport:{width:w,height:900} });
  await p.goto('file:///home/claude/mcl-v2.1-draft-c5.html', {waitUntil:'load'});
  const r = await p.evaluate(()=>{
    const sb=document.querySelector('.gl-sidebar'), ly=document.querySelector('.gl-layout');
    const cs=sb?getComputedStyle(sb):null;
    return {ov: document.documentElement.scrollWidth-document.documentElement.clientWidth,
            sbw: sb?Math.round(sb.getBoundingClientRect().width):null,
            sbtop: cs?cs.top:null, pos: cs?cs.position:null,
            grid: ly?getComputedStyle(ly).gridTemplateColumns:null};
  });
  console.log(w+'px  overflow='+r.ov+'  sidebar='+r.sbw+'px  pos='+r.pos+'  top='+r.sbtop+'  grid='+r.grid);
  await p.close();
}
const p = await b.newPage({ viewport:{width:1200,height:900} });
await p.goto('file:///home/claude/mcl-v2.1-draft-c5.html', {waitUntil:'load'});
await p.emulateMedia({media:'print'});
const pr = await p.evaluate(()=>({nav:getComputedStyle(document.querySelector('.site-nav-shell')).display,
  sb:getComputedStyle(document.querySelector('.gl-sidebar')).display,
  banner:getComputedStyle(document.querySelector('.draft-banner')).display,
  foot:getComputedStyle(document.querySelector('.page-footer')).display}));
console.log('print: nav='+pr.nav+' sidebar='+pr.sb+' draftbanner='+pr.banner+' footer='+pr.foot);
await b.close();
