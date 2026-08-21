#!/usr/bin/env python3
"""Create deterministic split manifests from a long-form response table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def make_splits(path: Path, output: Path, seed: int = 20260821) -> dict[str, object]:
    frame = pd.read_csv(path, usecols=["depmap_id", "drug_id_raw"])
    frame = frame.drop_duplicates().reset_index(drop=True)
    result: dict[str, object] = {"source": str(path), "seed": seed, "rows": len(frame)}
    pair = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    train, test = next(pair.split(frame, groups=frame["depmap_id"].astype(str) + "::" + frame["drug_id_raw"].astype(str)))
    result["pair_held_out"] = {"train_rows": len(train), "test_rows": len(test)}
    for name, column in (("cell_line_held_out", "depmap_id"), ("drug_held_out", "drug_id_raw")):
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
        train, test = next(splitter.split(frame, groups=frame[column].astype(str)))
        result[name] = {
            "train_rows": len(train),
            "test_rows": len(test),
            "train_groups": int(frame.iloc[train][column].nunique()),
            "test_groups": int(frame.iloc[test][column].nunique()),
            "train_group_ids": sorted(frame.iloc[train][column].astype(str).unique().tolist()),
            "test_group_ids": sorted(frame.iloc[test][column].astype(str).unique().tolist()),
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("response_table", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/processed/split_manifest.json"))
    args = parser.parse_args()
    print(json.dumps(make_splits(args.response_table, args.output), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
