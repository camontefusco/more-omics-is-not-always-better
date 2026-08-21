#!/usr/bin/env python3
"""Fail if committed release figures or source data are missing/empty."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("figure_dir", type=Path)
    args = parser.parse_args()
    required = ["lood_rmse.png", "lood_rmse.pdf", "lood_rmse_source.json"]
    report = {}
    for name in required:
        path = args.figure_dir / name
        if not path.exists() or path.stat().st_size == 0:
            raise SystemExit(f"missing or empty release figure artifact: {path}")
        report[name] = path.stat().st_size
    source = json.loads((args.figure_dir / "lood_rmse_source.json").read_text())
    if len(source["datasets"]) != 3 or len(source["modalities"]) != 4:
        raise SystemExit("unexpected LOOD figure source dimensions")
    print(json.dumps({"status": "pass", "artifacts": report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
