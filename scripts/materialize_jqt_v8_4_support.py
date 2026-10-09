#!/usr/bin/env python3
from pathlib import Path
import base64, hashlib, json, zlib
ROOT=Path(__file__).resolve().parents[1]
PARTS=sorted((ROOT/'paper'/'PAPER_JQT_v8_4.payload').glob('part*.b64'))
if not PARTS:
    raise SystemExit('no legacy v8.4 payload parts')
encoded=''.join(p.read_text().strip() for p in PARTS)
payload=json.loads(zlib.decompress(base64.b64decode(encoded)).decode('utf-8'))
wanted={'SUPPLEMENTARY_INFORMATION_JQT_v8_4.md','references_JQT_v8_4.bib'}
found=set()
for rel,rec in payload['files'].items():
    name=Path(rel).name
    if name not in wanted:
        continue
    data=base64.b64decode(rec['content_b64'])
    got=hashlib.sha256(data).hexdigest()
    if got != rec['sha256']:
        raise SystemExit(f'hash mismatch {name}: {got} != {rec["sha256"]}')
    out=ROOT/'paper'/name
    out.write_bytes(data)
    if hashlib.sha256(out.read_bytes()).hexdigest() != rec['sha256']:
        raise SystemExit(f'post-write hash mismatch {name}')
    print('verified',name,got)
    found.add(name)
if found != wanted:
    raise SystemExit(f'missing support assets: {wanted-found}')
print('materialized 2 JQT support assets without touching the expanded manuscript')
