#!/usr/bin/env python3
"""Run leave-one-dataset-out Ridge benchmarks from full raw modality tables."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from run_full_universe_benchmark import load_modality


def run(response_path: Path, raw_paths: dict[str, Path], output: Path, manifest_dir: Path, top_k: int) -> dict:
    response = pd.read_csv(response_path).dropna(subset=["response_value", "dataset_id"]).copy()
    response["depmap_id"] = response["depmap_id"].astype(str)
    ids = set(response["depmap_id"])
    matrices = {n: load_modality(p, f"{n}__", ids) for n, p in raw_paths.items()}
    results = {"top_k": top_k, "candidate_source": "full_raw_modality_tables", "raw_feature_counts": {k: int(v.shape[1]) for k, v in matrices.items()}, "folds": {}}
    manifest_dir.mkdir(parents=True, exist_ok=True)
    for held_out in sorted(response["dataset_id"].astype(str).unique()):
        train = response[response["dataset_id"].astype(str) != held_out].reset_index(drop=True)
        test = response[response["dataset_id"].astype(str) == held_out].reset_index(drop=True)
        selected = {}
        for name, matrix in matrices.items():
            train_matrix = matrix.reindex(train["depmap_id"])
            variance = train_matrix.apply(pd.to_numeric, errors="coerce").var(axis=0, skipna=True).fillna(0.0)
            selected[name] = variance.nlargest(min(top_k, len(variance))).index.tolist()
        selected["fusion"] = selected["expression"] + selected["copy_number"] + selected["mutation"]
        (manifest_dir / f"full_universe_lood_features_{held_out}.json").write_text(json.dumps(selected, indent=2) + "\n")
        fold_metrics = {}
        for name, cols in selected.items():
            if name == "fusion":
                train_x = pd.concat([matrices[m].reindex(columns=selected[m]).reindex(train["depmap_id"]) for m in ("expression", "copy_number", "mutation")], axis=1)
                test_x = pd.concat([matrices[m].reindex(columns=selected[m]).reindex(test["depmap_id"]) for m in ("expression", "copy_number", "mutation")], axis=1)
            else:
                train_x = matrices[name].reindex(columns=cols).reindex(train["depmap_id"])
                test_x = matrices[name].reindex(columns=cols).reindex(test["depmap_id"])
            model = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("model", Ridge(alpha=1.0))])
            model.fit(train_x, train["response_value"])
            pred = model.predict(test_x)
            fold_metrics[name] = {"mae": float(mean_absolute_error(test["response_value"], pred)), "rmse": float(mean_squared_error(test["response_value"], pred) ** 0.5), "feature_count": len(cols)}
        results["folds"][held_out] = {"train_rows": len(train), "test_rows": len(test), "metrics": fold_metrics}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n")
    return results


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--response", type=Path, required=True); p.add_argument("--expression", type=Path, required=True); p.add_argument("--copy-number", type=Path, required=True); p.add_argument("--mutation", type=Path, required=True); p.add_argument("--output", type=Path, required=True); p.add_argument("--manifest-dir", type=Path, required=True); p.add_argument("--top-k", type=int, default=2000)
    a = p.parse_args(); print(json.dumps(run(a.response, {"expression": a.expression, "copy_number": a.copy_number, "mutation": a.mutation}, a.output, a.manifest_dir, a.top_k), indent=2)); return 0

if __name__ == "__main__": raise SystemExit(main())
