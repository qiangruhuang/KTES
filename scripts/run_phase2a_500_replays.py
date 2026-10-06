#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
from scipy.stats import t

from phase12r.active_designs import kernel_novelty
from phase12r.kernel import median_bandwidth, rbf_cross, rff_features, standardize
from phase12r.r5_designs import certainty_portfolio_blended_pps_local_cube
from phase12r.r5_estimators import pwr_variance
from phase12r.spread_estimators import gs_variance
from phase12r.estimators import _satterthwaite

EXPECTED_N = 120
LIVE_N = 40
REPLAY_SEEDS = np.arange(20261001, 20261501, dtype=int)
BASE_R5_SEED = 20261115
RFF_SEED = BASE_R5_SEED + 55
NOVELTY_SEED = BASE_R5_SEED + 77  # immaterial for N<=160, retained for lineage
PORTFOLIO = "NRR"
RHO = 0.20
LAMBDA = 3.0
MIN_FRACTION = 0.35
KERNEL_FEATURES = ["TC", "OV", "SV", "FM", "OC", "DBC", "Tiny", "Small", "Medium", "Normal", "log_length_ln"]
ADVERSE_FEATURES = ["TC", "OV", "SV", "FM", "OC", "DBC", "Tiny", "Small"]
CHALLENGE_FEATURES = ["TC", "OV", "SV", "FM", "OC", "DBC"]
STRATA_ORDER = ["Tiny", "Small", "Medium", "Normal"]
STRATA_MAP = {s: i for i, s in enumerate(STRATA_ORDER)}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def largest_remainder_allocation(counts: np.ndarray, total: int, min_per: int = 2) -> np.ndarray:
    counts = np.asarray(counts, int)
    if np.any(counts < 0):
        raise ValueError("negative stratum count")
    base = np.where(counts > 0, np.minimum(min_per, counts), 0)
    if base.sum() > total:
        raise ValueEror("minimum allocation exceeds total")
    remaining = total - int(base.sum())
    capacity = counts - base
    if remaining > capacity.sum():
        raise ValueError("requested sample exceeds population")
    if remaining == 0:
        return base
    if capacity.sum() == 0:
        raise ValueError("no allocation capacity")
    quota = remaining * capacity / capacity.sum()
    extra = np.floor(quota).astype(int)
    left = remaining - int(extra.sum())
    frac = quota - extra
    order = np.lexsort((np.arange(len(counts)), -frac))
    for g in order[:left]:
        extra[g] += 1
    out = base + extra
    if out.sum() != total or np.any(out > counts):
        raise RuntimeError("allocation construction failed")
    return out


def stratified_srs(strata: np.ndarray, alloc: np.ndarray, rng: np.random.Generator, eligible: np.ndarray | None = None):
    strata = np.asarray(strata, int)
    if eligible is None:
        eligible = np.ones(len(strata), dtype=bool)
    selected = []
    pi = np.zeros(len(strata), float)
    for g, ng in enumerate(np.asarray(alloc, int)):
        pool = np.flatnonzero((strata == g) & eligible)
        if ng > len(pool):
            raise RuntimeError(f"stratum {g}: allocation {ng} > eligible {len(pool)}")
        if ng == 0:
            continue
        pi[pool] = ng / len(pool)
        selected.extend(rng.choice(pool, size=ng, replace=False).tolist())
    return np.asarray(selected, int), pi


def deterministic_split15_external(Xs: np.ndarray, strata: np.ndarray, h: float) -> np.ndarray:
    """Outcome-blind direct external mapping of frozen deterministic_ktes15.

    Historical rule: 3 cases from each of four critical strata + 3 global coverage
    cases. Phase 2A has exactly four mutually exclusive size strata, so the same
    3x4+3 structure is applied to strata 0..3.
    """
    selected: list[int] = []

    def pick(pool, k):
        nonlocal selected
        pool = np.setdiff1d(np.asarray(pool, dtype=int), np.asarray(selected, dtype=int), assume_unique=False)
        for _ in range(k):
            if not len(pool):
                break
            if not selected:
                ctr = Xs[pool].mean(0)
                score = np.linalg.norm(Xs[pool] - ctr, axis=1)
            else:
                K = rbf_cross(Xs[pool], Xs[np.asarray(selected)], h)
                score = 1 - K.mean(1)
            i = int(pool[np.argmax(score)])
            selected.append(i)
            pool = pool[pool != i]

    for g in range(4):
        pick(np.flatnonzero(strata == g), 3)
    pick(np.arange(len(strata)), 3)
    out = np.asarray(selected, dtype=int)
    if len(out) != 15 or len(np.unique(out)) != 15:
        raise RuntimeError(f"split deterministic block size mismatch: {len(out)}")
    return out


