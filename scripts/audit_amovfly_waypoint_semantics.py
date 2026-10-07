#!/usr/bin/env python3
"""Post-outcome semantic audit for the frozen AMOVFLY waypoint endpoint.

This script does NOT modify the frozen confirmatory endpoint. It quantifies whether
literal (0,0) current-waypoint values or other extreme target coordinates explain
the degenerate F10=1 result and very large per-episode distances, and reports a
clearly labelled diagnostic sensitivity that excludes exact (0,0) episodes only.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

EARTH = 6_371_008.8
REQ = ["real_lat", "real_long", "aim_lat", "aim_long"]
EXPECTED_N = 257
EXPECTED_FRAME_SHA = "92a6d63eb75a0eee58e9d310da9b140517e2dffd2c6f48986fd21b40c8b12c85"
EXPECTED_FROZEN_Y10 = 0.9461052329912304


def sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def haversine(lat, lon, alat, alon):
    lat = np.radians(lat)
    lon = np.radians(lon)
    a1 = math.radians(alat)
    a2 = math.radians(alon)
    dlat = lat - a1
    dlon = lon - a2
    a = np.sin(dlat / 2) ** 2 + np.cos(lat) * math.cos(a1) * np.sin(dlon / 2) ** 2
    return 2 * EARTH * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def episode_rows(path: Path, unit_id: str, scenario: str, uav: str):
    d = pd.read_csv(path, usecols=lambda c: str(c).strip() in REQ)
    d.columns = [str(c).strip() for c in d.columns]
    if set(d.columns) != set(REQ):
        raise RuntimeError(f"required columns missing: {path}")
    x = {c: pd.to_numeric(d[c], errors="coerce").to_numpy(float) for c in REQ}
    va = (
        np.isfinite(x["aim_lat"])
        & np.isfinite(x["aim_long"])
        & (np.abs(x["aim_lat"]) <= 90)
        & (np.abs(x["aim_long"]) <= 180)
    )
    vr = (
        np.isfinite(x["real_lat"])
        & np.isfinite(x["real_long"])
        & (np.abs(x["real_lat"]) <= 90)
        & (np.abs(x["real_long"]) <= 180)
    )

    out = []
    cur = None
    idx = []

    def flush():
        nonlocal cur, idx
        if cur is None or not idx:
            return
        ii = np.asarray(idx, int)
        good = vr[ii]
        if np.any(good):
            jj = ii[good]
            dmin = float(np.min(haversine(x["real_lat"][jj], x["real_long"][jj], cur[0], cur[1])))
        else:
            dmin = float("inf")
        exact_zero = bool(cur[0] == 0.0 and cur[1] == 0.0)
        near_zero = bool(abs(cur[0]) <= 1e-6 and abs(cur[1]) <= 1e-6)
        out.append(
            {
                "unit_id": unit_id,
                "scenario": scenario,
                "uav": uav,
                "aim_lat": cur[0],
                "aim_long": cur[1],
                "n_rows": int(len(ii)),
                "n_valid_position_rows": int(np.sum(good)),
                "dmin_m": dmin,
                "exact_zero_waypoint": exact_zero,
                "near_zero_waypoint": near_zero,
                "extreme_gt_100km": bool(np.isfinite(dmin) and dmin > 100_000),
            }
        )

    for i in range(len(d)):
        key = (
            (round(float(x["aim_lat"][i]), 7), round(float(x["aim_long"][i]), 7))
            if va[i]
            else None
        )
        if key != cur:
            flush()
            cur = key
            idx = []
        if key is not None:
            idx.append(i)
    flush()
    if not out:
        raise RuntimeError(f"no valid waypoint episode: {path}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", type=Path, required=True)
    ap.add_argument("--source-root", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if sha256(args.frame) != EXPECTED_FRAME_SHA:
        raise SystemExit("frozen frame hash mismatch")
    frame = pd.read_csv(args.frame)
    if len(frame) != EXPECTED_N or frame.unit_id.duplicated().any():
        raise SystemExit("frozen finite-population identity mismatch")

    episodes = []
    for _, r in frame.iterrows():
        p = args.source_root / str(r.canonical_ready_path)
        episodes.extend(episode_rows(p, str(r.unit_id), str(r.scenario), str(r.uav)))
    ep = pd.DataFrame(episodes)
    ep.to_csv(args.out / "amovfly_waypoint_semantic_episode_audit_v8.csv", index=False)

    flight_rows = []
    for unit_id, g in ep.groupby("unit_id", sort=False):
        d = g.dmin_m.to_numpy(float)
        orig_y10 = float(np.mean(d <= 10.0))
        exact_zero = g.exact_zero_waypoint.to_numpy(bool)
        keep = ~exact_zero
        if not np.any(keep):
            raise RuntimeError(f"all episodes exact-zero for {unit_id}")
        dc = d[keep]
        clean_y10 = float(np.mean(dc <= 10.0))
        row0 = g.iloc[0]
        flight_rows.append(
            {
                "unit_id": unit_id,
                "scenario": row0.scenario,
                "uav": row0.uav,
                "n_episodes": int(len(g)),
                "n_exact_zero_episodes": int(np.sum(exact_zero)),
                "n_extreme_gt_100km": int(np.sum(g.extreme_gt_100km)),
                "n_nonzero_extreme_gt_100km": int(np.sum(g.extreme_gt_100km & ~g.exact_zero_waypoint)),
                "Y10_frozen_literal": orig_y10,
                "F10_frozen_literal": int(np.any(d > 10.0)),
                "Y10_excluding_exact_zero_diagnostic": clean_y10,
                "F10_excluding_exact_zero_diagnostic": int(np.any(dc > 10.0)),
                "delta_Y10_clean_minus_frozen": clean_y10 - orig_y10,
            }
        )
    fl = pd.DataFrame(flight_rows)
    fl.to_csv(args.out / "amovfly_waypoint_semantic_flight_audit_v8.csv", index=False)

    frozen_mean = float(fl.Y10_frozen_literal.mean())
    if abs(frozen_mean - EXPECTED_FROZEN_Y10) > 1e-12:
        raise RuntimeError(f"literal Y10 reproduction mismatch: {frozen_mean}")

    exact_zero_eps = int(ep.exact_zero_waypoint.sum())
    extreme_eps = int(ep.extreme_gt_100km.sum())
    exact_zero_extreme = int((ep.exact_zero_waypoint & ep.extreme_gt_100km).sum())
    nonzero_extreme = int((~ep.exact_zero_waypoint & ep.extreme_gt_100km).sum())
    summary = {
        "schema_version": "KTES-AMOVFLY-WAYPOINT-SEMANTIC-AUDIT-v8.1",
        "classification": "POST_OUTCOME_DIAGNOSTIC_ONLY",
        "frozen_confirmatory_result_changed": False,
        "population_n": int(len(fl)),
        "total_waypoint_episodes": int(len(ep)),
        "flights_with_exact_zero_waypoint": int((fl.n_exact_zero_episodes > 0).sum()),
        "exact_zero_waypoint_episodes": exact_zero_eps,
        "near_zero_waypoint_episodes": int(ep.near_zero_waypoint.sum()),
        "extreme_gt_100km_episodes": extreme_eps,
        "extreme_gt_100km_exact_zero_episodes": exact_zero_extreme,
        "extreme_gt_100km_nonzero_episodes": nonzero_extreme,
        "fraction_extreme_explained_by_exact_zero": (exact_zero_extreme / extreme_eps if extreme_eps else None),
        "frozen_literal": {
            "Y10_mean": frozen_mean,
            "F10_rate": float(fl.F10_frozen_literal.mean()),
        },
        "diagnostic_excluding_exact_zero_only": {
            "Y10_mean": float(fl.Y10_excluding_exact_zero_diagnostic.mean()),
            "F10_rate": float(fl.F10_excluding_exact_zero_diagnostic.mean()),
            "mean_delta_Y10": float(fl.delta_Y10_clean_minus_frozen.mean()),
            "median_delta_Y10": float(fl.delta_Y10_clean_minus_frozen.median()),
            "flights_Y10_changed": int((np.abs(fl.delta_Y10_clean_minus_frozen) > 1e-15).sum()),
        },
        "interpretation_rule": "The exact-zero exclusion is a post-outcome semantic diagnostic and must not replace the frozen confirmatory endpoint or PASS result.",
    }
    (args.out / "AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    z = summary["diagnostic_excluding_exact_zero_only"]
    md = f"""# AMOVFLY waypoint semantic audit v8

