#!/usr/bin/env python3
"""Audit modality availability, structured missingness, and simple redundancy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd


def audit_table(path: Path) -> dict[str, object]:
    frame = pd.read_csv(path)
    groups = {
        "expression": [c for c in frame if c.startswith("expression__")],
        "copy_number": [c for c in frame if c.startswith("copy_number__")],
        "mutation": [c for c in frame if c.startswith("mutation__")],
    }
    availability = {name: float(frame[cols].notna().any(axis=1).mean()) for name, cols in groups.items()}
    complete_case = float(frame[[c for cols in groups.values() for c in cols]].notna().all(axis=1).mean())
    modality_means = pd.DataFrame({name: frame[cols].apply(pd.to_numeric, errors="coerce").mean(axis=1) for name, cols in groups.items()})
    correlations = modality_means.corr().where(~np.eye(3, dtype=bool)).stack().to_dict()
    return {
        "rows": int(len(frame)),
        "feature_counts": {name: len(cols) for name, cols in groups.items()},
        "modality_row_availability": availability,
        "all_modality_complete_case_fraction": complete_case,
        "row_mean_modality_correlations": {f"{a}__{b}": float(v) for (a, b), v in correlations.items() if a < b},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tables", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {path.stem: audit_table(path) for path in args.tables}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
