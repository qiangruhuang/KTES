#!/usr/bin/env python3
"""Recover Anti-UAV410 existence flags and reconcile them with pinned official boxes.

The large public ZIP mirror supplies per-frame `exist` flags that are absent from the
GitHub repository. The pinned official repository supplies the current test bounding
boxes. We accept the reconciliation only when: (1) all 120 names and frame counts
match; (2) every mirror-absent frame is also zero-boxed in the official annotation;
and (3) every visible frame for which both sources contain a nonzero box has identical
coordinates. The derived IR_label.json then uses official boxes + recovered existence.
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

def row_close(x,y,tol=1e-9):
    return len(x)==len(y)==4 and all(abs(float(u)-float(v))<=tol for u,v in zip(x,y))
def rows_close(a,b,tol=1e-9):
    return len(a)==len(b) and all(row_close(x,y,tol) for x,y in zip(a,b))
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def zero_box(x): return len(x)==4 and all(abs(float(v))<1e-12 for v in x)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--zip-url',required=True); ap.add_argument('--official-repo',type=Path,required=True); ap.add_argument('--frame-csv',type=Path,required=True); ap.add_argument('--out-root',type=Path,required=True); ap.add_argument('--manifest',type=Path,required=True); a=ap.parse_args()
    expected=[r['sequence_name'] for r in csv.DictReader(a.frame_csv.open(encoding='utf-8'))]
    if len(expected)!=120 or len(set(expected))!=120: raise SystemExit('frozen frame must contain 120 unique names')
    a.out_root.mkdir(parents=True,exist_ok=True)
    records=[]; mismatch_details=[]; total=mirror_zero=official_zero=absent=0
    zero_but_exist=nonzero_but_absent=0; absent_official_nonzero=0
    visible_both_nonzero_coord_mismatch=0; visible_mirror_zero_official_nonzero=0; visible_mirror_nonzero_official_zero=0
    with RemoteZip(a.zip_url) as rz:
        names=rz.namelist(); label_names=[n for n in names if n.replace('\\','/').endswith('/IR_label.json')]
        by_seq={}
        for n in label_names:
            parts=n.replace('\\','/').split('/')
            if len(parts)>=2: by_seq.setdefault(parts[-2],[]).append(n)
        for seq in expected:
            candidates=by_seq.get(seq,[])
            test=[n for n in candidates if '/test/' in ('/'+n.replace('\\','/').lower()+'/')]
            chosen=(test or candidates)
            if len(chosen)!=1: raise SystemExit(f'{seq}: label candidates={chosen}')
            raw=rz.read(chosen[0]); mirror=json.loads(raw.decode('utf-8')); gt=mirror['gt_rect']; ex=mirror['exist']
            official=num_rows(a.official_repo/'annos/test'/(seq+'.txt'))
            if len(ex)!=len(gt) or len(official)!=len(gt): raise SystemExit(f'{seq}: frame-count mismatch')
            seq_stats={'sequence_name':seq,'zip_member':chosen[0],'mirror_sha256':sha256_bytes(raw),'frames':len(gt),'mirror_raw_gt_equals_official':rows_close(gt,official),'absent_official_nonzero':0,'visible_both_nonzero_coord_mismatch':0,'visible_mirror_zero_official_nonzero':0,'visible_mirror_nonzero_official_zero':0}
            for idx,(g,e,o) in enumerate(zip(gt,ex,official),start=1):
                e=bool(e); zg=zero_box(g); zo=zero_box(o); total+=1; mirror_zero+=int(zg); official_zero+=int(zo); absent+=int(not e)
                zero_but_exist+=int(zg and e); nonzero_but_absent+=int((not zg) and (not e))
                category=None
                if (not e) and (not zo):
                    absent_official_nonzero+=1; seq_stats['absent_official_nonzero']+=1; category='absent_official_nonzero'
                elif e and (not zg) and (not zo) and not row_close(g,o):
                    visible_both_nonzero_coord_mismatch+=1; seq_stats['visible_both_nonzero_coord_mismatch']+=1; category='visible_both_nonzero_coord_mismatch'
                elif e and zg and (not zo):
                    visible_mirror_zero_official_nonzero+=1; seq_stats['visible_mirror_zero_official_nonzero']+=1; category='visible_mirror_zero_official_nonzero'
                elif e and (not zg) and zo:
                    visible_mirror_nonzero_official_zero+=1; seq_stats['visible_mirror_nonzero_official_zero']+=1; category='visible_mirror_nonzero_official_zero'
                if category:
                    mismatch_details.append({'sequence_name':seq,'frame_1based':idx,'category':category,'exist':e,'mirror_gt':g,'official_gt':o})
            # Hybrid label: current pinned official boxes are authoritative for localization;
            # recovered ZIP supplies only target-existence state needed by official SA semantics.
            hybrid=dict(mirror); hybrid['gt_rect']=official; hybrid['exist']=[bool(x) for x in ex]
            dest=a.out_root/'test'/seq/'IR_label.json'; dest.parent.mkdir(parents=True,exist_ok=True)
            hybrid_bytes=(json.dumps(hybrid,separators=(',',':'))+'\n').encode('utf-8'); dest.write_bytes(hybrid_bytes)
            seq_stats['hybrid_sha256']=sha256_bytes(hybrid_bytes); records.append(seq_stats)
    gate=(absent_official_nonzero==0 and visible_both_nonzero_coord_mismatch==0)
    manifest={'schema_version':'KTES-P2A-IRLABEL-RECONCILIATION-v8.3','zip_url':a.zip_url,'official_repository':'HwangBo94/Anti-UAV410','official_commit':'8a8eb04d976e9386b7c9c3ada5c85e5086013d52','population_n':len(records),'total_frames':total,'mirror_zero_gt_frames':mirror_zero,'official_zero_gt_frames':official_zero,'exist_false_frames':absent,'zero_but_exist_frames':zero_but_exist,'nonzero_but_absent_frames':nonzero_but_absent,'absent_official_nonzero_frames':absent_official_nonzero,'visible_both_nonzero_coordinate_mismatches':visible_both_nonzero_coord_mismatch,'visible_mirror_zero_official_nonzero_frames':visible_mirror_zero_official_nonzero,'visible_mirror_nonzero_official_zero_frames':visible_mirror_nonzero_official_zero,'reconciliation_gate_pass':gate,'hybrid_rule':'gt_rect = pinned official annos/test box; exist = recovered public-ZIP IR_label exist flag','mismatch_details':mismatch_details,'records':records}
    a.manifest.parent.mkdir(parents=True,exist_ok=True); a.manifest.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    keys=['population_n','total_frames','mirror_zero_gt_frames','official_zero_gt_frames','exist_false_frames','zero_but_exist_frames','nonzero_but_absent_frames','absent_official_nonzero_frames','visible_both_nonzero_coordinate_mismatches','visible_mirror_zero_official_nonzero_frames','visible_mirror_nonzero_official_zero_frames','reconciliation_gate_pass']
    print(json.dumps({k:manifest[k] for k in keys},indent=2))
    if not gate: raise SystemExit('recovered existence flags fail reconciliation with pinned official boxes')
if __name__=='__main__': main()
