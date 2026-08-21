#!/usr/bin/env python3
"""Summarize per-drug and seed-level secondary benchmark diagnostics."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
seeds = ["20260821", "20260822", "20260823", "20260824", "20260825"]
results = [json.loads((ROOT / f"data/processed/full_universe_{s}.json").read_text()) for s in seeds]

seed_rows = []
for d in results:
    e = d["metrics"]["expression"]
    f = d["metrics"]["fusion"]
    b = d["metrics"]["mean_response"]
    seed_rows.append({"seed": d["seed"], "expression_rmse": e["rmse"], "fusion_rmse": f["rmse"], "mean_response_rmse": b["rmse"], "fusion_delta_rmse": f["rmse"] - e["rmse"], "fusion_vs_mean_delta_rmse": f["rmse"] - b["rmse"]})

per_drug = {}
for d in results:
    for drug, models in d["per_drug"].items():
        row = per_drug.setdefault(drug, {"seeds": []})
        e, f, b = models["expression"], models["fusion"], models["mean_response"]
        row["seeds"].append({"seed": d["seed"], "n": e["n"], "expression_rmse": e["rmse"], "fusion_rmse": f["rmse"], "mean_response_rmse": b["rmse"], "fusion_delta_rmse": f["rmse"] - e["rmse"], "fusion_vs_mean_delta_rmse": f["rmse"] - b["rmse"]})
    
for drug, row in per_drug.items():
    deltas = [x["fusion_delta_rmse"] for x in row["seeds"]]
    row["n_seeds"] = len(deltas)
    row["mean_fusion_delta_rmse"] = float(np.mean(deltas))
    row["fusion_help_count"] = int(sum(x < 0 for x in deltas))
    row["fusion_harm_count"] = int(sum(x > 0 for x in deltas))

all_deltas = [x["fusion_delta_rmse"] for row in per_drug.values() for x in row["seeds"]]
out = {"seed_rows": seed_rows, "per_drug": per_drug, "summary": {"drug_seed_cells": len(all_deltas), "fusion_help_cells": int(sum(x < 0 for x in all_deltas)), "fusion_harm_cells": int(sum(x > 0 for x in all_deltas)), "fusion_help_fraction": float(np.mean(np.array(all_deltas) < 0))}}
(ROOT / "data/processed/full_universe_secondary_summary.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out["summary"], indent=2))
