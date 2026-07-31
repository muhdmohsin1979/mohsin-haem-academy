import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
for (const w of [1280,375]) {
const p = await b.newPage({viewport:{width:w,height:1000}});
await p.goto('file:///home/claude/mcl-v2.1-draft-c5.html',{waitUntil:'load'});
const r = await p.evaluate(()=>{
  const parse=s=>{const m=s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null;};
  const lum=c=>{const v=c.slice(0,3).map(x=>{x/=255;return x<=0.03928?x/12.92:Math.pow((x+0.055)/1.055,2.4)});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
  const ratio=(a,b)=>{const [l1,l2]=[lum(a),lum(b)].sort((x,y)=>y-x);return (l1+.05)/(l2+.05)};
  const bgOf=el=>{let n=el;while(n&&n.nodeType===1){const c=parse(getComputedStyle(n).backgroundColor);if(c&&c[3]>0.99)return c;n=n.parentElement;}return [255,255,255,1];};
  const out=[],seen=new Set();
  for(const el of document.querySelectorAll('body *')){
    if(el.closest('svg'))continue;
    const cs=getComputedStyle(el);
    if(cs.display==='none'||cs.visibility==='hidden')continue;
    let txt='';for(const n of el.childNodes)if(n.nodeType===3)txt+=n.nodeValue.trim();
    if(!txt)continue;
    const fg=parse(cs.color); if(!fg)continue;
    const bg=bgOf(el);
    const fs=parseFloat(cs.fontSize), fw=parseInt(cs.fontWeight)||400;
    const large = fs>=24 || (fs>=18.66 && fw>=700);
    const need = large?3:4.5;
    const rr=ratio(fg,bg);
    const key=cs.color+'|'+bg.join(',')+'|'+need;
    if(seen.has(key))continue; seen.add(key);
    out.push({sel:el.tagName.toLowerCase()+(el.className&&typeof el.className==='string'?'.'+el.className.trim().split(/\s+/).join('.'):''),
              fg:cs.color,bg:'rgb('+bg.slice(0,3).join(',')+')',fs,fw,need,r:+rr.toFixed(2),pass:rr>=need,sample:txt.slice(0,40)});
  }
  return out;
});
const fails=r.filter(x=>!x.pass);
console.log('=== '+w+'px : '+r.length+' distinct colour pairs, '+fails.length+' failing ===');
for(const f of fails) console.log('  FAIL '+f.r+' (need '+f.need+') '+f.fg+' on '+f.bg+' '+f.fs+'px/'+f.fw+'  <'+f.sel+'> "'+f.sample+'"');
await p.close();
}
await b.close();
