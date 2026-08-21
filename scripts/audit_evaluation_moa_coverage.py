#!/usr/bin/env python3
"""Audit MoA coverage for the declared cross-dataset evaluation universe."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def audit(result_files: list[Path], mapping: Path) -> dict[str, object]:
    universe = set()
    for path in result_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        universe.update(payload)
    mapped = set()
    with mapping.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            mapped.add((row.get("drug_id_raw") or "").strip())
    normalized = {item.replace("_", " ") for item in universe}
    matched = sorted(item for item in universe if item in mapped or item.replace("_", " ") in mapped)
    return {
        "evaluation_drug_count": len(universe),
        "mapped_evaluation_drug_count": len(matched),
        "coverage_fraction": len(matched) / len(universe) if universe else 0.0,
        "unmapped_evaluation_drugs": sorted(universe - set(matched)),
        "ok": len(matched) == len(universe),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.results, args.mapping), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
