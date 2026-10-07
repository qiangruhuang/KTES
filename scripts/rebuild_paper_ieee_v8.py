#!/usr/bin/env python3
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'paper' / 'PAPER_IEEE_v8.parts'
OUT = ROOT / 'paper' / 'PAPER_IEEE_v8.md'
EXPECTED_SHA256 = '710702c979036957cc00ad5b385965802331175d9d1d71d2f1573ca5c81e4bc1'
EXPECTED_BYTES = 49485

parts = sorted(PARTS.glob('part*.md'))
if len(parts) != 7:
    raise SystemExit(f'expected 7 parts, found {len(parts)}')
blob = b''.join(p.read_bytes() for p in parts)
sha = hashlib.sha256(blob).hexdigest()
if len(blob) != EXPECTED_BYTES:
    raise SystemExit(f'byte-size mismatch: {len(blob)} != {EXPECTED_BYTES}')
if sha != EXPECTED_SHA256:
    raise SystemExit(f'SHA256 mismatch: {sha} != {EXPECTED_SHA256}')
OUT.write_bytes(blob)
print(f'wrote {OUT} ({len(blob)} bytes, sha256={sha})')
