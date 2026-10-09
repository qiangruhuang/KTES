#!/usr/bin/env python3
from pathlib import Path
import base64,hashlib,zlib
ROOT=Path(__file__).resolve().parents[1]
parts=sorted((ROOT/"paper"/"PAPER_JQT_v8_4_expanded.payload").glob("part*.b64"))
encoded="".join(p.read_text(encoding="ascii").strip() for p in parts)
data=zlib.decompress(base64.b64decode(encoded))
expected="1a4fec05538eb2ab74d7884b2b0f38d96b09d2de3088c935d46beb2d973b3d2c"
got=hashlib.sha256(data).hexdigest()
if got != expected:
    raise SystemExit(f"hash mismatch: {got} != {expected}")
out=ROOT/"paper"/"PAPER_JQT_v8_4.md"
out.write_bytes(data)
got2=hashlib.sha256(out.read_bytes()).hexdigest()
if got2 != expected:
    raise SystemExit("post-write hash mismatch")
print("verified",out,got2)
