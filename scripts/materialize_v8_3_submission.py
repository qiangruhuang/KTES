#!/usr/bin/env python3
"""Materialize the locally audited KTES v8.3 text submission package.

The two base64 parts encode a zlib-compressed UTF-8 JSON mapping from repository
paths to exact canonical text bytes. This is a transport/reproducibility layer;
it does not recompute scientific results. Every written file is SHA-256 checked.
"""
from pathlib import Path
import base64, hashlib, json, zlib

ROOT = Path(__file__).resolve().parents[1]
PARTS = [
    ROOT / "paper/PAPER_IEEE_v8_3.payload/part01.b64",
    ROOT / "paper/PAPER_IEEE_v8_3.payload/part02.b64",
]
EXPECTED = {
    "paper/PAPER_IEEE_v8_3.md": "c90b1c20b9e605db8e30da1a70250ec0ea9eaf57cfcccddca1bd0f4b13f5a7e1",
    "paper/SUPPLEMENTARY_INFORMATION_v8_3.md": "38d2dd47b56e26605fb77853490969485eee4a04f60682c90ba0ab27612de6da",
    "paper/references_v8_3.bib": "ba4367a0233ef569643b9dacd96b6381370fdaaeb660657d53857033d035b40a",
    "paper/IEEE_JOURNAL_FORMAT_GATE_v8_3.md": "55feaa710db297a7d20c47173e382ddf90767644a4a4ae7dc204ed986fb768d8",
    "paper/IEEE_LATEX_MAPPING_v8_3.md": "f2a442afc102623a03da50e33162f48cd22728cefdb27f5c69d57404aefbf121",
    "paper/VIRTUAL_PAGEFLOW_AUDIT_v8_3.md": "701347481dc36fbf959f70612c5ad40f3a57629254e0c21b49a51256cf3eddef",
    "paper/REFERENCE_FORMAT_AUDIT_v8_3.md": "9abd7f299b5367a0264b9f42fdddb6155acdd9e59d9334beed7af42c30858691",
    "paper/ADVERSARIAL_REVIEW_v8_3.md": "f172e5c1eb4710812d92772e2b38db356e33b3f1ad9273f7f498405e8ca152ff",
    "paper/AUTOMATED_FREEZE_AUDIT_v8_3.md": "97d6ba1ef860dd179192aefecaf7227ba98dc13fb6b40df607230f60bd6a967e",
    "paper/HANDOFF_v8_3.md": "dc568b788f84d7c7601eb0f769340588cab26ddadc95b1ed71c2ad54bcec16ee",
    "paper/V8_3_SUBMISSION_MANIFEST.json": "3a30939db48baa2ca9eceedd17fe03cb24e37e77a93341040004b0fcd57d3485",
    "scripts/audit_v8_3_submission.py": "52f0e2df80ccfc952841446ee02f45a6ca8ff0ec0044cdc6947c3289643c7da2",
}

encoded = "".join(p.read_text(encoding="ascii").strip() for p in PARTS)
payload = json.loads(zlib.decompress(base64.b64decode(encoded)).decode("utf-8"))
if set(payload) != set(EXPECTED):
    raise SystemExit(f"payload path mismatch: {sorted(set(payload) ^ set(EXPECTED))}")
for rel, expected in EXPECTED.items():
    data = payload[rel].encode("utf-8")
    got = hashlib.sha256(data).hexdigest()
    if got != expected:
        raise SystemExit(f"payload hash mismatch for {rel}: {got} != {expected}")
    dest = ROOT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    got2 = hashlib.sha256(dest.read_bytes()).hexdigest()
    if got2 != expected:
        raise SystemExit(f"post-write hash mismatch for {rel}: {got2} != {expected}")
    print(f"verified {rel} {expected}")
print(f"materialized {len(EXPECTED)} canonical v8.3 text assets")
