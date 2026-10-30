"""Historical statistical definitions extracted from project code (MIT).
Source files and SHA-256 records: provenance/recovered_sources.json.
No experiment runner or serving engine is imported.
"""
from __future__ import annotations
import math
from typing import Any
from types import SimpleNamespace
import numpy as np
import pandas as pd
BOOTSTRAP_B=2000
BOOTSTRAP_SEED=20270225
FDR_Q=0.10
hg=SimpleNamespace(BOOTSTRAP_B=2000, BOOTSTRAP_SEED=3108260827, NULL_EPS=1e-6, FDR_Q=0.10, PAIRWISE_PRIORITY_FAIRNESS_ID='fdbca4434f9e')
def ci_mean_instances(
    values: np.ndarray,
    *,
    seed: int = BOOTSTRAP_SEED,
    b: int = BOOTSTRAP_B,
) -> tuple[float, float, float]:
    """Percentile bootstrap CI for the mean of instance-level values."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return math.nan, math.nan, math.nan
    rng = np.random.default_rng(seed)
    means = np.empty(b)
    n = len(values)
    for i in range(b):
        means[i] = float(np.mean(values[rng.integers(0, n, n)]))
    return float(np.mean(values)), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))

def permutation_p_instances(
    x: np.ndarray,
    y: np.ndarray,
    *,
    seed: int = BOOTSTRAP_SEED,
    b: int = BOOTSTRAP_B,
) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    if len(x) == 0 or len(y) == 0:
        return math.nan
    obs = abs(float(np.mean(y) - np.mean(x)))
    pooled0 = np.concatenate([x, y])
    n = len(x)
    rng = np.random.default_rng(seed)
    hits = 1
    for _ in range(b):
        pooled = pooled0.copy()
        rng.shuffle(pooled)
        stat = abs(float(np.mean(pooled[n:]) - np.mean(pooled[:n])))
        hits += int(stat >= obs - 1e-15)
    return hits / (b + 1)

def bh_qvalues(pvals: list[float], q: float = FDR_Q) -> list[float]:
    """Benjamini-Hochberg q-values. `q` retained for API clarity; procedure is BH."""
    del q  # threshold applied by callers comparing q-values to FDR_Q
    arr = np.asarray([1.0 if not np.isfinite(p) else float(p) for p in pvals], dtype=float)
    n = len(arr)
    if n == 0:
        return []
    order = np.argsort(arr)
    out = np.empty(n)
    prev = 1.0
    for rev_rank, idx in enumerate(order[::-1], start=1):
        k = n - rev_rank + 1
        val = min(prev, arr[idx] * n / max(k, 1))
        out[idx] = val
        prev = val
    return [float(v) for v in out]

def ci_excludes_zero(lo: float, hi: float) -> bool:
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return False
    return (lo > 0.0) or (hi < 0.0)
def bootstrap_two_sided_p(
    values: np.ndarray,
    *,
    seed: int = BOOTSTRAP_SEED,
    b: int = BOOTSTRAP_B,
) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return math.nan
    obs = float(np.mean(values))
    rng = np.random.default_rng(seed)
    n = len(values)
    boots = np.empty(b)
    for i in range(b):
        boots[i] = float(np.mean(values[rng.integers(0, n, n)]))
    if obs >= 0:
        return float(min(1.0, 2.0 * np.mean(boots <= 0.0)))
    return float(min(1.0, 2.0 * np.mean(boots >= 0.0)))
def _ci_dict(values: np.ndarray, *, seed: int = hg.BOOTSTRAP_SEED) -> dict[str, Any]:
    mean, lo, hi = ci_mean_instances(values, seed=seed, b=hg.BOOTSTRAP_B)
    p = bootstrap_two_sided_p(values, seed=seed, b=hg.BOOTSTRAP_B)
    return {"mean": mean, "ci_low": lo, "ci_high": hi, "ci_excludes_zero": ci_excludes_zero(lo, hi), "bootstrap_p": p}

def _status_from_relationship(r: float, *, direction_positive: bool, ci_signal: bool) -> str:
    if not np.isfinite(r):
        return "NO_GENERALIZATION"
    if direction_positive and r > 0.35 and ci_signal:
        return "STRONG_GENERALIZATION"
    if direction_positive and r > 0.0:
        return "PARTIAL_GENERALIZATION"
    if direction_positive and r < -0.35:
        return "CONTRADICTED"
    return "NO_GENERALIZATION"

def priority_generalization(single_df: pd.DataFrame, div_df: pd.DataFrame, probes: pd.DataFrame) -> dict[str, Any]:
    sub = single_df[(single_df["family"].isin(["priority", "priority_fairness"])) & (single_df["module_type"] == "priority")]
    inst = sub.groupby(["config_id", "cell_id"], dropna=False).agg(
        mean_abs_delta_anwg=("abs_delta_anwg", "mean"),
        mean_delta_anwg=("delta_anwg", "mean"),
        mean_abs_delta_slo=("delta_num_slo_violated", lambda s: float(np.mean(np.abs(s)))),
    ).reset_index()
    div_inst = div_df[div_df["module_type"] == "priority"].groupby("config_id").agg(
        decision_divergence_rate=("decision_divergence_rate", "mean"),
        request_change_rate=("fraction_requests_completion_time_changed", "mean"),
    ).reset_index()
    merged = inst.merge(div_inst, on="config_id", how="left").merge(
        probes[["config_id", "candidate_set_ge2_fraction", "priority_rank_disagreement_fraction", "priority_top_choice_disagreement_fraction", "potential_decision_divergence_rate"]],
        on="config_id",
        how="left",
    )
    out: dict[str, Any] = {"instance_table": merged.to_dict(orient="records")}
    contrasts = []
    for cell, g in merged.groupby("cell_id"):
        vals = g["decision_divergence_rate"].to_numpy(dtype=float)
        abs_vals = g["mean_abs_delta_anwg"].to_numpy(dtype=float)
        contrasts.append({
            "cell_id": cell,
            "n_instances": int(len(g)),
            "decision_divergence": _ci_dict(vals),
            "mean_abs_delta_anwg": _ci_dict(abs_vals),
            "candidate_set_ge2_mean": float(g["candidate_set_ge2_fraction"].mean()),
            "rank_disagreement_mean": float(g["priority_rank_disagreement_fraction"].mean()),
        })
    out["by_cell"] = contrasts
    for x, y in [
        ("candidate_set_ge2_fraction", "decision_divergence_rate"),
        ("priority_rank_disagreement_fraction", "decision_divergence_rate"),
        ("decision_divergence_rate", "request_change_rate"),
        ("decision_divergence_rate", "mean_abs_delta_anwg"),
    ]:
        mask = np.isfinite(merged[x].to_numpy(dtype=float)) & np.isfinite(merged[y].to_numpy(dtype=float))
        if mask.sum() >= 3:
            out[f"pearson_{x}_vs_{y}"] = float(np.corrcoef(merged.loc[mask, x], merged.loc[mask, y])[0, 1])
    low = merged[merged["cell_id"] == "hg_prio_low_opportunity"]["decision_divergence_rate"].to_numpy(dtype=float)
    high = merged[merged["cell_id"].isin(["hg_prio_mid_opportunity", "hg_prio_high_opportunity"])]["decision_divergence_rate"].to_numpy(dtype=float)
    out["low_vs_higher_opportunity_divergence_permutation_p"] = permutation_p_instances(low, high, seed=hg.BOOTSTRAP_SEED, b=hg.BOOTSTRAP_B)
    out["status"] = _status_from_relationship(
        out.get("pearson_candidate_set_ge2_fraction_vs_decision_divergence_rate", math.nan),
        direction_positive=True,
        ci_signal=bool(np.nanmean(high) > np.nanmean(low)) if len(low) and len(high) else False,
    )
    return out

def priority_fairness_generalization(pairwise_df: pd.DataFrame, probes: pd.DataFrame) -> dict[str, Any]:
    if pairwise_df.empty:
        return {"status": "NO_GENERALIZATION", "reason": "no pairwise rows"}
    g = pairwise_df[pairwise_df["pairwise_id"] == hg.PAIRWISE_PRIORITY_FAIRNESS_ID]
    inst_i = g.groupby("config_id")["interaction"].mean().to_numpy()
    i = _ci_dict(inst_i)
    i["bh_q"] = bh_qvalues([i["bootstrap_p"]])[0] if np.isfinite(i["bootstrap_p"]) else 1.0
    seed_i = g.groupby("seed")["interaction"].mean()
    mean_i = i["mean"]
    seed_same = int(np.sum(np.sign(seed_i) == np.sign(mean_i))) if np.isfinite(mean_i) and abs(mean_i) > hg.NULL_EPS else 0
    p_probe = probes[probes["cell_id"] == "hg_prio_high_opportunity"]
    pf_probe = probes[probes["cell_id"] == "hg_prio_fair_interaction"]
    fairness_shift = {
        "candidate_set_ge2_delta_vs_high_priority_cell": float(pf_probe["candidate_set_ge2_fraction"].mean() - p_probe["candidate_set_ge2_fraction"].mean()) if len(p_probe) and len(pf_probe) else math.nan,
        "rank_disagreement_delta_vs_high_priority_cell": float(pf_probe["priority_rank_disagreement_fraction"].mean() - p_probe["priority_rank_disagreement_fraction"].mean()) if len(p_probe) and len(pf_probe) else math.nan,
        "promotion_opportunity_fraction": float(pf_probe["promotion_opportunity_fraction"].mean()) if len(pf_probe) else math.nan,
    }
    if i["ci_excludes_zero"] and seed_same >= 4:
        status = "STRONG_GENERALIZATION"
    elif np.isfinite(mean_i) and abs(mean_i) > hg.NULL_EPS:
        status = "PARTIAL_GENERALIZATION"
    else:
        status = "NO_GENERALIZATION"
    return {
        "pairwise_id": hg.PAIRWISE_PRIORITY_FAIRNESS_ID,
        "n_instances": int(len(inst_i)),
        "interaction": i,
        "seed_same_sign_count": seed_same,
        "seed_total": int(len(seed_i)),
        "per_seed_interaction": {int(k): float(v) for k, v in seed_i.items()},
        "fairness_opportunity_shift": fairness_shift,
        "status": status,
    }

def kv_guard_generalization(single_df: pd.DataFrame) -> dict[str, Any]:
    sub = single_df[single_df["family"] == "kv_guard"]
    inst = sub.groupby(["config_id", "cell_id", "kv_pressure_index"], dropna=False).agg(
        mean_delta_anwg=("delta_anwg", "mean"),
        mean_abs_delta_anwg=("abs_delta_anwg", "mean"),
    ).reset_index()
    by_pressure = []
    for idx, g in inst.groupby("kv_pressure_index"):
        vals = g["mean_delta_anwg"].to_numpy(dtype=float)
        abs_vals = g["mean_abs_delta_anwg"].to_numpy(dtype=float)
        by_pressure.append({
            "kv_pressure_index": int(idx),
            "n_instances": int(len(g)),
            "delta_anwg": _ci_dict(vals),
            "abs_delta_anwg": _ci_dict(abs_vals),
        })
    xs = inst["kv_pressure_index"].to_numpy(dtype=float)
    ys = inst["mean_abs_delta_anwg"].to_numpy(dtype=float)
    r = float(np.corrcoef(xs, ys)[0, 1]) if len(inst) >= 3 and np.std(xs) > 0 and np.std(ys) > 0 else math.nan
    low = inst[inst["kv_pressure_index"] == 0]["mean_abs_delta_anwg"].to_numpy(dtype=float)
    high = inst[inst["kv_pressure_index"] >= 1]["mean_abs_delta_anwg"].to_numpy(dtype=float)
    p = permutation_p_instances(low, high, seed=hg.BOOTSTRAP_SEED, b=hg.BOOTSTRAP_B)
    seed_vals = sub.groupby("seed")["delta_anwg"].mean()
    mean_delta = float(seed_vals.mean()) if len(seed_vals) else math.nan
    seed_same = int(np.sum(np.sign(seed_vals) == np.sign(mean_delta))) if abs(mean_delta) > hg.NULL_EPS else 0
    if np.isfinite(r) and r > 0.25 and np.nanmean(high) > np.nanmean(low):
        status = "STRONG_GENERALIZATION" if p < 0.10 else "PARTIAL_GENERALIZATION"
    elif np.isfinite(r) and r < -0.25:
        status = "CONTRADICTED"
    else:
        status = "NO_GENERALIZATION"
    return {
        "by_pressure": by_pressure,
        "instance_table": inst.to_dict(orient="records"),
        "pearson_pressure_index_vs_abs_delta_anwg": r,
        "low_vs_higher_pressure_abs_delta_permutation_p": p,
        "seed_same_sign_count": seed_same,
        "seed_total": int(len(seed_vals)),
        "kv_guard_corrected_activation": True,
        "status": status,
    }

def prefill_generalization(single_df: pd.DataFrame, div_df: pd.DataFrame, probes: pd.DataFrame) -> dict[str, Any]:
    sub = single_df[(single_df["family"] == "prefill") & (single_df["module_type"] == "prefill")]
    div = div_df[div_df["module_type"] == "prefill"]
    inst = sub.groupby(["config_id", "cell_id"], dropna=False).agg(
        mean_delta_anwg=("delta_anwg", "mean"),
        mean_abs_delta_anwg=("abs_delta_anwg", "mean"),
    ).reset_index()
    div_inst = div.groupby("config_id").agg(
        decision_divergence_rate=("decision_divergence_rate", "mean"),
        request_change_rate=("fraction_requests_completion_time_changed", "mean"),
        median_abs_completion_time_diff=("median_abs_completion_time_diff", "mean"),
    ).reset_index()
    merged = inst.merge(div_inst, on="config_id", how="left").merge(
        probes[["config_id", "pressure_ge_threshold_fraction", "prefill_candidate_filter_disagreement_fraction", "prefill_action_divergence_fraction"]],
        on="config_id",
        how="left",
    )
    by_cell = []
    for cell, g in merged.groupby("cell_id"):
        by_cell.append({
            "cell_id": cell,
            "n_instances": int(len(g)),
            "decision_divergence": _ci_dict(g["decision_divergence_rate"].to_numpy(dtype=float)),
            "request_change": _ci_dict(g["request_change_rate"].to_numpy(dtype=float)),
            "mean_abs_delta_anwg": _ci_dict(g["mean_abs_delta_anwg"].to_numpy(dtype=float)),
            "pressure_ge_threshold_mean": float(g["pressure_ge_threshold_fraction"].mean()),
        })
    inactive = merged[merged["cell_id"] == "hg_prefill_inactive"]["decision_divergence_rate"].to_numpy(dtype=float)
    active = merged[merged["cell_id"] == "hg_prefill_active"]["decision_divergence_rate"].to_numpy(dtype=float)
    p = permutation_p_instances(inactive, active, seed=hg.BOOTSTRAP_SEED, b=hg.BOOTSTRAP_B)
    if len(active) and np.nanmean(active) > np.nanmean(inactive):
        status = "PARTIAL_GENERALIZATION" if p >= 0.10 else "STRONG_GENERALIZATION"
    else:
        status = "NO_GENERALIZATION"
    return {"by_cell": by_cell, "instance_table": merged.to_dict(orient="records"), "active_vs_inactive_divergence_permutation_p": p, "status": status}
