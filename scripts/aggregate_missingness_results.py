#!/usr/bin/env python3
"""Aggregate cross-dataset missingness evaluation JSON outputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def aggregate(inputs: dict[str, Path]) -> dict[str, object]:
    datasets = {}
    all_rows = []
    for dataset, path in inputs.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = list(payload.values())
        coverages = [float(row["interval_coverage"]) for row in rows]
        datasets[dataset] = {
            "drugs": len(rows),
            "mean_coverage": sum(coverages) / len(coverages),
            "min_coverage": min(coverages),
            "max_coverage": max(coverages),
            "at_or_above_nominal_90": sum(value >= 0.9 for value in coverages),
            "results": payload,
        }
        all_rows.extend((dataset, value) for value in coverages)
    coverages = [value for _, value in all_rows]
    return {
        "nominal_coverage": 0.9,
        "datasets": datasets,
        "pooled_drugs": len(coverages),
        "pooled_mean_coverage": sum(coverages) / len(coverages),
        "pooled_at_or_above_nominal_90": sum(value >= 0.9 for value in coverages),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gdsc1", type=Path, required=True)
    parser.add_argument("--gdsc2", type=Path, required=True)
    parser.add_argument("--ctd2", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = aggregate({"GDSC1": args.gdsc1, "GDSC2": args.gdsc2, "CTD2": args.ctd2})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
