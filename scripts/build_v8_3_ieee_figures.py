#!/usr/bin/env python3
"""Build IEEE-width-optimized SVG vector masters for KTES v8.3.

Presentation-only transformation of frozen v8.2 evidence. No outcomes are read,
no statistics are recomputed, and no evidence class is changed.
The graphics intentionally omit figure numbers/titles; captions live in manuscript.
Final IEEE submission export should be PDF/EPS from these vector masters.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Arial, Helvetica, sans-serif"
DARK = "#111111"; MID = "#555555"; LIGHT = "#D8D8D8"; PALE = "#F4F4F4"; WHITE = "#FFFFFF"

# At IEEE two-column width (7.16 in = 515.52 pt), 34 SVG units in a
# 1900-unit viewBox reproduce at ~9.22 pt. All informational text >=34.
def start(w,h,title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(desc)}</desc>',
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{WHITE}"/>']
def txt(x,y,s,size=34,weight="normal",anchor="start",fill=DARK):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{escape(str(s))}</text>'
def box(x,y,w,h,fill=WHITE,stroke=DARK,sw=3,rx=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,stroke=DARK,sw=3,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def arrow(x1,y1,x2,y2):
    out=[line(x1,y1,x2,y2,DARK,4)]
    if abs(x2-x1)>=abs(y2-y1):
        pts=f"{x2},{y2} {x2-16 if x2>=x1 else x2+16},{y2-10} {x2-16 if x2>=x1 else x2+16},{y2+10}"
    else:
        pts=f"{x2},{y2} {x2-10},{y2-16 if y2>=y1 else y2+16} {x2+10},{y2-16 if y2>=y1 else y2+16}"
    return out+[f'<polygon points="{pts}" fill="{DARK}"/>']
def multi(parts,x,y,lines,size=34,weight="normal",anchor="middle",fill=DARK,gap=42):
    for j,s in enumerate(lines): parts.append(txt(x,y+j*gap,s,size,weight,anchor,fill))
def write(name,parts):
    parts.append('</svg>'); p=OUT/name; p.write_text('\n'.join(parts)+'\n',encoding='utf-8'); return p

# Fig 1
p=start(1900,790,"Frozen c-pKTES-Hedge architecture","Forty-test probability-preserving active allocation architecture.")
p.append(box(45,80,295,230,PALE)); multi(p,192,145,["Finite operational","frame"],38,"bold"); multi(p,192,235,["preoutcome","covariates + weights"],34,fill=MID,gap=42)
p.append(box(405,30,390,180,PALE)); multi(p,600,95,["3 certainty sentinels","π = 1"],38,"bold"); p.append(txt(600,180,"outcome-blind",34,"normal","middle",MID))
p.append(box(405,255,390,230,PALE)); multi(p,600,320,["37-unit probability","remainder"],38,"bold"); multi(p,600,420,["positive π","80% novelty + 20% tail"],34,fill=MID)
p += arrow(340,190,405,120); p += arrow(340,205,405,370)
p.append(box(885,155,300,210)); multi(p,1035,220,["Local Cube","selection"],40,"bold"); multi(p,1035,310,["fixed strata","spread + balance"],34,fill=MID)
p += arrow(795,120,885,215); p += arrow(795,370,885,310)
p.append(box(1275,30,570,180)); multi(p,1560,95,["Hájek model-assisted","residual correction"],38,"bold"); p.append(txt(1560,180,"finite-population inference",34,"normal","middle",MID))
p.append(box(1275,255,570,180)); multi(p,1560,320,["Frozen UQ +","3-state decision"],38,"bold"); p.append(txt(1560,405,"Accept / Reject / Inconclusive",34,"normal","middle",MID))
p += arrow(1185,220,1275,120); p += arrow(1185,300,1275,345)
# parameter matrix 3 columns x 2 rows
p.append(box(80,555,1740,160,WHITE,DARK,3,6))
for x,s in [(365,"n = 40"),(950,"3 + 37"),(1535,"ρ = 0.20")]: p.append(txt(x,615,s,34,"bold","middle"))
for x,s in [(365,"λ = 3"),(950,"positive-π floor"),(1535,"hashed realized design")]: p.append(txt(x,675,s,34,"bold","middle"))
p.append(txt(950,765,"Outcome values never enter selection-design construction.",34,"bold","middle"))
write("FIG1_METHOD_ARCHITECTURE_v8_3.svg",p)

# Fig 2
p=start(1900,930,"R5 independent confirmation","Paired differences with 95 percent confidence intervals.")
p.append(txt(70,65,"Paired difference: c-pKTES-Hedge − Split15",36,"normal",fill=MID))
def ci_panel(parts,y0,title,rows,xmin,xmax,xleft=620,xright=1720):
    parts.append(txt(80,y0,title,40,"bold")); zero=xleft+(0-xmin)/(xmax-xmin)*(xright-xleft)
    parts.append(line(zero,y0+35,zero,y0+285,MID,3,"10,10"))
    for i,(lab,est,lo,hi) in enumerate(rows):
        y=y0+85+i*85; parts.append(txt(90,y+10,lab,34,"bold")); X=lambda v:xleft+(v-xmin)/(xmax-xmin)*(xright-xleft)
        parts.append(line(X(lo),y,X(hi),y,DARK,6)); parts.append(line(X(lo),y-12,X(lo),y+12,DARK,4)); parts.append(line(X(hi),y-12,X(hi),y+12,DARK,4))
        parts.append(f'<circle cx="{X(est)}" cy="{y}" r="12" fill="{DARK}"/>'); parts.append(txt(1770,y+10,f"{est:+.4f}",34,"bold","end"))
    parts.append(txt(zero,y0+315,"0",34,"normal","middle",MID))
ci_panel(p,125,"A. Discovery / decision",[("Edge hit",0.033,-0.0013,0.0673),("Definitive correct",0.084,0.0555,0.1125),("Abstain",-0.085,-0.1135,-0.0565)],-0.13,0.13)
ci_panel(p,495,"B. Inferential error (negative is better)",[("Profile MAE",-0.001525,-0.002025,-0.001024),("Failure MAE",-0.008653,-0.012595,-0.004711),("Critical-tail MAE",-0.004147,-0.004798,-0.003497)],-0.014,0.003)
p.append(txt(950,900,"Edge-hit CI crosses zero: no superiority claim.",36,"bold","middle"))
write("FIG2_R5_CONFIRMATION_v8_3.svg",p)

# Fig 3
p=start(1900,900,"Layered external evidence","Three external datasets terminate at different evidence classes under one frozen method.")
for x in [55,665,1275]: p.append(box(x,45,570,760,WHITE,DARK,3,12))
p.append(txt(340,110,"Anti-UAV410",42,"bold","middle")); p.append(txt(340,165,"Source gate: PASS",34,"bold","middle"))
multi(p,340,245,["Profile Δ vs SRS","+0.00404","95% CI [0.00137, 0.00671]"],34,fill=MID,gap=45)
multi(p,340,410,["Inside frozen +0.01","non-inferiority bound","critical-domain error lower"],34,fill=MID,gap=45)
multi(p,340,610,["PASS_WITH_EXECUTION_","CLARIFICATION"],34,"bold",gap=48)
p.append(txt(950,110,"IDF-DS",42,"bold","middle")); p.append(txt(950,165,"Source gate: STOP",34,"bold","middle"))
multi(p,950,260,["Required flight-level","preoutcome frame","not recoverable"],34,fill=MID,gap=48)
multi(p,950,455,["No outcome opening","No method-performance result"],34,fill=MID,gap=48)
multi(p,950,610,["BLOCKED_","SOURCE_STRUCTURE"],34,"bold",gap=48)
p.append(txt(1560,110,"AMOVFLY",42,"bold","middle")); p.append(txt(1560,165,"Source gate: PASS",34,"bold","middle"))
multi(p,1560,235,["Profile Δ vs SRS","−0.0007586","95% CI [−0.0011638,","−0.0003534]"],34,fill=MID,gap=43)
multi(p,1560,425,["Numerical gates pass","but exact (0,0) placeholders","contaminate literal endpoint"],34,fill=MID,gap=43)
multi(p,1560,610,["NUMERICAL CONFIRMATORY","PASS WITH ENDPOINT-","SEMANTIC LIMITATION"],34,"bold",gap=45)
p.append(txt(950,860,"Same frozen method; source, execution, and endpoint validity determine evidence strength.",34,"bold","middle"))
write("FIG3_EXTERNAL_EVIDENCE_v8_3.svg",p)

# Fig 4
p=start(1900,760,"Validity gates","Engineering evidence is assigned only after source, design, endpoint, provenance, and numerical gates.")
labels=[("1","Source\nstructure"),("2","Frozen design\nidentity"),("3","Endpoint\nsemantics"),("4","Realized-design\nprovenance"),("5","Numerical\nperformance + UQ"),("6","Claim\nclassification")]
x0=45; gap=305; y=50
for i,(n,lbl) in enumerate(labels):
    x=x0+i*gap; p.append(box(x,y,250,180)); p.append(txt(x+30,y+50,n,40,"bold")); multi(p,x+125,y+105,lbl.split('\n'),34,"bold",gap=42)
    if i<5: p += arrow(x+250,y+90,x+gap,y+90)
lanes=[("IDF-DS",1,"STOP: source structure"),("AMOVFLY",3,"endpoint-semantic limitation"),("Hosted replay",4,"immutable realized design required"),("Anti-UAV410",6,"PASS with execution clarification")]
for j,(name,gate,msg) in enumerate(lanes):
    yy=330+j*88; p.append(txt(55,yy,name,34,"bold")); end=x0+(gate-1)*gap+125; p.append(line(320,yy-10,end,yy-10,DARK,5)); p.append(f'<circle cx="{end}" cy="{yy-10}" r="11" fill="{DARK}"/>')
    if gate==6: p.append(txt(end-25,yy+42,msg,34,"normal","end",MID))
    else: p.append(txt(end+28,yy,msg,34,"normal",fill=MID))
p.append(txt(950,735,"Numerical success is necessary but not sufficient for an unrestricted engineering claim.",34,"bold","middle"))
write("FIG4_VALIDITY_GATES_v8_3.svg",p)
print('wrote 4 IEEE-optimized SVG vector masters to', OUT)
