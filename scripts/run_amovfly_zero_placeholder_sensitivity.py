#!/usr/bin/env python3
"""Post-outcome sensitivity for AMOVFLY exact-(0,0) waypoint placeholders.

This analysis does not replace the frozen confirmatory endpoint. It keeps the
pre-outcome KTES design, comparators, seeds, inclusion probabilities and gates
fixed, but recomputes the bounded waypoint-attainment outcome after excluding
only exact (0,0) aim-waypoint episodes identified by the semantic audit.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

import run_amovfly_external_validation as base
from audit_amovfly_waypoint_semantics import episode_rows


def clean_outcomes(frame: pd.DataFrame, source_root: Path) -> pd.DataFrame:
    rows = []
    for _, r in frame.iterrows():
        ep = pd.DataFrame(
            episode_rows(
                source_root / str(r.canonical_ready_path),
                str(r.unit_id),
                str(r.scenario),
                str(r.uav),
            )
        )
        ep = ep.loc[~ep.exact_zero_waypoint].copy()
        if ep.empty:
            raise RuntimeError(f"all waypoint episodes are exact zero: {r.unit_id}")
        d = ep.dmin_m.to_numpy(float)
        rows.append(
            {
                "unit_id": r.unit_id,
                "scenario": r.scenario,
                "uav": r.uav,
                "Y10": float(np.mean(d <= 10.0)),
                "F10": int(np.any(d > 10.0)),
                "Y2": float(np.mean(d <= 2.0)),
                "F2": int(np.any(d > 2.0)),
                "n_waypoint_episodes": int(len(ep)),
                "n_no_position_episodes": int(np.sum(~np.isfinite(d))),
            }
        )
    out = pd.DataFrame(rows)
    if out.unit_id.tolist() != frame.unit_id.tolist():
        raise RuntimeError("outcome/frame order mismatch")
    return out


def paired(a, b):
    d = np.asarray(a, float) - np.asarray(b, float)
    m = float(d.mean())
    se = float(d.std(ddof=1) / math.sqrt(len(d)))
    return {"mean_diff": m, "ci_lo": m - 1.96 * se, "ci_hi": m + 1.96 * se}


def run(frame, st, p, Xs, Xadv, phi, nov, risk, obj, eng, outcomes, outdir):
    *_, cpk, pwr, gs, satt = eng
    y = outcomes.Y10.to_numpy(float)
    f10 = outcomes.F10.to_numpy(float)
    y2 = outcomes.Y2.to_numpy(float)
    unit_ids = frame.unit_id.astype(str).to_numpy()
    order = np.lexsort((unit_ids, y))
    difficult = set(order[: math.ceil(0.10 * base.N)].tolist())
    masks = [(frame.scenario == s).to_numpy() for s in base.STRATA] + [
        (frame.uav == u).to_numpy() for u in base.UAVG
    ]

    rows = []
    failures = []
    for seed in base.SEEDS:
        for method in ["c-pKTES-Hedge", "Stratified-SRS", "Split15+Audit25"]:
            try:
                sel, pi, prob, bal = base.sample(
                    method, seed, frame, st, p, Xs, Xadv, phi, nov, risk, obj, cpk
                )
                est, pe, cov, ess = base.profile(y, p, st, sel, pi, Xs, gs, pwr, satt)
                _, fe, fcov, _ = base.profile(f10, p, st, sel, pi, Xs, gs, pwr, satt)
                _, p2, _, _ = base.profile(y2, p, st, sel, pi, Xs, gs, pwr, satt)
                de = float(np.mean([base.domain_error(y, p, m, sel, pi) for m in masks]))
                w = p[prob] / pi[prob]
                pess = float(w.sum() ** 2 / max(np.sum(w * w), 1e-15))
                rows.append(
                    {
                        "seed": int(seed),
                        "method": method,
                        "profile_estimate_Y10": est,
                        "profile_error_Y10": pe,
                        "failure_error_F10": fe,
                        "critical_domain_error_Y10": de,
                        "difficult_case_hit": int(any(int(i) in difficult for i in sel)),
                        "ess_all": ess,
                        "ess_probability_component": pess,
                        "min_pi_selected": float(np.min(pi[sel])),
                        "profile_uq_covered_Y10": cov,
                        "failure_uq_covered_F10": fcov,
                        "profile_error_Y2": p2,
                        "balance_error": bal,
                    }
                )
            except Exception as e:
                failures.append({"seed": int(seed), "method": method, "error": repr(e)})

    raw = pd.DataFrame(rows)
    raw_path = outdir / "amovfly_zero_placeholder_sensitivity_500_replay_raw_v8.csv"
    raw.to_csv(raw_path, index=False)
    if failures or len(raw) != 1500:
        (outdir / "amovfly_zero_placeholder_sensitivity_failures_v8.json").write_text(
            json.dumps(failures, indent=2) + "\n"
        )
        raise RuntimeError(f"sensitivity replay failure n={len(failures)} rows={len(raw)}")

    summaries = []
    for method, d in raw.groupby("method"):
        summaries.append(
            {
                "method": method,
                "n_replays": len(d),
                "profile_error_Y10_mean": float(d.profile_error_Y10.mean()),
                "critical_domain_error_Y10_mean": float(d.critical_domain_error_Y10.mean()),
                "difficult_case_hit_rate": float(d.difficult_case_hit.mean()),
                "ess_probability_median": float(d.ess_probability_component.median()),
                "ess_probability_p05": float(d.ess_probability_component.quantile(0.05)),
                "profile_uq_coverage_Y10": float(d.profile_uq_covered_Y10.mean()),
                "failure_error_F10_mean": float(d.failure_error_F10.mean()),
                "failure_uq_coverage_F10": float(d.failure_uq_covered_F10.mean()),
                "profile_error_Y2_mean": float(d.profile_error_Y2.mean()),
            }
        )
    summary = pd.DataFrame(summaries)
    summary.to_csv(outdir / "amovfly_zero_placeholder_sensitivity_summary_v8.csv", index=False)

    k = raw[raw.method == "c-pKTES-Hedge"].sort_values("seed")
    s = raw[raw.method == "Stratified-SRS"].sort_values("seed")
    b = raw[raw.method == "Split15+Audit25"].sort_values("seed")
    g3 = paired(k.profile_error_Y10, s.profile_error_Y10)
    kdom = float(k.critical_domain_error_Y10.mean())
    sdom = float(s.critical_domain_error_Y10.mean())
    bdom = float(b.critical_domain_error_Y10.mean())
    best = min(sdom, bdom)
    khit = float(k.difficult_case_hit.mean())
    bhit = float(b.difficult_case_hit.mean())

    gates = {
        "G1_positive_pi_no_sampling_failure": bool(len(k) == 500 and np.all(k.min_pi_selected > 0)),
        "G2_ESS": bool(k.ess_probability_component.median() >= 18.5 and k.ess_probability_component.quantile(0.05) >= 12),
        "G3_profile_noninferiority": bool(g3["mean_diff"] <= 0.01),
        "G4_critical_domain": bool(kdom - best <= 0.02),
        "G5_difficult_hit": bool(khit - bhit >= -0.10),
    }
    result = {
        "schema_version": "KTES-AMOVFLY-ZERO-PLACEHOLDER-SENSITIVITY-v8.1",
        "classification": "POST_OUTCOME_SENSITIVITY_ONLY",
        "confirmatory_result_replaced": False,
        "population_truth": {
            "N": base.N,
            "Y10_mean": float(outcomes.Y10.mean()),
            "F10_rate": float(outcomes.F10.mean()),
            "Y2_mean": float(outcomes.Y2.mean()),
            "F2_rate": float(outcomes.F2.mean()),
            "difficult_n": len(difficult),
        },
        "gates_under_sensitivity_definition": gates,
        "all_five_sensitivity_gates_pass": bool(all(gates.values())),
        "G3_paired": g3,
        "G4": {
            "ktes": kdom,
            "srs": sdom,
            "split15": bdom,
            "better_comparator": best,
            "ktes_minus_better": kdom - best,
        },
        "G5": {"ktes": khit, "split15": bhit, "difference": khit - bhit},
        "design_sha256": base.DESIGN_SHA,
        "frame_sha256": base.FRAME_SHA,
        "raw_replay_sha256": base.sha(raw_path),
        "interpretation": "Diagnostic robustness analysis only. Exact-zero exclusion was defined after outcome access and cannot replace the frozen confirmatory endpoint.",
    }
    (outdir / "AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    md = f"""# AMOVFLY exact-zero waypoint sensitivity v8

