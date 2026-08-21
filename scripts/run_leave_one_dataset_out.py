#!/usr/bin/env python3
"""Run dataset-held-out Ridge benchmarks with training-only feature selection."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


MODALITY_PREFIXES = {
    "expression": "expression__",
    "copy_number": "copy_number__",
    "mutation": "mutation__",
}


def fit_metrics(train: pd.DataFrame, test: pd.DataFrame, columns: list[str]) -> dict[str, float | int]:
    model = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
        ("model", Ridge(alpha=1.0)),
    ])
    model.fit(train[columns], train["response_value"])
    prediction = model.predict(test[columns])
    observed = test["response_value"]
    return {
        "mae": float(mean_absolute_error(observed, prediction)),
        "rmse": float(mean_squared_error(observed, prediction) ** 0.5),
        "feature_count": len(columns),
    }


def run(path: Path, top_k: int, seed: int) -> dict[str, object]:
    frame = pd.read_csv(path).dropna(subset=["response_value", "dataset_id"]).reset_index(drop=True)
    frame["dataset_id"] = frame["dataset_id"].astype(str)
    datasets = sorted(frame["dataset_id"].unique().tolist())
    results: dict[str, object] = {"seed": seed, "top_k": top_k, "datasets": datasets, "folds": {}}

    for held_out in datasets:
        train = frame[frame["dataset_id"] != held_out].copy()
        test = frame[frame["dataset_id"] == held_out].copy()
        selected: dict[str, list[str]] = {}
        for name, prefix in MODALITY_PREFIXES.items():
            columns = [c for c in frame.columns if c.startswith(prefix)]
            variance = train[columns].apply(pd.to_numeric, errors="coerce").var(axis=0, skipna=True).fillna(0.0)
            selected[name] = variance.nlargest(min(top_k, len(columns))).index.tolist()
        selected["fusion"] = selected["expression"] + selected["copy_number"] + selected["mutation"]

        complete_case = np.ones(len(test), dtype=bool)
        for name in MODALITY_PREFIXES:
            complete_case &= test[selected[name]].notna().any(axis=1).to_numpy()
        fold_metrics = {}
        for name, columns in selected.items():
            fold_metrics[name] = fit_metrics(train, test, columns)
            fold_metrics[name]["complete_case_rows"] = int(complete_case.sum())
            fold_metrics[name]["missing_case_rows"] = int((~complete_case).sum())
        results["folds"][held_out] = {
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
            "train_datasets": sorted(train["dataset_id"].unique().tolist()),
            "metrics": fold_metrics,
        }
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("--top-k", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.table, args.top_k, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
