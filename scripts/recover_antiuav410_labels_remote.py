#!/usr/bin/env python3
"""Range-read Anti-UAV410 IR_label.json files from a public ZIP mirror.

The recovered labels are accepted only when their gt_rect arrays agree exactly (within
numeric tolerance) with the official pinned Anti-UAV410 annos/test box files for all
120 frozen test sequences.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
from remotezip import RemoteZip


def num_rows(p:Path):
    out=[]
    for line in p.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if line: out.append([float(x) for x in line.replace(',',' ').split()])
    return out

def close_rows(a,b,tol=1e-9):
    return len(a)==len(b) and all(len(x)==len(y)==4 and all(abs(float(u)-float(v))<=tol for u,v in zip(x,y)) for x,y in zip(a,b))
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def zero_box(x): return len(x)==4 and all(abs(float(v))<1e-12 for v in x)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--zip-url',required=True); ap.add_argument('--official-repo',type=Path,required=True); ap.add_argument('--frame-csv',type=Path,required=True); ap.add_argument('--out-root',type=Path,required=True); ap.add_argument('--manifest',type=Path,required=True); a=ap.parse_args()
    expected=[r['sequence_name'] for r in csv.DictReader(a.frame_csv.open(encoding='utf-8'))]
    if len(expected)!=120 or len(set(expected))!=120: raise SystemExit('frozen frame must contain 120 unique names')
    a.out_root.mkdir(parents=True,exist_ok=True); records=[]; gt_mismatch=[]; existence_disagreements=[]; total=zero=absent=0
    with RemoteZip(a.zip_url) as rz:
        names=rz.namelist(); label_names=[n for n in names if n.replace('\\','/').endswith('/IR_label.json')]
        by_seq={}
        for n in label_names:
            parts=n.replace('\\','/').split('/')
            if len(parts)>=2: by_seq.setdefault(parts[-2],[]).append(n)
        for seq in expected:
            candidates=by_seq.get(seq,[])
            # Prefer entries whose path contains a test component.
            test=[n for n in candidates if '/test/' in ('/'+n.replace('\\','/').lower()+'/')]
            chosen=(test or candidates)
            if len(chosen)!=1: raise SystemExit(f'{seq}: label candidates={chosen}')
            raw=rz.read(chosen[0]); label=json.loads(raw.decode('utf-8')); gt=label['gt_rect']; ex=label['exist']
            official=num_rows(a.official_repo/'annos/test'/(seq+'.txt'))
            if not close_rows(gt,official): gt_mismatch.append(seq)
            if len(ex)!=len(gt): raise SystemExit(f'{seq}: exist/gt length mismatch')
            d10=d01=0
            for g,e in zip(gt,ex):
                z=zero_box(g); total+=1; zero+=int(z); absent+=int(not bool(e)); d10+=int(z and bool(e)); d01+=int((not z) and (not bool(e)))
            if d10 or d01: existence_disagreements.append({'sequence_name':seq,'zero_but_exist':d10,'nonzero_but_absent':d01})
            dest=a.out_root/'test'/seq/'IR_label.json'; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw)
            records.append({'sequence_name':seq,'zip_member':chosen[0],'sha256':sha256_bytes(raw),'frames':len(gt),'zero_but_exist':d10,'nonzero_but_absent':d01})
    manifest={'schema_version':'KTES-P2A-IRLABEL-RECOVERY-v8.1','zip_url':a.zip_url,'population_n':len(records),'gt_rect_matches_official_120':not gt_mismatch,'gt_mismatch_sequences':gt_mismatch,'total_frames':total,'zero_gt_frames':zero,'exist_false_frames':absent,'zero_gt_equivalent_to_exist_false':not existence_disagreements and zero==absent,'existence_disagreements':existence_disagreements,'records':records}
    a.manifest.parent.mkdir(parents=True,exist_ok=True); a.manifest.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['population_n','gt_rect_matches_official_120','total_frames','zero_gt_frames','exist_false_frames','zero_gt_equivalent_to_exist_false']},indent=2))
    if gt_mismatch: raise SystemExit('recovered labels fail official gt_rect provenance audit')
if __name__=='__main__': main()