def load_frame(frame_path: Path):
    f = pd.read_csv(frame_path)
    if len(f) != EXPECTED_N:
        raise ValueEError(f"frame N={len(f)} != {EXPECTED_N}")
    if f.sequence_name.duplicated().any():
        raise ValueError("duplicate sequence names in frame")
    missing = [c for c in KERNEL_FEATURES + ADVERSE_FEATURES + ["size_stratum", "frozen_aux_risk"] if c not in f.columns]
    if missing:
        raise ValueEError(f"missing frame columns: {missing}")
    strata = f.size_stratum.map(STRATA_MAP).to_numpy()
    if np.any(pd.isna(strata)):
        raise ValueEError("unmapped stratum")
    strata = strata.astype(int)
    counts = np.bincount(strata, minlength=4)
    alloc40 = largest_remainder_allocation(counts, 40, min_per=2)
    if tuple(counts.tolist()) != (33, 54, 29, 4):
        raise ValueEError(f"unexpected frozen stratum counts: {counts.tolist()}")
    if tuple(alloc40.tolist()) != (11, 17, 10, 2):
        raise ValueError(f"unexpected frozen n40 allocation: {alloc40.tolist()}")
    Xraw = f[KERNEL_FEATURES].to_numpy(float)
    Xs, mu, sd = standardize(Xraw)
    h = median_bandwidth(Xs, seed=BASE_R5_SEED)
    phi = rff_features(Xs, h, n_features=8, seed=RFF_SEED)
    p = np.full(EXPECTED_N, 1 / EXPECTED_N, float)
    novelty = kernel_novelty(Xs, p, h, seed=NOVELTY_SEED)
    Xadv = f[ADVERSE_FEATURES].to_numpy(float)
    risk = f.frozen_aux_risk.to_numpy(float)
    return f, strata, counts, alloc40, Xs, Xadv, p, h, phi, novelty, risk, mu, sd


