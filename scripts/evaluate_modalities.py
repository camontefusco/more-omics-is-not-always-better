#!/usr/bin/env python3
"""Compare modality-specific Ridge models on one shared grouped split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def evaluate(path: Path, target: str, group: str, modalities: dict[str, list[str]], seed: int = 20260821) -> dict[str, object]:
    frame = pd.read_csv(path).dropna(subset=[target, group]).reset_index(drop=True)
    missing = {feature for features in modalities.values() for feature in features} - set(frame.columns)
    if missing:
        raise ValueError(f"missing feature columns: {sorted(missing)}")
    train_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(frame, groups=frame[group]))
    observed = frame.loc[test_idx, target]
    scores: dict[str, dict[str, float | int]] = {}
    for name, features in modalities.items():
        pipeline = Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("model", Ridge(alpha=1.0)),
        ])
        pipeline.fit(frame.loc[train_idx, features], frame.loc[train_idx, target])
        prediction = pipeline.predict(frame.loc[test_idx, features])
        scores[name] = {
            "mae": float(mean_absolute_error(observed, prediction)),
            "rmse": float(mean_squared_error(observed, prediction) ** 0.5),
            "feature_count": len(features),
        }
    baseline = scores[next(iter(scores))]["rmse"]
    deltas = {name: float(score["rmse"] - baseline) for name, score in scores.items()}
    return {"seed": seed, "group": group, "target": target, "scores": scores, "rmse_delta_vs_first": deltas}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("--modalities", required=True, help='JSON object, e.g. \'{"expression":["expr_1"],"fusion":["expr_1","mut_1"]}\'')
    parser.add_argument("--target", default="response_value")
    parser.add_argument("--group", default="cell_line_id_raw")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(args.table, args.target, args.group, json.loads(args.modalities))
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