**Classification:** **POST-OUTCOME DIAGNOSTIC ONLY**  
**Frozen confirmatory result:** unchanged

## Finding

- Frozen population: {summary['population_n']} flights, {summary['total_waypoint_episodes']} waypoint episodes.
- Flights containing at least one exact `(0,0)` aim waypoint episode: **{summary['flights_with_exact_zero_waypoint']}**.
- Exact `(0,0)` episodes: **{exact_zero_eps}**.
- Episodes with minimum actual-to-aim distance >100 km: **{extreme_eps}**.
- Of those extreme episodes, exact `(0,0)` episodes account for **{exact_zero_extreme}**; non-zero targets account for **{nonzero_extreme}**.
- Fraction of >100 km episodes explained by exact zero: **{summary['fraction_extreme_explained_by_exact_zero']}**.

## Frozen literal endpoint

- mean `Y10`: **{frozen_mean:.9f}**.
- `F10` rate: **{float(fl.F10_frozen_literal.mean()):.9f}**.

## Diagnostic exact-zero exclusion

Excluding exact `(0,0)` episodes only, without changing any other episode rule:

- mean `Y10`: **{z['Y10_mean']:.9f}**;
- `F10` rate: **{z['F10_rate']:.9f}**;
- mean per-flight change in `Y10`: **{z['mean_delta_Y10']:.9f}**;
- flights whose `Y10` changes: **{z['flights_Y10_changed']} / {summary['population_n']}**.

## Research-integrity interpretation

This audit was defined after the frozen telemetry outcome was opened. It is therefore a semantic diagnostic, not a repaired confirmatory endpoint. The frozen AMOVFLY external-validation result must remain reported exactly as executed. If exact-zero episodes materially drive the endpoint, the appropriate response is to narrow the engineering interpretation and, if desired, preregister a new independent validation rather than silently replacing the endpoint on the same dataset.
"""
    (args.out / "AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md").write_text(md, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
