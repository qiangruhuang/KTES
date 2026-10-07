#!/usr/bin/env python3
"""AMOVFLY v8.2 outcome-blind path inventory.

Reads only the pinned Git tree (path/blob SHA/size). No Flight_info row and no
raw/ready flight CSV bytes are downloaded. Primary units are unique ready-data
blobs in the four autonomous scenarios; byte-identical aliases are collapsed.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,os,re
from collections import Counter,defaultdict
from pathlib import Path,PurePosixPath
import requests

REPO="YujiaoHu/AMOVFLY-Dataset"
COMMIT="67069ed00ddbebd62b71aa9bb1272415e9b15ff8"
TREE_SHA="4f847e7b901d1c66619371f57346fd6932f28025"
STRATA=("FAFS","FAVS","VAFS","VAVS")
READY_RE=re.compile(r"^Uav(?P<uav>[A-Za-z0-9]+)_(?P<cond>.+)_(?P<num>\d+)\.csv$",re.I)
COND_RE=re.compile(r"^P(?P<payload>\d+)(?P<avar>Var)?A(?P<alt>\d*)(?P<svar>Var)?S(?P<speed>\d+)$",re.I)

def h256(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def nu(x:str)->str:return re.sub(r"^uav","",x,flags=re.I).upper()

def tree():
    h={"Accept":"application/vnd.github+json"};t=os.getenv("GITHUB_TOKEN")
    if t:h["Authorization"]=f"Bearer {t}"
    r=requests.get(f"https://api.github.com/repos/{REPO}/git/trees/{TREE_SHA}?recursive=1",headers=h,timeout=60);r.raise_for_status();o=r.json()
    if o.get("truncated") or o.get("sha")!=TREE_SHA:raise RuntimeError("FAIL-CLOSED: source tree identity/truncation")
    return o["tree"]

def pc(x:str)->dict:
    m=COND_RE.fullmatch(x)
    if not m:return {"ok":False,"payload":None,"alt":None,"speed":None,"avar":None,"svar":None,"alt_avail":False}
    a=m.group("alt")
    return {"ok":True,"payload":float(m.group("payload")),"alt":float(a) if a else None,"speed":float(m.group("speed")),"avar":bool(m.group("avar")),"svar":bool(m.group("svar")),"alt_avail":bool(a)}

def completeness(r):
    p=r["p"];n=sum(p[k] is not None for k in ("payload","alt","speed"))
    return (int(p["ok"]),n,len(r["cond"]),r["path"])

def compatible(rs,c):
    cp=c["p"]
    for r in rs:
        p=r["p"]
        if (r["scenario"],r["uav"],r["num"])!=(c["scenario"],c["uav"],c["num"]):return False
        if p["ok"] and cp["ok"]:
            if p["payload"]!=cp["payload"] or p["speed"]!=cp["speed"]:return False
            if p["alt"] is not None and cp["alt"] is not None and p["alt"]!=cp["alt"]:return False
            if p["avar"]!=cp["avar"] or p["svar"]!=cp["svar"]:return False
    return True

def alloc(counts):
    base={s:2 for s in STRATA};rem=40-sum(base.values());res={s:max(0,counts[s]-2) for s in STRATA};den=sum(res.values())
    q={s:rem*res[s]/den for s in STRATA};ex={s:int(math.floor(q[s])) for s in STRATA};left=rem-sum(ex.values())
    for s in sorted(STRATA,key=lambda z:(-(q[z]-ex[z]),STRATA.index(z)))[:left]:ex[s]+=1
    out={s:base[s]+ex[s] for s in STRATA}
    if sum(out.values())!=40:raise RuntimeError("FAIL-CLOSED: allocation")
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,default=Path("outputs/amovfly_preoutcome"));a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    tr=tree();bl=[x for x in tr if x.get("type")=="blob"]
    tm="\n".join(f"{x['path']}\t{x['sha']}\t{x.get('size','')}" for x in sorted(bl,key=lambda z:z["path"]))+"\n"
    ready=[];fails=[];manual=[]
    for x in bl:
        p=PurePosixPath(x["path"])
        if len(p.parts)!=3 or not p.name.lower().endswith(".csv"):continue
        sc,sub,name=p.parts
        if sc=="Random" and sub==sc:manual.append(x["path"]);continue
        if sc not in STRATA or sub!=sc:continue
        m=READY_RE.fullmatch(name)
        if not m:fails.append(x["path"]);continue
        cond=m.group("cond");ready.append({"scenario":sc,"uav":nu(m.group("uav")),"cond":cond,"num":int(m.group("num")),"path":x["path"],"blob":x["sha"],"size":x.get("size"),"p":pc(cond)})
    bb=defaultdict(list)
    for r in ready:bb[r["blob"]].append(r)
    alias={};conf={};units=[]
    for sha,rs in sorted(bb.items()):
        c=max(rs,key=completeness)
        if len(rs)>1:
            alias[sha]=sorted(r["path"] for r in rs)
            if not compatible(rs,c):conf[sha]=alias[sha]
        p=c["p"];units.append({"unit_id":f"readyblob:{sha}","scenario":c["scenario"],"uav":c["uav"],"condition_token":c["cond"],"payload_parameter":p["payload"],"altitude_parameter":p["alt"],"speed_parameter":p["speed"],"altitude_variable":p["avar"],"speed_variable":p["svar"],"altitude_parameter_available":p["alt_avail"],"condition_parse_ok":p["ok"],"flight_no":c["num"],"canonical_ready_path":c["path"],"ready_blob_sha":sha,"ready_size_bytes":c["size"],"alias_count":len(rs),"alias_paths":json.dumps(sorted(r["path"] for r in rs),separators=(",",":"))})
    pv=[u["payload_parameter"] for u in units if u["payload_parameter"] is not None];lo,hi=min(pv),max(pv)
    for u in units:
        ps=0 if hi==lo else (u["payload_parameter"]-lo)/(hi-lo);vs=(float(bool(u["altitude_variable"]))+float(bool(u["speed_variable"])))/2
        u.update(payload_severity=ps,variability_severity=vs,frozen_aux_risk=.5*ps+.5*vs)
    cs=dict(Counter(u["scenario"] for u in units));cu=dict(Counter(u["uav"] for u in units));al=alloc(cs)
    for u in units:u.update(stratum=u["scenario"],stratum_n_population=cs[u["scenario"]],stratum_n_allocated=al[u["scenario"]])
    fields=["unit_id","scenario","uav","condition_token","payload_parameter","altitude_parameter","speed_parameter","altitude_variable","speed_variable","altitude_parameter_available","condition_parse_ok","flight_no","payload_severity","variability_severity","frozen_aux_risk","stratum","stratum_n_population","stratum_n_allocated","canonical_ready_path","ready_blob_sha","ready_size_bytes","alias_count","alias_paths"]
    fp=a.out/"amovfly_path_only_unit_frame_v8.csv"
    with fp.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(sorted(units,key=lambda z:(z["scenario"],z["canonical_ready_path"])))
    counts={"autonomous_ready_paths":len(ready),"finite_population_unique_ready_blobs":len(units),"excluded_manual_random_paths":len(manual),"path_parse_failures":len(fails),"condition_parse_failures":sum(not u["condition_parse_ok"] for u in units),"alias_blob_groups":len(alias),"unresolved_alias_conflicts":len(conf)}
    gate="PASS_AUTONOMOUS_PATH_FRAME" if len(units)>=80 and not fails and counts["condition_parse_failures"]==0 and not conf else "BLOCKED_AUTONOMOUS_PATH_FRAME"
    man={"schema_version":"KTES-AMOVFLY-PATH-ONLY-v8.2","gate":gate,"source_repository":REPO,"source_commit":COMMIT,"source_tree_sha":TREE_SHA,"source_tree_metadata_sha256":h256(tm.encode()),"unit_definition":"one unique ready-data Git blob in FAFS/FAVS/VAFS/VAVS; byte-identical aliases collapsed","outcome_access":{"flight_info_rows":False,"raw_csv_values":False,"ready_csv_values":False},"eligibility":{"included_scenarios":list(STRATA),"excluded_random_reason":"README identifies Random as manual control","multi_uav_in_primary_population":False},"kernel_geometry_fields":["scenario one-hot","uav one-hot","payload_parameter","altitude_parameter + availability flag","speed_parameter","altitude_variable","speed_variable"],"adverse_tail_fields":["payload_severity","altitude_variable","speed_variable"],"auxiliary_risk_formula":"0.5*((altitude_variable+speed_variable)/2)+0.5*minmax(payload_parameter)","counts":counts,"counts_by_scenario":cs,"counts_by_uav":cu,"allocation_n40":al,"parse_fail_paths":fails,"unresolved_alias_conflicts_detail":conf,"alias_blob_groups":alias,"unit_frame_sha256":h256(fp.read_bytes())}
    jp=a.out/"amovfly_path_only_inventory_manifest_v8.json";jp.write_text(json.dumps(man,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    md=["# AMOVFLY autonomous-flight pre-outcome path inventory v8","",f"**Gate:** **{gate}**","","Only pinned Git-tree metadata were read. No `Flight_info.csv` row and no raw/ready telemetry value was opened.","",f"- source commit: `{COMMIT}`",f"- unique autonomous ready-blob units: {len(units)}",f"- excluded Random/manual paths: {len(manual)}",f"- alias groups collapsed: {len(alias)}",f"- unresolved alias conflicts: {len(conf)}",f"- path parse failures: {len(fails)}",f"- condition parse failures: {counts['condition_parse_failures']}","","## Scenario strata and n=40 allocation","","| Stratum | N | n |","|---|---:|---:|"]
    for s in STRATA:md.append(f"| {s} | {cs.get(s,0)} | {al.get(s,0)} |")
    md += ["","## Frozen design-side semantics","","Kernel geometry uses scenario/UAV identity, payload, explicitly encoded altitude/speed parameters, structural altitude availability, and altitude/speed variability flags. Missing variable-altitude values are not imputed from telemetry.","","Auxiliary risk is `0.5*variability_severity + 0.5*payload_severity`. Speed and altitude magnitudes are not assigned an adverse direction without independent engineering justification.","","`Random` is excluded because the source README describes manual control. Multi-UAV records are not added without a separately frozen one-flight-one-outcome map.","","A PASS authorizes R5 design-object instantiation only; telemetry outcomes remain closed.",""]
    mp=a.out/"AMOVFLY_PATH_ONLY_INVENTORY_v8.md";mp.write_text("\n".join(md),encoding="utf-8")
    print(json.dumps({"gate":gate,"counts":counts,"counts_by_scenario":cs,"counts_by_uav":cu,"allocation_n40":al},indent=2))
    for p in (mp,jp,fp):print(p.name,h256(p.read_bytes()))
if __name__=="__main__":main()
