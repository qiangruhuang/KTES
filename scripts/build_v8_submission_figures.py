#!/usr/bin/env python3
"""Build deterministic SVG submission figures for KTES v8.

Presentation only. Uses frozen numbers already reported in PAPER_IEEE_v8.md.
No outcomes are read and no statistical analysis is recomputed.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Arial, Helvetica, sans-serif"
DARK = "#111111"
MID = "#666666"
LIGHT = "#D9D9D9"
PALE = "#F3F3F3"
WHITE = "#FFFFFF"


def svg_start(w, h, title):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        '<desc id="desc">KTES v8 submission figure generated from frozen manuscript values.</desc>',
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{WHITE}"/>',
    ]


def text(x, y, s, size=22, weight="normal", anchor="start", fill=DARK):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{escape(str(s))}</text>'


def rect(x,y,w,h,fill=WHITE,stroke=DARK,sw=2,rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1,y1,x2,y2,stroke=DARK,sw=2,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def arrow(x1,y1,x2,y2):
    parts=[line(x1,y1,x2,y2,DARK,2)]
    if x2>=x1:
        pts=f"{x2},{y2} {x2-10},{y2-6} {x2-10},{y2+6}"
    else:
        pts=f"{x2},{y2} {x2+10},{y2-6} {x2+10},{y2+6}"
    parts.append(f'<polygon points="{pts}" fill="{DARK}"/>')
    return parts


def write(name, parts):
    parts.append('</svg>')
    p=OUT/name
    p.write_text('\n'.join(parts), encoding='utf-8')
    return p

p=svg_start(1800,950,"c-pKTES-Hedge method architecture")
p += [text(80,70,"Fig. 1. Probability-preserving active test allocation",34,"bold")]
boxes=[
    (70,170,260,170,"Finite operational population","Outcome-blind covariates\n+ operational weights"),
    (400,120,270,150,"3 certainty sentinels","Outcome-blind\nπ = 1"),
    (400,330,270,190,"37-unit remainder","positive π\n80% kernel novelty\n20% adverse-tail"),
    (760,220,280,190,"Local Cube","fixed stratum allocation\nspreading + balance"),
    (1130,220,280,190,"Hájek MA estimator","stratum-wise residual\ncorrection"),
    (1490,160,240,150,"Frozen UQ","max(GS, PWR)\nR3 calibration"),
    (1490,390,240,150,"Decision","Accept / Reject /\nInconclusive"),
]
for x,y,w,h,t,b in boxes:
    p.append(rect(x,y,w,h,PALE if 'certainty' in t.lower() or 'remainder' in t.lower() else WHITE))
    p.append(text(x+w/2,y+45,t,25,"bold","middle"))
    for j,l in enumerate(b.split('\n')):
        p.append(text(x+w/2,y+84+32*j,l,20,"normal","middle",MID))
p += arrow(330,255,400,195)
p += arrow(330,255,400,420)
p += arrow(670,195,760,275)
p += arrow(670,420,760,345)
p += arrow(1040,315,1130,315)
p += arrow(1410,290,1490,235)
p += arrow(1410,340,1490,465)
p.append(rect(120,650,1560,180,WHITE,DARK,2,4))
p.append(text(150,700,"Frozen design contract",25,"bold"))
params=["n = 40","3 + 37 architecture","ρ = 0.20","λ = 3","positive-π floor","immutable realized design object"]
xs=[170,410,720,910,1120,1390]
for x,s in zip(xs,params):
    p.append(text(x,770,s,21,"bold","middle"))
p.append(text(900,890,"Outcome values do not enter sentinel, novelty, tail-score, stratum-allocation, or inclusion-probability construction.",20,"normal","middle",MID))
write("FIG1_METHOD_ARCHITECTURE_v8.svg",p)

p=svg_start(1800,1100,"R5 independent controlled confirmation")
p += [text(70,65,"Fig. 2. R5 independent confirmation: preserve discovery, improve inference",34,"bold")]
p.append(text(80,125,"A. Discovery and decision behavior",26,"bold"))
rows=[
    ("Edge hit",0.812,0.779,"+0.033  [−0.0013, +0.0673]"),
    ("Definitive correct",0.173,0.089,"+0.084  [+0.0555, +0.1125]"),
    ("Abstain",0.826,0.911,"−0.085  [−0.1135, −0.0565]"),
]
x0,x1=410,1160
for i,(lab,a,b,ci) in enumerate(rows):
    y=195+i*110
    p.append(text(90,y+7,lab,22,"bold"))
    p.append(line(x0,y,x1,y,LIGHT,8))
    for val,label,dy in [(b,"Split15",-15),(a,"c-pKTES",18)]:
        x=x0+(x1-x0)*val
        p.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{DARK if label=="c-pKTES" else WHITE}" stroke="{DARK}" stroke-width="3"/>')
        p.append(text(x,y+dy,label,17,"normal","middle",MID))
    p.append(text(1210,y+5,ci,20,"normal"))
p.append(text(410,515,"0",18,"normal","middle",MID)); p.append(text(1160,515,"1",18,"normal","middle",MID))
p.append(text(785,545,"Proportion",19,"normal","middle",MID))
p.append(text(80,625,"B. Inferential error (lower is better)",26,"bold"))
errs=[
    ("Profile MAE",0.006824,0.008348,"−0.001525  [−0.002025, −0.001024]",0.010),
    ("Failure MAE",0.051746,0.060399,"−0.008653  [−0.012595, −0.004711]",0.070),
    ("Critical-tail MAE",0.016811,0.020958,"−0.004147  [−0.004798, −0.003497]",0.025),
]
for i,(lab,a,b,ci,mx) in enumerate(errs):
    y=700+i*105
    p.append(text(90,y+7,lab,22,"bold"))
    p.append(line(x0,y,x1,y,LIGHT,8))
    for val,label,dy in [(b,"Split15",-15),(a,"c-pKTES",18)]:
        x=x0+(x1-x0)*(val/mx)
        p.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{DARK if label=="c-pKTES" else WHITE}" stroke="{DARK}" stroke-width="3"/>')
        p.append(text(x,y+dy,label,17,"normal","middle",MID))
    p.append(text(1210,y+5,ci,20,"normal"))
p.append(text(900,1045,"Edge-hit superiority is not claimed because its paired CI crosses zero.",21,"bold","middle"))
write("FIG2_R5_CONFIRMATION_v8.svg",p)

p=svg_start(1900,1050,"Layered external validation")
p += [text(70,65,"Fig. 3. External validation is layered: numerical performance is only one gate",34,"bold")]
headers=["Dataset","Source gate","Frozen design","Numerical comparison","Validity boundary","Final evidence class"]
xs=[70,300,560,820,1170,1480]
ws=[210,240,240,330,280,340]
for x,w,h in zip(xs,ws,headers):
    p.append(rect(x,120,w,80,PALE,DARK,2,2)); p.append(text(x+w/2,170,h,20,"bold","middle"))
rows=[
    ("Anti-UAV410","PASS","PASS","Profile Δ vs SRS +0.00404\n95% CI [0.00137, 0.00671]\ninside +0.01 NI bound;\ncritical-domain error lower","Split15/domain estimator\nneeded execution clarification","PASS_WITH_EXECUTION_\nCLARIFICATION"),
    ("IDF-DS","STOP","NOT RUN","No method-performance result","Flight-level preoutcome\nframe not recoverable","BLOCKED_\nSOURCE_STRUCTURE"),
    ("AMOVFLY","PASS","PASS","Profile Δ vs SRS −0.0007586\n95% CI [−0.0011638, −0.0003534]\nall frozen numerical gates pass","Exact (0,0) waypoint\nplaceholders contaminate endpoint","NUMERICAL\nCONFIRMATORY PASS WITH\nENDPOINT-SEMANTIC\nLIMITATION"),
]
for r,row in enumerate(rows):
    y=230+r*245
    for c,(x,w) in enumerate(zip(xs,ws)):
        fill=PALE if c in [0,5] else WHITE
        p.append(rect(x,y,w,210,fill,DARK,2,2))
        val=row[c]
        for j,l in enumerate(val.split('\n')):
            p.append(text(x+w/2,y+55+j*34,l,19,"bold" if c in [0,5] else "normal","middle",DARK if c in [0,5] else MID))
p.append(text(950,1000,"Same frozen method; different evidence classes because source, execution and endpoint validity are assessed separately.",21,"bold","middle"))
write("FIG3_EXTERNAL_EVIDENCE_v8.svg",p)

p=svg_start(1900,1000,"Validity gates and provenance")
p += [text(70,65,"Fig. 4. Engineering evidence is a gated chain, not a single accuracy number",34,"bold")]
gates=[
    ("1","Preoutcome\nsource structure"),
    ("2","Frozen design\nidentity"),
    ("3","Endpoint\nsemantics"),
    ("4","Realized-design\nprovenance"),
    ("5","Numerical\nperformance + UQ"),
    ("6","Claim\nclassification"),
]
start=80; gap=300; y=210
for i,(n,lbl) in enumerate(gates):
    x=start+i*gap
    p.append(rect(x,y,230,150,WHITE,DARK,3,8))
    p.append(text(x+30,y+42,n,28,"bold"))
    for j,l in enumerate(lbl.split('\n')):
        p.append(text(x+115,y+80+j*32,l,21,"bold","middle"))
    if i < len(gates)-1:
        p += arrow(x+230,y+75,x+gap,y+75)
cases=[
    ("IDF-DS",1,"STOP: public release cannot instantiate the frozen flight-level preoutcome frame"),
    ("Anti-UAV410",6,"PASS WITH EXECUTION CLARIFICATION"),
    ("AMOVFLY",3,"Numerical gate passes later, but endpoint semantics limit the engineering claim"),
    ("Hosted-runner replay",4,"254/257 first-order inclusion probabilities drift > 1e−12; immutable design object required"),
]
ys=[500,610,720,830]
for (name,stop,msg),yy in zip(cases,ys):
    p.append(text(90,yy,name,22,"bold"))
    x_end=start+(stop-1)*gap+115
    p.append(line(300,yy-7,x_end,yy-7,DARK,4))
    p.append(f'<circle cx="{x_end}" cy="{yy-7}" r="10" fill="{DARK}"/>')
    p.append(text(x_end+30,yy,msg,19,"normal","start",MID))
p.append(text(950,955,"A favorable numerical comparison is necessary but not sufficient for an unrestricted engineering-validity claim.",21,"bold","middle"))
write("FIG4_VALIDITY_GATES_v8.svg",p)
