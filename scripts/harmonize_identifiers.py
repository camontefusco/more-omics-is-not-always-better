#!/usr/bin/env python3
"""Apply explicit cell-line, compound, and gene mapping tables to a CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_mapping(path: Path, raw_column: str, canonical_column: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        if not rows.fieldnames or raw_column not in rows.fieldnames or canonical_column not in rows.fieldnames:
            raise ValueError(f"{path}: expected columns {raw_column!r}, {canonical_column!r}")
        mapping: dict[str, str] = {}
        for row in rows:
            raw = (row.get(raw_column) or "").strip()
            canonical = (row.get(canonical_column) or "").strip()
            if not raw:
                continue
            if raw in mapping and mapping[raw] != canonical:
                raise ValueError(f"{path}: conflicting mappings for {raw!r}")
            mapping[raw] = canonical
        return mapping


def harmonize(input_path: Path, output_path: Path, mappings: dict[str, dict[str, str]]) -> dict[str, int]:
    with input_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("input CSV has no header")
        rows = list(reader)
        fieldnames = list(reader.fieldnames)
        for raw_column, mapping in mappings.items():
            canonical_column = next(iter(mapping.values()), None)
            if raw_column not in fieldnames or canonical_column is None:
                continue
            if canonical_column not in fieldnames:
                fieldnames.append(canonical_column)
        counts = {f"{column}_unmatched": 0 for column in mappings}
        for row in rows:
            for raw_column, mapping in mappings.items():
                canonical_column = next(iter(mapping.values()), None)
                if raw_column not in row or canonical_column is None:
                    continue
                raw_value = (row.get(raw_column) or "").strip()
                canonical = mapping.get(raw_value, "")
                row[canonical_column] = canonical
                if raw_value and not canonical:
                    counts[f"{raw_column}_unmatched"] += 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    counts["rows"] = len(rows)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cell-line-map", type=Path)
    parser.add_argument("--compound-map", type=Path)
    parser.add_argument("--gene-map", type=Path)
    args = parser.parse_args()
    mappings: dict[str, dict[str, str]] = {}
    if args.cell_line_map:
        mappings["cell_line_id_raw"] = load_mapping(args.cell_line_map, "cell_line_id_raw", "cellosaurus_id")
    if args.compound_map:
        mappings["drug_id_raw"] = load_mapping(args.compound_map, "drug_id_raw", "pubchem_cid")
    if args.gene_map:
        mappings["gene_id_raw"] = load_mapping(args.gene_map, "gene_id_raw", "gene_id_canonical")
    import json
    print(json.dumps(harmonize(args.input, args.output, mappings), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