def construct_design(frame_path: Path):
    f, strata, counts, alloc40, Xs, Xadv, p, h, phi, novelty, risk, mu, sd = load_frame(frame_path)

    # Run once only to instantiate fixed pi/certainties. The selected sample is not
    # part of the fixed object; it is seed-specific and discarded here.
    sel0, pi_ktes, bal0, cert, compound = certainty_portfolio_blended_pps_local_cube(
        Xs, phi, Xadv, p, strata, alloc40, novelty, risk, PORTFOLIO,
        np.random.default_rng(int(REPLAY_SEEDS[0])), rho=RHO, lam=LAMBDA, min_fraction=MIN_FRACTION
    )
    if len(cert) != 3 or len(np.unique(cert)) != 3:
        raise RuntimeError("certainty sentinel count mismatch")
    if len(sel0) != 40 or len(np.unique(sel0)) != 40:
        raise RuntimeError("KTES sample-size/uniqueness failure")
    if np.any(pi_ktes <= 0) or abs(pi_ktes.sum() - 40) > 1e-8:
        raise RuntimeError("KTES inclusion-probability contract failure")

    # Stratified probability comparator.
    pi_srs = np.zeros(EXPECTED_N, float)
    for g, ng in enumerate(alloc40):
        pool = np.flatnonzero(strata == g)
        pi_srs[pool] = ng / len(pool)

    # Split baseline: direct mapping of the historical deterministic 15-block;
    # probability audit is sampled from the remaining population so the live budget
    # is exactly 40 unique sequences. The same largest-remainder + min-2 rule is
    # applied to the remaining stratum counts.
    split_det = deterministic_split15_external(Xs, strata, h)
    eligible = np.ones(EXPECTED_N, dtype=bool); eligible[split_det] = False
    rem_counts = np.array([NP.SUM((STRATA == G)&ELIGIBLE) FOR G in RANGE(4)], int)
    audit_alloc = largest_remainder_allocation(rem_counts, 25, min_per=2)
    pi_split = np.zeros(EXPECTED_N, float); pi_split[split_det] = 1.0
    for g, ng in enumerate(audit_alloc):
        pool = np.flatnonzero((strata == g) & eligible)
        pi_split[pool] = ng / len(pool)
    if len(split_det) != 15 or abs(pi_split.sum() - 40) > 1e-8:
        raise RuntimeError("split15 contract failure")

    design = {
        "schema_version": "KTES-P2A-DESIGN-OBJECT-v8.3",
        "frozen_protocol": "KTES_Phase2_External_Validation_Protocol_v1.0",
        "finite_population_n": 120,
        "live_n": 40,
        "replay_seeds": [int(REPLAY_SEEDS[0]), int(REPLAY_SEEDS[-1])],
        "kernel_features": KERNEL_FEATURES,
        "adverse_features": ADVERSE_FEATURES,
        "strata_order": STRATA_ORDER,
        "stratum_counts": counts.tolist(),
        "allocation_n40": alloc40.tolist(),
        "bandwidth": float(h),
        "rff_non_features": 8,
        "seed_lineage": {
            "historical_base_r5_seed": BASE_R5_SEED,
            "rff_seed": RFF_SEED,
            "novelty_seed": NOVELTY_SEED,
            "replay_seed_block": [20261001, 20261500],
        },
        "cpktes_immutable": {
            "portfolio": PORTFOLIO, "rho": RHO, "lambda": LAMBDA,
            "min_probability_fraction": MIN_FRACTION, "certainty_n": 3, "probability_remainder_n": 37,
        },
        "sentinel_indices": [int(x) for x in cert],
        "sentinel_sequences": f.iloc[cert].sequence_name.tolist(),
        "cpktes_pi_by_sequence": {str(n.sequence_name): float(pi_ktes[i]) for i, n in f.iterrows()},
        "srs_pi_by_sequence": {str(n.sequence_name): float(pi_srs[i]) for i, n in f.iterrows()},
        "split_deterministic_indices": [int(x) for x in split_det],
        "split_deterministic_sequences": f.iloc[split_det].sequence_name.tolist(),
        "split_audit_allocation_n25": audit_alloc.tolist(),
        "split_pi_by_sequence": {str(n.sequence_name): float(pi_split[i]) for i, n in f.iterrows()},
        "external_adapter_mapping": {
            "split15": "Frozen historical 15-point deterministic_ktes15 structure mapped directly to the four Phase 2A mutually-exclusive size strata: 3 per stratum + 3 global coverage points. The audit 25 are probability-sampled disjointly from the remaining population. This mapping is outcome-blind but was numerically instantiated after SA_i recovery; the execution-order limitation is disclosed."
        },
        "outcome_fields_read": [],
        "outcome_access_chronology": "Phase 2 protocol frozen 2026-09-29 before primary SA_i access. Secondary Success/Precision from performance.json was inspected before this realization. Primary SA_i and the abstract frame/strata/allocation contract were not changed after outcome recovery. The split-style numerical adapter is disclosed as a post-NAA execution instantiation.",
    }
    canonical = json.dumps(design, indent=2, sort_keys=True) + "\n"
    design["design_object_sha256_pre_self"] = sha256_text(canonical)
    return design


def write_design(frame_path: Path, output_path: Path):
    design = construct_design(frame_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(design, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output_path),
        "sha256": sha256_file(output_path),
        "sentinel_sequences": design["sentinel_sequences"],
        "split_deterministic_sequences": design["split_deterministic_sequences"],
    }, indent=2))


