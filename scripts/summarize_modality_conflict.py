#!/usr/bin/env python3
"""Summarize fusion-versus-expression disagreement across frozen folds."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lood", type=Path, required=True)
    parser.add_argument("--drug-results", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    lood = json.loads(args.lood.read_text())
    rows = []
    for dataset, fold in lood["folds"].items():
        e = fold["metrics"]["expression"]["rmse"]
        f = fold["metrics"]["fusion"]["rmse"]
        rows.append({"validation": "leave_one_dataset_out", "held_out": dataset, "expression_rmse": e, "fusion_rmse": f, "fusion_delta_rmse": f - e, "outcome": "helps" if f < e else "harms"})
    for path in args.drug_results:
        result = json.loads(path.read_text())
        e = result["metrics"]["expression"]["rmse"]
        f = result["metrics"]["fusion"]["rmse"]
        rows.append({"validation": "drug_heldout", "held_out": str(result["seed"]), "expression_rmse": e, "fusion_rmse": f, "fusion_delta_rmse": f - e, "outcome": "helps" if f < e else "harms"})
    summary = {"rows": rows, "help_count": sum(r["outcome"] == "helps" for r in rows), "harm_count": sum(r["outcome"] == "harms" for r in rows), "interpretation": "Fusion effects are conditional when the sign of fusion_delta_rmse varies across held-out folds."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
