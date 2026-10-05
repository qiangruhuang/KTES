#!/usr/bin/env python3
"""Audit Anti-UAV410 performance.json against the frozen KTES Phase 2A input contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_SIAMFC_SEQUENCES = 120
EXPECTED_SHA256 = "7861cded4d79dfd37ce251e8167f81ce145ea8f9ed68d8dd1f4b252ca33d82a0"
SA_KEYS = {"sa", "sa_score", "state_accuracy", "state_accuracy_score"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("performance_json", type=Path)
    args = parser.parse_args()

    path = args.performance_json
    digest = sha256(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    siamfc = data.get("SiamFC")
    if not isinstance(siamfc, dict):
        raise SystemExit("FAIL: SiamFC block is absent")

    seq = siamfc.get("seq_wise")
    if not isinstance(seq, dict):
        raise SystemExit("FAIL: SiamFC.seq_wise is absent")

    field_union = set()
    for record in seq.values():
        if isinstance(record, dict):
            field_union.update(record.keys())

    normalized = {k.lower() for k in field_union}
    has_sa = bool(normalized & SA_KEYS)
    overall = siamfc.get("overall", {})

    print(f"path={path}")
    print(f"size_bytes={path.stat().st_size}")
    print(f"sha256={digest}")
    print(f"sha256_matches_expected={digest == EXPECTED_SHA256}")
    print(f"tracker_blocks={len(data)}")
    print(f"siamfc_sequence_count={len(seq)}")
    print(f"sequence_count_matches_protocol={len(seq) == EXPECTED_SIAMFC_SEQUENCES}")
    print(f"sequence_fields={','.join(sorted(field_union))}")
    print(f"has_state_accuracy={has_sa}")
    print(f"siamfc_success_score={overall.get('success_score')}")
    print(f"siamfc_precision_score={overall.get('precision_score')}")
    print(f"siamfc_success_rate={overall.get('success_rate')}")

    if len(seq) != EXPECTED_SIAMFC_SEQUENCES:
        print("RESULT GATE BLOCKED: finite-population sequence count does not match N=120")
        return 2
    if not has_sa:
        print("RESULT GATE BLOCKED: pre-registered per-sequence SA_i endpoint is absent")
        return 2

    print("PRIMARY OUTCOME PRESENT: proceed to the frozen 500-replay gate evaluator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
