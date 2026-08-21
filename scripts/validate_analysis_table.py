#!/usr/bin/env python3
"""Validate a harmonized cell-line × drug response table."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REQUIRED = {
    "cell_line_id_raw", "drug_id_raw", "response_value", "response_metric",
    "dataset_id", "release_id", "download_date",
}


def validate(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        errors.extend(f"missing required column: {field}" for field in sorted(REQUIRED - fields))
        rows = list(reader)

    seen: set[tuple[str, str]] = set()
    duplicate_count = 0
    invalid_response_count = 0
    for index, row in enumerate(rows, start=2):
        key = ((row.get("cell_line_id_raw") or "").strip(), (row.get("drug_id_raw") or "").strip())
        if key in seen and key != ("", ""):
            duplicate_count += 1
        seen.add(key)
        try:
            value = float(row.get("response_value", ""))
            if value != value or value in (float("inf"), float("-inf")):
                raise ValueError
        except ValueError:
            invalid_response_count += 1
            errors.append(f"row {index} has invalid response_value")
        for column in ("response_metric", "dataset_id", "release_id", "download_date"):
            if not (row.get(column) or "").strip():
                errors.append(f"row {index} has empty {column}")

    if duplicate_count:
        errors.append(f"duplicate cell-line/drug observations: {duplicate_count}")
    if not rows:
        errors.append("table contains no data rows")
    if len({(row.get("response_metric") or "").strip() for row in rows}) > 1:
        warnings.append("multiple response metrics are present; do not compare without a pre-specified sensitivity analysis")

    return {
        "path": str(path),
        "ok": not errors,
        "rows": len(rows),
        "duplicate_count": duplicate_count,
        "invalid_response_count": invalid_response_count,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    result = validate(args.table)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