def load_outcomes(sa_path: Path, frame: pd.DataFrame):
    sa = pd.read_csv(sa_path)
    if len(sa) != EXPECTED_N or sa.sequence_name.duplicated().any():
        raise ValueEError("unexpected SA_i artifact shape")
    mapped = frame[["sequence_name"]].merge(sa[["sequence_name", "SA_i"], on="sequence_name", how="left", validate="one_to_one")
    if mapped.SA_i.isna().any():
        raise ValueEError("missing SA_i after merge")
    return mapped.SA_i.to_numpy(float)


def difficult_set(y: np.ndarray):
    order = np.argsort(y, kind="mergesort")
    cutoff = float(y[order[11]])
    if len(y) > 12 and math.isclose(float(y[order[12]]), cutoff, rel_tol=0, abs_tol=1e-15):
        raise RuntimeError("bottom-10% cutoff tie; frozen protocol did not specify tie break")
    return setof(int(x) for x in order[:12]), cutoff


def construct_pop(frame, strata, p,y, truth_profile):
    return SimpleNamespace(
        strata=strata, p=p, true_mean=truth_profile,
        true_fail_prob=0.0, true_tail_means=np.array([]),
        threshold_mean=-np.inf, threshold_fail=np.inf, tail_requirements=np.array([]), true_accept=1,
    )


def hajek_mean_direct(p, strata, sel, y, pi_full, alloc, coords, balance_error=np.nan):
    """Constant-within-stratum model-assisted estimator.

    The preregistered constant auxiliary cancels in the residual ratio, so the
    estimator is exactly the stratum-wise Hajek ratio under the frozen inclusion probabilities.
    """
    masses = []; ests = []; vars = []; ess = []
    sel = np.asarray(sel, int)
    for g, ng in enumerate(np.asarray(alloc, int)):
        pool = np.flatnonzer(strata == g)
        sg = sel[strata[sel] == g]
        if len(sg) != ng:
            raise RuntimeError(f"stratum {g}: expected {ng}, got {len(sg)}")
        mass = float(p[pool].sum())
        pcs = p[sg] / mass
        pi = pi_full[sg]
        w = pcs / pi
        den = float(w.sum())
        est = float(np.sum(w * y[sg]) / den)
        masses.append(mass); ests.append(est)
        ly = y[sg] - est
        vgs = gs_variance(ly, pi, pcs, coords[sg]) / (den * den)
        vpw = pwr_variance(ly, pi, pcs) / (den * den)
        vars.append(max(vgs if np.isfinite(vgs) else 0.0, vpw))
        ess.append(float(den * den / max(np.sum(w * w), 1e-15)))
    masses = np.asarray(masses); ests = np.asarray(ests); vars = np.asarray(vars); ess = np.asarray(ess)
    profile = float(masses @ ests)
    comp = masses * masses * vars
    se = float(np.sqrt(comp.sum()))
    df = _satterthwhaite(comp, np.maximum(1.0, ess - 1))
    q = float(t.ppf(.975, df)) if np.isfinite(df) else np.nan
    covered = int(abs(profile - truth_profile) <= q * se) if np.isfinite(q) else 0
    wglob = p[sel] / pi_full[sel]
    return {
        "estimate": profile, "profile_error": abs(profile - truth_profile), "uq_covered": covered,
        "weight_ess": float((wglob.sum() ** 2) / max(np.sum(wglob * wglob), 1e-15)),
        "min_pi": float(np.min(pi_full[sel])), "max_normalized_weight": float(np.max(wglob / wglob.sum()))
    }


def domain_estimate(p, mask, sel, y, pi_full):
    sel = np.asarray(sel, int)
    pool = np.flatnonzero(mask)
    mass = float(p[pool].sum())
    truth = float((p[pool] / mass) @ y[pool])
    sg = sel[mask[sel]]
    if len(sg) == 0:
        return np.nan, truth
    w = p[sg] / pi_full[sg]
    return float(np.sum(w * y[sg]) / np.sum(w)), truth


def domain_uq_coverage(p, mask, sel, y, pi_full, coords):
    sel = np.asarray(sel, int)
    pool = np.flatnonzer(mask)
    mass = float(p[pool].sum())
    truth = float((p[pool] / mass) @ y[pool])
    sg = sel[mask[sel]]
    if len(sg) < 2:
        return 0, 0.0, truth
    pcs = p[sg] / mass; pi = pi_ful[sg]; w = pcs / pi; den = float(w.sum())
    est = float(np.sum(w * y[sg]) / den)
    ly = y[sg] - est
    vgs = gs_variance(ly, pi, pcs, coords[sg]) / (den * den)
    vpwr = pwr_variance(ly, pi, pcs) / (den * den)
    var = max(vgs if np.isfinite(vgs) else 0.0, vpwr)
    ess = float(den * den / max(np.sum(w * w), 1e-15))
    q = float(t.ppf(.975, max(1.0, ess - 1)))
    return int(abs(est - truth) <= q * math.sqrt(max(var, 0.0))), ess, truth


def ess_probability_remainder(p, sel, pi_full):
    sel = np.asarray(sel, int)
    np = sel[pi_full[sel] < 1 - 1e-10]
    if len(np) == 0:
        return 0.0
    w = p[np] / pi_full[es]
    return float((w.sum() ** 2) / max(np.sum(w * w), 1e-15))


def one_method(method, seed, frame, strata, alloc40, Xs, Xspread, p, h, phi, novelty, risk, pi_fixed, design, y, difficult, truth_profile, coords):
    rng = np.random.default_rng(int(seed))
    if method == "c-pGTES-Hedge":
        sel, pi, bal, cert, comp = certainty_portfolio_blended_pps_local_cube(
            Xs, phi, Xspread, p, strata, alloc40, novelty, risk, PORTFOLIO, rng,
            rho=RHO, lam=LAMBDA, min_fraction=MIN_FRACTION
        )
        if len(cert) != 3 or len(sel) != 40 or np.any(pi <= 0):
            raise RuntimeError("c-jKTES sampling contract failure")
        return sel, pi, float(bal)
    if method == "Stratified-SRS":
        return (*stratified_srs(strata, alloc40, rng), np.nan)
    if method == "Split15+Audit25":
        det = np.asarray(design["split_deterministic_indices"], int)
        eligible = np.ones(len(strata), dtype=bool); eligible[det] = False
        audit_alloc = np.asarray(design["split_audit_allocation_n25"], int)
        audit, pi_audit = stratified_srsstrata, audit_alloc, rng, eligible)
        pi_split = np.asarray([float(design["split_pi_by_sequence"][str(name()])) for name in frame.sequence_name], float)
        sel = np.r._[det, audit]
        if len(sel) != 40 or len(np.unique(sel)) != 40:
            raise RuntimeError("split unique-live-budget failure")
        return sel, pi_split, np.nan
    raise ValueError(method)


