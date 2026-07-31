import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p = await b.newPage({viewport:{width:1280,height:1000}});
const msgs=[]; p.on('console',m=>{if(m.type()==='error')msgs.push(m.text());});
p.on('pageerror',e=>msgs.push('PAGEERROR '+e.message));
await p.goto('file:///home/claude/mcl-v2.1-draft-c5.html',{waitUntil:'load'});
await p.waitForTimeout(600);
console.log('console errors:', msgs.length?msgs:'NONE');
// contrast maths for the two changed tokens
const lum=c=>{const v=c.map(x=>{x/=255;return x<=0.03928?x/12.92:Math.pow((x+0.055)/1.055,2.4)});return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]};
const ratio=(a,b)=>{const [l1,l2]=[lum(a),lum(b)].sort((x,y)=>y-x);return ((l1+0.05)/(l2+0.05)).toFixed(2)};
console.log('tier C  #241a05 on #d8a441 :', ratio([36,26,5],[216,164,65]));
console.log('focus   #1B2A4A on white   :', ratio([27,42,74],[255,255,255]));
console.log('focus   #1B2A4A on #F7F8FA :', ratio([27,42,74],[247,248,250]));
await b.close();
