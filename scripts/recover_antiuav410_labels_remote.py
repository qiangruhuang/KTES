#!/usr/bin/env python3
"""Range-read Anti-UAV410 IR_label.json files from a public ZIP mirror.

Provenance is accepted only when the recovered labels reproduce the official pinned
Anti-UAV410 annos/test files under the benchmark's visibility projection: a visible
frame retains gt_rect, while an absent frame maps to [0,0,0,0]. This is stricter and
more appropriate than requiring raw gt_rect equality on absent frames, where the JSON
may retain a nonzero box even though exist=false.
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
    records=[]; raw_gt_mismatch=[]; projected_mismatch=[]; total=mirror_zero=official_zero=absent=0
    zero_but_exist=nonzero_but_absent=0; projected_frame_mismatch=0; visible_nonzero_coord_mismatch=0
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
            raw=rz.read(chosen[0]); label=json.loads(raw.decode('utf-8')); gt=label['gt_rect']; ex=label['exist']
            official=num_rows(a.official_repo/'annos/test'/(seq+'.txt'))
            if len(ex)!=len(gt) or len(official)!=len(gt): raise SystemExit(f'{seq}: frame-count mismatch')
            raw_equal=rows_close(gt,official)
            if not raw_equal: raw_gt_mismatch.append(seq)
            seq_projected_mismatch=seq_zero_exist=seq_nonzero_absent=seq_visible_coord_mismatch=0
            for g,e,o in zip(gt,ex,official):
                e=bool(e); total+=1; mirror_zero+=int(zero_box(g)); official_zero+=int(zero_box(o)); absent+=int(not e)
                seq_zero_exist+=int(zero_box(g) and e); seq_nonzero_absent+=int((not zero_box(g)) and (not e))
                expected_o=g if e else [0.0,0.0,0.0,0.0]
                if not row_close(expected_o,o): seq_projected_mismatch+=1
                if e and (not zero_box(g)) and not row_close(g,o): seq_visible_coord_mismatch+=1
            zero_but_exist+=seq_zero_exist; nonzero_but_absent+=seq_nonzero_absent; projected_frame_mismatch+=seq_projected_mismatch; visible_nonzero_coord_mismatch+=seq_visible_coord_mismatch
            if seq_projected_mismatch: projected_mismatch.append(seq)
            dest=a.out_root/'test'/seq/'IR_label.json'; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw)
            records.append({'sequence_name':seq,'zip_member':chosen[0],'sha256':sha256_bytes(raw),'frames':len(gt),'raw_gt_equals_official':raw_equal,'visibility_projection_mismatches':seq_projected_mismatch,'zero_but_exist':seq_zero_exist,'nonzero_but_absent':seq_nonzero_absent})
    gate=(not projected_mismatch and projected_frame_mismatch==0 and visible_nonzero_coord_mismatch==0)
    manifest={'schema_version':'KTES-P2A-IRLABEL-RECOVERY-v8.2','zip_url':a.zip_url,'population_n':len(records),'raw_gt_rect_matches_official_120':not raw_gt_mismatch,'raw_gt_mismatch_sequence_count':len(raw_gt_mismatch),'official_box_equals_visibility_projection_120':gate,'visibility_projection_mismatch_sequences':projected_mismatch,'visibility_projection_frame_mismatches':projected_frame_mismatch,'visible_nonzero_coordinate_mismatches':visible_nonzero_coord_mismatch,'total_frames':total,'mirror_zero_gt_frames':mirror_zero,'official_zero_gt_frames':official_zero,'exist_false_frames':absent,'zero_but_exist_frames':zero_but_exist,'nonzero_but_absent_frames':nonzero_but_absent,'records':records}
    a.manifest.parent.mkdir(parents=True,exist_ok=True); a.manifest.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    keys=['population_n','raw_gt_rect_matches_official_120','raw_gt_mismatch_sequence_count','official_box_equals_visibility_projection_120','visibility_projection_frame_mismatches','visible_nonzero_coordinate_mismatches','total_frames','mirror_zero_gt_frames','official_zero_gt_frames','exist_false_frames','zero_but_exist_frames','nonzero_but_absent_frames']
    print(json.dumps({k:manifest[k] for k in keys},indent=2))
    if not gate: raise SystemExit('recovered labels fail official visibility-projection provenance audit')
if __name__=='__main__': main()
