#!/usr/bin/env python3
"""Run fold-local feature selection and drug-held-out Ridge benchmarks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def run(path: Path, top_k: int, seed: int, split_output: Path | None = None) -> dict[str, object]:
    frame = pd.read_csv(path).dropna(subset=["response_value", "drug_id_raw"]).reset_index(drop=True)
    groups = frame["drug_id_raw"].astype(str)
    train_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(frame, groups=groups))
    if split_output:
        split_output.parent.mkdir(parents=True, exist_ok=True)
        split_output.write_text(json.dumps({"seed": seed, "train_drugs": sorted(groups.iloc[train_idx].unique().tolist()), "test_drugs": sorted(groups.iloc[test_idx].unique().tolist())}, indent=2) + "\n")
    modality_cols = {name: [c for c in frame if c.startswith(prefix)] for name, prefix in [("expression", "expression__"), ("copy_number", "copy_number__"), ("mutation", "mutation__")]}
    selected = {}
    for name, cols in modality_cols.items():
        numeric = frame.loc[train_idx, cols].apply(pd.to_numeric, errors="coerce")
        selected[name] = numeric.var(axis=0, skipna=True).fillna(0).nlargest(min(top_k, len(cols))).index.tolist()
    selected["fusion"] = selected["expression"] + selected["copy_number"] + selected["mutation"]
    observed = frame.loc[test_idx, "response_value"]
    predictions = {}
    for name, cols in selected.items():
        model = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("model", Ridge(alpha=1.0))])
        model.fit(frame.loc[train_idx, cols], frame.loc[train_idx, "response_value"])
        predictions[name] = model.predict(frame.loc[test_idx, cols])
    metrics = {}
    modality_available = {
        name: frame.loc[test_idx, cols].notna().any(axis=1)
        for name, cols in ((name, selected[name]) for name in ("expression", "copy_number", "mutation"))
    }
    missing_stratum = modality_available["expression"] & modality_available["copy_number"] & modality_available["mutation"]
    for name, pred in predictions.items():
        metrics[name] = {"mae": float(mean_absolute_error(observed, pred)), "rmse": float(mean_squared_error(observed, pred) ** 0.5), "feature_count": len(selected[name])}
        metrics[name]["complete_case_rows"] = int(missing_stratum.sum())
        metrics[name]["missing_case_rows"] = int((~missing_stratum).sum())
    return {"seed": seed, "train_drug_count": int(groups.iloc[train_idx].nunique()), "test_drug_count": int(groups.iloc[test_idx].nunique()), "metrics": metrics, "selected_features": {k: len(v) for k, v in selected.items()}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("--top-k", type=int, default=2000)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split-output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.table, args.top_k, args.seed, args.split_output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
