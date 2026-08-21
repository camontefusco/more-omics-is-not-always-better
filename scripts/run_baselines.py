#!/usr/bin/env python3
"""Run simple reproducible regression baselines on a prepared CSV table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error


def run(path: Path, target: str, group: str, features: list[str], seed: int = 20260821) -> dict[str, float | int | str]:
    frame = pd.read_csv(path)
    required = {target, group, *features} - set(frame.columns)
    if required:
        raise ValueError(f"missing columns: {sorted(required)}")
    frame = frame.dropna(subset=[target, group]).reset_index(drop=True)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    train_idx, test_idx = next(splitter.split(frame, groups=frame[group]))
    numeric = [column for column in features if pd.api.types.is_numeric_dtype(frame[column])]
    if not numeric:
        raise ValueError("at least one numeric feature is required")
    pipeline = Pipeline([
        ("impute_scale", Pipeline([( "impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])),
        ("model", Ridge(alpha=1.0)),
    ])
    pipeline.fit(frame.loc[train_idx, numeric], frame.loc[train_idx, target])
    prediction = pipeline.predict(frame.loc[test_idx, numeric])
    observed = frame.loc[test_idx, target]
    return {
        "model": "ridge",
        "target": target,
        "group": group,
        "features": ",".join(numeric),
        "train_rows": int(len(train_idx)),
        "test_rows": int(len(test_idx)),
        "mae": float(mean_absolute_error(observed, prediction)),
        "rmse": float(mean_squared_error(observed, prediction) ** 0.5),
        "seed": seed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("--target", default="response_value")
    parser.add_argument("--group", default="cell_line_id_raw")
    parser.add_argument("--features", nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.table, args.target, args.group, args.features)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
