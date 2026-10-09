#!/usr/bin/env python3
from pathlib import Path
import base64, hashlib, json, zlib
ROOT=Path(__file__).resolve().parents[1]
PARTS=sorted((ROOT/'paper'/'PAPER_JQT_v8_4.payload').glob('part*.b64'))
if not PARTS:
    raise SystemExit('no payload parts')
encoded=''.join(p.read_text().strip() for p in PARTS)
payload=json.loads(zlib.decompress(base64.b64decode(encoded)).decode('utf-8'))
for rel,rec in payload['files'].items():
    data=base64.b64decode(rec['content_b64'])
    got=hashlib.sha256(data).hexdigest()
    if got != rec['sha256']:
        raise SystemExit(f'hash mismatch {rel}: {got} != {rec["sha256"]}')
    out=ROOT/rel
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(data)
    got2=hashlib.sha256(out.read_bytes()).hexdigest()
    if got2 != rec['sha256']:
        raise SystemExit(f'post-write hash mismatch {rel}')
    print('verified',rel,got2)
print('materialized',len(payload['files']),'canonical v8.4 JQT assets')
