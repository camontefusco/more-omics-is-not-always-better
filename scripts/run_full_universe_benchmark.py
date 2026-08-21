#!/usr/bin/env python3
"""Run drug-held-out Ridge benchmarks with selection from full raw modalities.

This runner intentionally bypasses the prepared 2,000-feature candidate tables.
Feature ranking is performed inside each split on the full raw modality matrices.
"""
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


def load_modality(path: Path, prefix: str, ids: set[str]) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["depmap_id"] = frame["depmap_id"].astype(str)
    frame = frame[frame["depmap_id"].isin(ids)].copy()
    feature_cols = [c for c in frame.columns if c != "depmap_id" and not c.startswith("lineage_") and c not in {"cell_line_display_name"}]
    frame = frame[["depmap_id"] + feature_cols]
    frame = frame.rename(columns={c: f"{prefix}{c}" for c in feature_cols})
    if frame["depmap_id"].duplicated().any():
        raise ValueError(f"duplicate depmap_id values in {path}")
    return frame.set_index("depmap_id")


def run(response_path: Path, raw_paths: dict[str, Path], output: Path, manifest_dir: Path, seed: int, top_k: int) -> dict[str, object]:
    response = pd.read_csv(response_path)
    response = response.dropna(subset=["response_value", "drug_id_raw"]).copy()
    response["depmap_id"] = response["depmap_id"].astype(str)
    ids = set(response["depmap_id"])
    modalities = {name: load_modality(path, f"{name}__", ids) for name, path in raw_paths.items()}
    frame = response[["depmap_id", "drug_id_raw", "dataset_id", "response_value"]].reset_index(drop=True)
    groups = frame["drug_id_raw"].astype(str)
    train_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(frame, groups=groups))
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"seed": seed, "top_k": top_k, "train_drugs": sorted(groups.iloc[train_idx].unique()), "test_drugs": sorted(groups.iloc[test_idx].unique()), "response_rows": len(frame), "raw_feature_counts": {k: int(v.shape[1]) for k, v in modalities.items()}}
    (manifest_dir / f"full_universe_drug_split_{seed}.json").write_text(json.dumps(manifest, indent=2) + "\n")

    selected: dict[str, list[str]] = {}
    train_ids = frame.iloc[train_idx]["depmap_id"].to_numpy()
    test_ids = frame.iloc[test_idx]["depmap_id"].to_numpy()
    for name, matrix in modalities.items():
        train_matrix = matrix.reindex(train_ids)
        variance = train_matrix.apply(pd.to_numeric, errors="coerce").var(axis=0, skipna=True).fillna(0.0)
        selected[name] = variance.nlargest(min(top_k, len(variance))).index.tolist()
    selected["fusion"] = selected["expression"] + selected["copy_number"] + selected["mutation"]
    (manifest_dir / f"full_universe_features_{seed}.json").write_text(json.dumps({k: v for k, v in selected.items()}, indent=2) + "\n")

    y_train = frame.iloc[train_idx]["response_value"].to_numpy()
    y_test = frame.iloc[test_idx]["response_value"].to_numpy()
    metrics: dict[str, object] = {}
    per_drug: dict[str, dict[str, dict[str, float]]] = {}
    baseline_prediction = float(np.mean(y_train))
    baseline_pred = np.full_like(y_test, baseline_prediction, dtype=float)
    metrics["mean_response"] = {"mae": float(mean_absolute_error(y_test, baseline_pred)), "rmse": float(mean_squared_error(y_test, baseline_pred) ** 0.5), "feature_count": 0}
    for drug in sorted(frame.iloc[test_idx]["drug_id_raw"].astype(str).unique()):
        per_drug[drug] = {}
    for name, cols in selected.items():
        blocks = []
        for modality in ("expression", "copy_number", "mutation"):
            if name == modality:
                blocks = [modalities[modality].reindex(columns=cols).reindex(train_ids), modalities[modality].reindex(columns=cols).reindex(test_ids)]
                break
        if name == "fusion":
            train_x = pd.concat([modalities[m].reindex(columns=selected[m]).reindex(train_ids) for m in ("expression", "copy_number", "mutation")], axis=1)
            test_x = pd.concat([modalities[m].reindex(columns=selected[m]).reindex(test_ids) for m in ("expression", "copy_number", "mutation")], axis=1)
        else:
            train_x, test_x = blocks
        model = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("model", Ridge(alpha=1.0))])
        model.fit(train_x, y_train)
        prediction = model.predict(test_x)
        metrics[name] = {"mae": float(mean_absolute_error(y_test, prediction)), "rmse": float(mean_squared_error(y_test, prediction) ** 0.5), "feature_count": len(cols)}
        test_drugs = frame.iloc[test_idx]["drug_id_raw"].astype(str).to_numpy()
        for drug in per_drug:
            mask = test_drugs == drug
            if mask.any():
                per_drug[drug][name] = {"n": int(mask.sum()), "mae": float(mean_absolute_error(y_test[mask], prediction[mask])), "rmse": float(mean_squared_error(y_test[mask], prediction[mask]) ** 0.5)}
    test_drugs = frame.iloc[test_idx]["drug_id_raw"].astype(str).to_numpy()
    for drug in per_drug:
        mask = test_drugs == drug
        per_drug[drug]["mean_response"] = {"n": int(mask.sum()), "mae": float(mean_absolute_error(y_test[mask], baseline_pred[mask])), "rmse": float(mean_squared_error(y_test[mask], baseline_pred[mask]) ** 0.5)}
    result = {"seed": seed, "top_k": top_k, "candidate_source": "full_raw_modality_tables", "metrics": metrics, "per_drug": per_drug, "raw_feature_counts": {k: int(v.shape[1]) for k, v in modalities.items()}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--expression", type=Path, required=True)
    parser.add_argument("--copy-number", type=Path, required=True)
    parser.add_argument("--mutation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--top-k", type=int, default=2000)
    args = parser.parse_args()
    result = run(args.response, {"expression": args.expression, "copy_number": args.copy_number, "mutation": args.mutation}, args.output, args.manifest_dir, args.seed, args.top_k)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
