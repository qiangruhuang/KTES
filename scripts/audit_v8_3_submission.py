#!/usr/bin/env python3
"""Fail-closed structural audit for the KTES v8.3 submission layer."""
from pathlib import Path
import re, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
MAIN=ROOT/'paper'/'PAPER_IEEE_v8_3.md'
SUPP=ROOT/'paper'/'SUPPLEMENTARY_INFORMATION_v8_3.md'
BIB=ROOT/'paper'/'references_v8_3.bib'
FIGROOT=ROOT/'paper'/'figures'

main=MAIN.read_text(encoding='utf-8')
supp=SUPP.read_text(encoding='utf-8')
bib=BIB.read_text(encoding='utf-8')
fig3=(FIGROOT/'FIG3_EXTERNAL_EVIDENCE_v8_3.svg').read_text(encoding='utf-8')
checks=[]
def ck(name,cond,detail=''):
    checks.append((name,bool(cond),detail))

ck('main_has_4_v8_3_figures',len(re.findall(r'figures/FIG[1-4]_[A-Z0-9_]*v8_3\.svg',main))==4)
ck('no_old_v8_figure_paths',all(x not in main for x in ['FIG1_METHOD_ARCHITECTURE_v8.svg','FIG2_R5_CONFIRMATION_v8.svg','FIG3_EXTERNAL_EVIDENCE_v8.svg','FIG4_VALIDITY_GATES_v8.svg']))
ck('main_has_3_tables',len(re.findall(r'\*\*TABLE (?:I|II|III)\.',main))==3)
ck('supp_sections_S1_S10',re.findall(r'^## (S\d+)\.',supp,flags=re.M)==[f'S{i}' for i in range(1,11)])
ck('supp_tables_S1_S4',re.findall(r'\*\*TABLE (S\d+)\.',supp)==[f'S{i}' for i in range(1,5)])
labels=['PASS_WITH_EXECUTION_CLARIFICATION','BLOCKED_SOURCE_STRUCTURE','NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION']
for lab in labels:
    ck('main_label_'+lab,lab in main); ck('supp_label_'+lab,lab in supp)
ck('fig3_antiuav_class','PASS_WITH_EXECUTION_' in fig3 and 'CLARIFICATION' in fig3)
ck('fig3_idfds_class','BLOCKED_' in fig3 and 'SOURCE_STRUCTURE' in fig3)
ck('fig3_amovfly_class','NUMERICAL CONFIRMATORY' in fig3 and 'PASS WITH ENDPOINT-' in fig3 and 'SEMANTIC LIMITATION' in fig3)
for token in ['+0.00404','0.00137','0.00671','-0.0007586','-0.0011638','-0.0003534','81.2%','77.9%']:
    ck('main_token_'+token,token in main)
ck('main_r5_no_superiority','no edge-superiority claim' in main or 'not statistically significant superiority' in main)
ck('main_idfds_no_result','no method-performance result' in main)
ck('main_amovfly_placeholder','(0,0)' in main and 'placeholder' in main)
ck('main_realized_design','hashed realized design object' in main and 'immutable realized design object' in main)
for n in range(1,5):
    intro=main.find(f'Figure {n}'); cap=main.find(f'**Fig. {n}.**')
    ck(f'figure_{n}_introduced_before_caption',intro!=-1 and cap!=-1 and intro<cap,f'{intro}<{cap}')
for roman in ['I','II','III']:
    intro=main.find(f'Table {roman}'); cap=main.find(f'**TABLE {roman}.')
    ck(f'table_{roman}_introduced_before_caption',intro!=-1 and cap!=-1 and intro<cap,f'{intro}<{cap}')
for p in sorted(FIGROOT.glob('*_v8_3.svg')):
    ET.parse(p); t=p.read_text(encoding='utf-8'); W=float(re.search(r'width="([0-9.]+)"',t).group(1)); fs=[float(x) for x in re.findall(r'font-size="([0-9.]+)"',t)]
    rendered=min(fs)*515.52/W
    ck('font_'+p.stem,rendered>=9.0,f'{rendered:.2f} pt')
ck('main_17_references',len(re.findall(r'^\[\d+\]',main,flags=re.M))==17)
ck('bib_17_entries',len(re.findall(r'^@',bib,flags=re.M))==17)

fails=[c for c in checks if not c[1]]
for name,ok,detail in checks:
    print(('PASS' if ok else 'FAIL'),name,detail)
print(f'SUMMARY {len(checks)-len(fails)}/{len(checks)} PASS')
if fails:
    raise SystemExit(1)
