#!/usr/bin/env python3
"""Select high-variance features using training cell lines only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


META = ["depmap_id", "cell_line_display_name", "lineage_1", "lineage_2", "lineage_3", "lineage_6", "lineage_4"]


def select(path: Path, train_ids: set[str], output: Path, top_k: int = 2000) -> dict[str, object]:
    frame = pd.read_csv(path)
    if "depmap_id" not in frame.columns:
        raise ValueError("feature table must contain depmap_id")
    feature_columns = [column for column in frame.columns if column not in META]
    train = frame[frame["depmap_id"].astype(str).isin(train_ids)].copy()
    if train.empty:
        raise ValueError("no training cell lines matched")
    numeric = train[feature_columns].apply(pd.to_numeric, errors="coerce")
    variances = numeric.var(axis=0, skipna=True).fillna(0).sort_values(ascending=False)
    selected = variances.head(min(top_k, len(variances))).index.tolist()
    result = frame[["depmap_id"] + selected].copy()
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    return {"source": str(path), "output": str(output), "train_ids": len(train_ids), "matched_train_ids": len(train), "selected_features": len(selected), "features": selected}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_table", type=Path)
    parser.add_argument("train_ids", type=Path, help="one depmap_id per line")
    parser.add_argument("output", type=Path)
    parser.add_argument("--top-k", type=int, default=2000)
    args = parser.parse_args()
    ids = {line.strip() for line in args.train_ids.read_text(encoding="utf-8").splitlines() if line.strip()}
    print(json.dumps(select(args.feature_table, ids, args.output, args.top_k), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
