#!/usr/bin/env python3
"""Audit mechanism-of-action coverage against a response table."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_column(path: Path, column: str) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if column not in (reader.fieldnames or []):
            raise ValueError(f"{path}: missing column {column}")
        return {(row.get(column) or "").strip() for row in reader if (row.get(column) or "").strip()}


def audit(response_table: Path, mapping_table: Path) -> dict[str, object]:
    response_drugs = read_column(response_table, "drug_id_raw")
    with mapping_table.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"drug_id_raw", "moa_primary", "confidence"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{mapping_table}: missing columns {sorted(missing)}")
        mappings = list(reader)

    mapped_drugs = {(row.get("drug_id_raw") or "").strip() for row in mappings if (row.get("drug_id_raw") or "").strip()}
    covered = response_drugs & mapped_drugs
    unmapped = sorted(response_drugs - mapped_drugs)
    uncertain = sorted({(row.get("drug_id_raw") or "").strip() for row in mappings if (row.get("confidence") or "").strip().lower() in {"uncertain", "low"}})
    return {
        "response_drug_count": len(response_drugs),
        "mapped_drug_count": len(covered),
        "coverage_fraction": (len(covered) / len(response_drugs)) if response_drugs else 0.0,
        "unmapped_drugs": unmapped,
        "uncertain_mappings": uncertain,
        "ok": not unmapped,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("response_table", type=Path)
    parser.add_argument("mapping_table", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    result = audit(args.response_table, args.mapping_table)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
