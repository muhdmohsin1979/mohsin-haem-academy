import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p = await b.newPage({viewport:{width:1280,height:1000}});
await p.goto('file:///home/claude/mcl-v2.1-draft-c5.html',{waitUntil:'load'});
const r = await p.evaluate(()=>{
  const parse=s=>{const m=s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)/);return m?[+m[1],+m[2],+m[3]]:null;};
  const lum=c=>{const v=c.map(x=>{x/=255;return x<=0.03928?x/12.92:Math.pow((x+0.055)/1.055,2.4)});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
  const ratio=(a,b)=>{const [l1,l2]=[lum(a),lum(b)].sort((x,y)=>y-x);return (l1+.05)/(l2+.05)};
  const out={};
  for(const a of document.querySelectorAll('a')){
    const par=a.parentElement;
    // only links sitting inside a text block with sibling text
    let sib=''; for(const n of par.childNodes) if(n.nodeType===3) sib+=n.nodeValue.trim();
    if(!sib) continue;
    const cs=getComputedStyle(a), ps=getComputedStyle(par);
    const dec=cs.textDecorationLine;
    const rr=ratio(parse(cs.color),parse(ps.color)).toFixed(2);
    const key=dec+' | linkcolor '+cs.color+' vs text '+ps.color+' = '+rr+':1';
    out[key]=(out[key]||0)+1;
  }
  return out;
});
console.log(JSON.stringify(r,null,1));
await b.close();