**Classification:** **POST-OUTCOME SENSITIVITY ONLY**  
**Confirmatory AMOVFLY result:** unchanged

The frozen design, inclusion probabilities, certainty sentinels, comparators, replay seeds and numerical guardrails are unchanged. The only diagnostic change is exclusion of exact `(0,0)` aim-waypoint episodes, which the semantic audit identified after outcome access as the sole source of all >100 km waypoint distances.

## Diagnostic population

- mean `Y10`: **{result['population_truth']['Y10_mean']:.9f}**
- `F10` rate: **{result['population_truth']['F10_rate']:.9f}**
- mean `Y2`: **{result['population_truth']['Y2_mean']:.9f}**

## Frozen-design replay sensitivity

| Quantity | Result |
|---|---:|
| G3 KTES−SRS profile-error mean difference | {g3['mean_diff']:.9f} |
| G3 95% CI | [{g3['ci_lo']:.9f}, {g3['ci_hi']:.9f}] |
| KTES critical-domain error | {kdom:.9f} |
| SRS critical-domain error | {sdom:.9f} |
| Split15 critical-domain error | {bdom:.9f} |
| KTES−better-comparator domain error | {kdom-best:.9f} |
| KTES difficult-case hit | {khit:.6f} |
| Split15 difficult-case hit | {bhit:.6f} |
| All five numerical gates under this sensitivity definition | {'PASS' if all(gates.values()) else 'FAIL'} |

## Interpretation

This sensitivity cannot be promoted to a new confirmatory result because the exact-zero exclusion was specified after telemetry outcome access. Its role is only to determine whether the method-comparison conclusion is fragile to the systematic placeholder identified in the frozen endpoint. The original confirmatory result and this sensitivity must be reported side by side.
"""
    (outdir / "AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md").write_text(md, encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", type=Path, required=True)
    ap.add_argument("--source-root", type=Path, required=True)
    ap.add_argument("--vendor-src", type=Path, default=Path("vendor/r5_engine_recovered_v8/src"))
    ap.add_argument("--out", type=Path, default=Path("outputs/amovfly_zero_sensitivity"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    frame, st, p, Xs, Xadv, phi, nov, risk, obj, eng = base.prepare_design(
        args.frame, args.vendor_src, args.out
    )
    outcomes = clean_outcomes(frame, args.source_root)
    outcomes.to_csv(args.out / "amovfly_zero_placeholder_sensitivity_outcomes_v8.csv", index=False)
    run(frame, st, p, Xs, Xadv, phi, nov, risk, obj, eng, outcomes, args.out)


if __name__ == "__main__":
    main()
