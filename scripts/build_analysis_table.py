#!/usr/bin/env python3
"""Build long-form response tables and a modality-availability report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


META = ["depmap_id", "cell_line_display_name", "lineage_1", "lineage_2", "lineage_3", "lineage_6", "lineage_4"]


def response_long(path: Path, dataset_id: str, release_id: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    response_columns = [column for column in frame.columns if column not in META]
    long = frame.melt(id_vars=[column for column in META if column in frame.columns], value_vars=response_columns, var_name="drug_id_raw", value_name="response_value")
    long["dataset_id"] = dataset_id
    long["release_id"] = release_id
    long["response_metric"] = "AUC"
    long["download_date"] = "2026-08-21"
    long = long.dropna(subset=["response_value"])
    return long


def availability(paths: dict[str, Path]) -> dict[str, object]:
    ids: dict[str, set[str]] = {}
    for name, path in paths.items():
        ids[name] = set(pd.read_csv(path, usecols=["depmap_id"])["depmap_id"].dropna())
    union = set().union(*ids.values())
    return {"counts": {name: len(values) for name, values in ids.items()}, "union": len(union), "intersection": len(set.intersection(*ids.values()))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-root", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    raw = args.raw_root
    response_specs = {
        "ctd2": (raw / "CTD^2_(AUC)_subsetted.csv", "Harmonized CTD^2 25Q2"),
        "gdsc1": (raw / "Drug_sensitivity_AUC_(Sanger_GDSC1)_subsetted.csv", "Harmonized GDSC 25Q2"),
        "gdsc2": (raw / "Drug_sensitivity_AUC_(Sanger_GDSC2)_subsetted.csv", "Harmonized GDSC 25Q2"),
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    reports: dict[str, object] = {}
    for dataset, (path, release) in response_specs.items():
        table = response_long(path, dataset, release)
        out = args.output_root / f"response_{dataset}_long.csv"
        table.to_csv(out, index=False)
        reports[dataset] = {"rows": len(table), "cell_lines": int(table["depmap_id"].nunique()), "drugs": int(table["drug_id_raw"].nunique()), "path": str(out)}
    reports["modality_availability"] = availability({
        "expression": raw / "Expression_(Short-read)_Public_26Q1_subsetted.csv",
        "copy_number": raw / "Copy_Number_WGS_Public_26Q1_(log2)_subsetted.csv",
        "mutation": raw / "Damaging_Mutations_(Public_26Q1)_subsetted.csv",
    })
    (args.output_root / "ingestion_report.json").write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(reports, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
