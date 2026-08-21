#!/usr/bin/env python3
"""Evaluate simple feature masking and residual-based prediction intervals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def evaluate(path: Path, target: str, group: str | None, features: list[str], mask_fraction: float = 0.25, seed: int = 20260821) -> dict[str, float | int | str]:
    frame = pd.read_csv(path)
    if group is None:
        group = next((candidate for candidate in ("depmap_id", "cell_line_id_raw") if candidate in frame.columns), None)
    if group is None:
        raise ValueError("no grouping column found; expected depmap_id or cell_line_id_raw")
    frame = frame.dropna(subset=[target, group]).reset_index(drop=True)
    missing = set(features) - set(frame.columns)
    if missing:
        raise ValueError(f"missing feature columns: {sorted(missing)}")
    train_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(frame, groups=frame[group]))
    fit_idx, calibration_idx = next(
        GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed + 1).split(
            frame.loc[train_idx], groups=frame.loc[train_idx, group]
        )
    )
    fit_idx = train_idx[fit_idx]
    calibration_idx = train_idx[calibration_idx]
    rng = np.random.default_rng(seed)
    fit = frame.loc[fit_idx, features].astype(float).copy()
    calibration = frame.loc[calibration_idx, features].astype(float).copy()
    test = frame.loc[test_idx, features].astype(float).copy()
    calibration.values[rng.random(calibration.shape) < mask_fraction] = np.nan
    test.values[rng.random(test.shape) < mask_fraction] = np.nan
    model = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("model", Ridge(alpha=1.0))])
    model.fit(fit, frame.loc[fit_idx, target])
    calibration_prediction = model.predict(calibration)
    prediction = model.predict(test)
    residuals = np.abs(frame.loc[calibration_idx, target].to_numpy() - calibration_prediction)
    radius = float(np.quantile(residuals, 0.9, method="higher"))
    observed = frame.loc[test_idx, target].to_numpy()
    coverage = float(np.mean((observed >= prediction - radius) & (observed <= prediction + radius)))
    return {"group": group, "rows_fit": int(len(fit_idx)), "rows_calibration": int(len(calibration_idx)), "rows_test": int(len(test_idx)), "mask_fraction": mask_fraction, "interval_radius_90": radius, "interval_coverage": coverage, "seed": seed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("--features", nargs="+", required=True)
    parser.add_argument("--target", default="response_value")
    parser.add_argument("--group")
    parser.add_argument("--mask-fraction", type=float, default=0.25)
    parser.add_argument("--mask-fractions", type=float, nargs="+", help="Evaluate several masking fractions in one run")
    parser.add_argument("--seeds", type=int, nargs="+", help="Evaluate several random seeds in one run")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    fractions = args.mask_fractions or [args.mask_fraction]
    seeds = args.seeds or [20260821]
    result = [evaluate(args.table, args.target, args.group, args.features, fraction, seed) for seed in seeds for fraction in fractions]
    rendered = json.dumps(result[0] if len(result) == 1 else result, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
