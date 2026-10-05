#!/usr/bin/env python3
"""Rebuild the frozen v7 manuscript from GitHub-safe line-boundary parts."""
from pathlib import Path
import hashlib

EXPECTED = "49f4810fa2cbfe91b9d9143cfa7715b1250939d5d28d7e476b896eb8ca4ce01d"
root = Path(__file__).resolve().parents[1]
parts_dir = root / "paper" / "PAPER_IEEE_v7.parts"
out = root / "paper" / "PAPER_IEEE_v7.md"
parts = sorted(parts_dir.glob("part*.md"))
if len(parts) != 7:
    raise SystemExit(f"expected 7 parts, found {len(parts)}")
data = b"".join(p.read_bytes() for p in parts)
digest = hashlib.sha256(data).hexdigest()
if digest != EXPECTED:
    raise SystemExit(f"SHA256 mismatch: {digest} != {EXPECTED}")
out.write_bytes(data)
print(f"rebuilt {out} ({len(data)} bytes) sha256={digest}")
