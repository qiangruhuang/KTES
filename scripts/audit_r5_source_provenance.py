#!/usr/bin/env python3
"""Fail-closed provenance checker for the frozen Phase 1.2R-5 engine."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
REQUIRED=[
 'src/run_r5_pps_confirm.py',
 'src/run_r5_pps_confirm_chunk.py',
 'src/run_r5_uq_audit_chunk.py',
 'src/phase12r/r5_designs.py',
 'src/phase12r/r5_estimators.py',
]
def sha256(p:Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--output',type=Path); a=ap.parse_args()
    rows=[]; missing=[]
    for rel in REQUIRED:
        p=a.root/rel
        if not p.is_file(): missing.append(rel); continue
        rows.append({'path':rel,'size_bytes':p.stat().st_size,'sha256':sha256(p)})
    out={'schema_version':'KTES-R5-SOURCE-PROVENANCE-v8.1','required_files':REQUIRED,'files':rows,'missing':missing,'gate_pass':not missing}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(text,encoding='utf-8')
    print(text,end='')
    if missing: raise SystemExit(2)
if __name__=='__main__': main()
