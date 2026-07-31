import re, io, xml.etree.ElementTree as ET

NS='{http://www.w3.org/2000/svg}'
def hx(c):
    c=c.strip()
    if c=='white': return (255,255,255)
    if c=='black': return (0,0,0)
    if c.startswith('#'):
        c=c[1:]
        if len(c)==3: c=''.join(x*2 for x in c)
        return tuple(int(c[i:i+2],16) for i in (0,2,4))
    return None

def lum(rgb):
    o=[]
    for v in rgb:
        v/=255.0
        o.append(v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4)
    return 0.2126*o[0]+0.7152*o[1]+0.0722*o[2]

def ratio(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True)
    return (l1+0.05)/(l2+0.05)

h=io.open('mcl-v2.1-draft-c5.html',encoding='utf-8').read()
svgs=re.findall(r'<svg\b.*?</svg>',h,re.S)
worst=[]; checked=0; unresolved=[]
for si,s in enumerate(svgs):
    root=ET.fromstring(s)
    rects=[]
    for r in root.iter(NS+'rect'):
        f=r.get('fill')
        if not f or f=='none': continue
        try:
            x=float(r.get('x',0)); y=float(r.get('y',0)); w=float(r.get('width',0)); hh=float(r.get('height',0))
        except (TypeError,ValueError): continue
        rects.append((x,y,w,hh,f))
    page=hx('#ffffff')
    for t in root.iter(NS+'text'):
        try:
            tx=float(t.get('x')); ty=float(t.get('y'))
        except (TypeError,ValueError): continue
        fill=t.get('fill') or '#000000'
        fg=hx(fill)
        if fg is None:
            unresolved.append((si,fill)); continue
        # smallest rect containing the text anchor point (baseline: probe slightly above)
        best=None; area=None
        for (x,y,w,hh,f) in rects:
            if x<=tx<=x+w and y<=ty<=y+hh:
                a=w*hh
                if area is None or a<area:
                    area=a; best=f
        bg=hx(best) if best else page
        if bg is None:
            unresolved.append((si,best)); continue
        fs=float(t.get('font-size',11))
        bold = t.get('font-weight') in ('700','bold')
        need = 3.0 if (fs>=18 or (fs>=14 and bold)) else 4.5
        r_=ratio(fg,bg); checked+=1
        if r_<need:
            worst.append((round(r_,2),need,fill,best or '#ffffff',fs,si,(t.text or '')[:60]))
worst.sort()
print('svg text nodes checked:', checked)
print('unresolved fills:', set(unresolved) if unresolved else 'none')
if not worst:
    print('SVG TEXT CONTRAST: all pass')
else:
    for w in worst: print('  FAIL %.2f (need %.1f) fg=%s bg=%s size=%s svg#%d  %r' % w)