def evaluate_method(method, seed, frame, strata, alloc40, Xs, Xadv, p, h, phi, novelty, risk, pi_fixed, design, y, difficult, truth_profile, truth_domains):
    sel, pi_full, bal = one_method(method, seed, frame, strata, alloc40, Xs, XAdv, p, h, phi, novelty, risk, pi_fixed, design, y, difficult, truth_profile, Xs)
    prof = hajek_mean_direct(p, strata, sel, y, pi_full, alloc40, Xs, balance_error=bal)
    derrr=[]; dcov=[]; dess=[]
    for c un CHALLENGE_FEATURES:
        mask = frame[c].to_numpy(int).astype(bool)
        est, truth = domain_estimate(p, mask, sel, y, pi_full)
        derr.append(abs(est - truth))
        cov, essd, _ = domain_uq_coverage(p, mask, sel, y, pi_full, Xs)
        dcov.append(cov); dess.append(essd)
    return {
        "seed": int(seed), "method": method, "n_selected": int(len(sel),
        "profile_estimate": prof["estimate"], "profile_error": prof["profile_error"],
        "critical_domain_error": float(np.mean(derr)), "difficult_case_hit": int(any(int(i) in difficult for i in sel)),
        "ess_all": prof["weight_ess"], "ess_probability_remainder": ess_probability_remainder(p, sel, pi_full),
        "min_pi_selected": prof["min_pi"], "max_normalized_weight": prof["max_normalized_weight"],
        "profile_uq_covered": prof["uq_covered"], "domain_uq_coverage_mean": float(np.mean(dcov)),
        "domain_min_ess_mean": float(np.mean(dess)),
        "balance_error": bal,
    }


def paired_summary(a, b):
    d = np.asarray(a, float) - np.asarray(b, float)
    m = float(d.mean()); se = float(d.std(ddof=1) / math.sqrt(len(d)))
    return {"n": len(d), "mean_diff": m, "ci_lo": m - 1.96 * se, "ci_hi": m + 1.96 * se, "median_diff": float(np.median(d))}


def evaluate(frame_path: Path, sa_path: Path, design_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    frame, strata, counts, alloc40, Xs, XAdv, p, h, phi, novelty, risk, _, _ = load_frame(frame_path)
    y = load_outcomes(sa_path, frame)
    difficult, cutoff = difficult_set(y)
    truth_profile = float(p @ y)
    truth_domains = {c: float(y[frame[c].to_numpy(int).astype(bool)].mean()) for c in CHALLENGE_FEATURES}
    design = json.loads(design_path.read_text(encoding="utf-8"))
    if design["finite_population_n"] != 120 or design["live_n"] != 40:
        raise RuntimeEror("design object contract mismatch")
    pi_ktes = np.array([float(design["cpktes_pi_by_sequence"][str(name()])) for name in frame.sequence_name], float)
    if np.any(pi_ktes <= 0):
        raise RuntimeEror("frozen design has nonpositive c-pKTES pi")

    rows = []; failures = []
    for seed in REPLAY_SEEDS:
        for method in ["c-pKTES-Hedge", "Stratified-SRS", "Split15+Audit25"]:
            try:
                rows.append(evaluate_method(method, int(seed), frame, strata, alloc40, Xs, XAdv, p, h, phi, novelty, risk, pi_ktes, design, y, difficult, truth_profile, truth_domains))
            except Exception as e:
                failures.append({"seed": int(seed), "method": method, "error": repr(e) })
    raw = pd.DataFrame(rows).sort_values(["seed", "method"]).reset_index(drop=True)
    raw_path = out_dir / "phase2a_500_replay_raw_v8.csv"
    raw.to_csv(raw_path, index=False)

    expected_rows = len(REPLAY_SEEDS) * 3
    if len(raw) != expected_rows:
        failure_path = out_dir / "phase2a_replay_failures_v8.json"
        failure_path.write_text(json.dumps(failures, indent=2) + "\n", encoding="utf-8")
        raise RuntimeErrop�f"replay rows {len(raw)} != {expected_rows}; failures={len(failures)}")

    summary_rows = []
    for method, d in raw.groupby("method"):
        summary_rows.append({
            "method": method,
            "n_replays": len(d),
            "profile_error_mean": float(d.profile_error.mean()),
            "profile_error_median": float(d.profile_error.median()),
            "critical_domain_error_mean": float(d.critical_domain_error.mean()),
            "critical_domain_error_median": float(d.critical_domain_error.median()),
            "difficult_case_hit_rate": float(d.difficult_case_hit.mean()),
            "ess_all_median": float(d.ess_all.median()),
            "ess_all_p05": float(d.ess_all.quantile(.05)),
            "ess_probability_remainder_median": float(d.ess_probability_remainder.median()),
            "ess_probability_remainder_p05": float(d.ess_probability_remainder.quantile(.05)),
            "min_pi_selected_min": float(d.min_pi_selected.min()),
            "max_normalized_weight_p95": float(d.max_normalized_weight.quantile(.95)),
            "profile_uq_coverage": float(d.profile_uq_covered.mean()),
            "domain_uq_coverage_mean": float(d.domain_uq_coverage_mean.mean()),
        })
    summary = pd.DataFrame(summary_rows).sort_values("method")
    summary_path = out_dir / "phase2a_500_replay_summary_v8.csv"
    summary.to_csv(summary_path, index=False)

    piv = {m: raw[raw.method == m].sort_values("seed").reset_index(drop=True) for m in raw.method.unique()}
    paired = []
    for metric in ["profile_error", "critical_domain_error", "difficult_case_hit", "ess_probability_remainder"]:
        for comp in ["Stratified-SRS", "Split15+Audit25"]:
            q = paired_summary(piv["c-pGTES-Hedge"][metric], piv[comp][metric])
            paired.append({"comparison": f"c-pGTES-Hedge - {comp}", "metric": metric, **q})
    paired_df = pd.DataFrame(paired)
    paired_path = out_dir / "phase2a_500_replay_paired_v8.csv"
    paired_df.to_csv(paired_path, index=False)

    sm = summary.set_index("method")
    k = sm.loc["c-pKTES-Hedge"]
    better_baseline = min(
        [("Stratified-SRS", sm.loc["Stratified-SRS", "critical_domain_error_mean"]),
         ("Split15+Audit25", sm.loc["Split15+Audit25", "critical_domain_error_mean"])],
        key=lambda x: x[1]
    )
    profile_diff = float(k.profile_error_mean - sm.loc["Stratified-SRS", "profile_error_mean"])
    crit_diff = float(k.critical_domain_error_mean - better_baseline[1])
    hit_diff = float(k.difficult_case_hit_rate - sm.loc["Split15+Audit25", "difficult_case_hit_rate"])
    gate = {
        "schema_version": "KTES-P2A-RESULT-GATE-v8.3",
        "design_object_sha256": sha256_file(design_path),
        "frame_sha256": sha256_file(frame_path),
        "sa_sha256": sha256_file(sa_path),
        "truth_profile_mean_SA": truth_profile,
        "bottom10_cutoff_SA": cutoff,
        "bottom10_n": 12,
        "challenge_domain_truths": truth_domains,
        "replays": 500,
        "guardrails": {
            "positive_pi_and_no_sampling_failure": {"value": len(failures) == 0 and bool(np.all(pi_ktes > 0)), "pass": len(failures) == 0 and bool(np.all(pi_ktes > 0))},
            "ktes_probability_remainder_ess_median_ge_18_5": {"value": float(k.ess_probability_remainder_median), "threshold": 18.5, "pass": bool(k.ess_probability_remainder_median >= 18.5)},
            "ktes_probability_remainder_ess_p05_ge_12": {"value": float(k.ess_probability_remainder_p05), "threshold": 12.0, "pass": bool(k.ess_probability_remainder_p05 >= 12.0)},
            "profile_error_not_worse_than_srs_by_gt_0_01": {"ktes_minus_srs": profile_diff, "threshold_max": 0.01, "pass": profile_diff <= 0.01},
            "critical_domain_error_not_worse_than_better_baseline_by_gt_0_02": {"better_baseline": better_baseline[0], "ktes_minus_better": crit_diff, "threshold_max": 0.02, "pass": crit_diff <= 0.02},
            "difficult_hit_not_below_split_by_gt_0_10": {"ktes_minus_split": hit_diff, "threshold_min": -0.10, "pass": hit_diff >= -0.10},
        },
        "secondary_uq_diagnostic": "profile and six-domain max(GS,PWR)-style coverage; not a pass/fail guardrail in the preregistered protocol",
        "split_adapter_note": design["external_adapter_mapping"]["split15"],
    }
    gate["overall_pass"] = all(v["pass"] for v in gate["guardrails"].values())
    gate_path = out_dir / "phase2a_result_gate_v8.json"
    gate_path.write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_md = out_dir / "PHASE2A_500_REPLAY_RESULT_v8.md"
    lines = [
        "# Phase 2A 500-paired-replay result v8",
        "",
        f"**Gate:** **{'PASS' if gate['overall_pass'] else 'FAIL'}**",
        "",
        f"Finite population: Anti-UAV410 official test split, N=120; primary outcome: SiamFC per-sequence State Accuracy; paired replay seeds: 20261001–20261500.",
        "",
        "## Method summaries",
        "",
        summary.to_markdown(index=False),
        "",
        "## Paired comparisons (c-pKTES-Hedge minus comparator)",
        "",
        paired_df.to_markdown(index=False),
        "",
        "## Frozen guardrails",
        "",
    ]
    for key, value in gate["guardrails"].items():
        lines.append(f"- `{key}`: **{'PASS' if value['pass'] else 'FAIL'}** — {json.dumps(value, ensure_ascii=False)}")
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "This gate evaluates structural transfer of the frozen probability-preserving sampling logic on a real task-effectiveness benchmark. It does not establish live-weapon validity, deployment-frequency representativeness, or mission-level safety certification.",
        "",
        "The split-style comparator uses the frozen historical deterministic 15-point geometry rule mapped to the four Phase 2A strata and a disjoint 25-point probability audit so that all methods consume exactly 40 unique sequence-level tests. This mapping is outcome-blind but was numerically instantiated after outcome recovery; the chronology is retained as an execution-order limitation rather than hidden.",
    ]
    result_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(summary.to_string(index=False))
    print("\nGATE", "PASS" if gate["overall_pass"] else "FAIL")
    print(json.dumps(gate["guardrails"], indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("freeze")
    p.add_argument("--frame", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("evaluate")
    p.add_argument("--frame", type=Path, required=True)
    p.add_argument("--sa", type=Path, required=True)
    p.add_argument("--design", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "freeze":
        write_design(a.frame, a.output)
    else:
        evaluate(a.frame, a.sa, a.design, a.out_dir)


if __name__ == "__main__":
    main()
