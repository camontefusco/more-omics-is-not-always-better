#!/usr/bin/env python3
"""Build compact per-drug tables from locked responses and selected modalities."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def build(response: Path, modality_paths: dict[str, Path], drugs: list[str], output: Path, join: str = "inner") -> list[dict[str, object]]:
    response_frame = pd.read_csv(response)
    modalities = []
    for name, path in modality_paths.items():
        frame = pd.read_csv(path)
        frame = frame.rename(columns={c: f"{name}__{c}" for c in frame.columns if c != "depmap_id"})
        modalities.append(frame)
    joined = modalities[0]
    for frame in modalities[1:]:
        joined = joined.merge(frame, on="depmap_id", how=join, validate="one_to_one")
    output.mkdir(parents=True, exist_ok=True)
    reports = []
    for drug in drugs:
        response_subset = response_frame[response_frame["drug_id_raw"] == drug][["depmap_id", "response_value"]].dropna().copy()
        response_subset["drug_id_raw"] = drug
        table = response_subset.merge(joined, on="depmap_id", how="inner", validate="one_to_one")
        path = output / (drug.replace(" ", "_").replace("/", "-") + ".csv")
        table.to_csv(path, index=False)
        reports.append({"drug_id_raw": drug, "rows": len(table), "path": str(path)})
    return reports


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--expression", type=Path, required=True)
    parser.add_argument("--copy-number", type=Path, required=True)
    parser.add_argument("--mutation", type=Path, required=True)
    parser.add_argument("--drug", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--join", choices=["inner", "outer"], default="inner")
    args = parser.parse_args()
    import json
    print(json.dumps(build(args.response, {"expression": args.expression, "copy_number": args.copy_number, "mutation": args.mutation}, args.drug, args.output, args.join), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
