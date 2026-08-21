#!/usr/bin/env python3
"""Create an ingestion run directory only when the manifest is locked."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from audit_dataset_manifest import audit, load_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", type=Path, default=Path("data/interim/ingestion"))
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    errors = audit(manifest)
    result = {
        "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(args.manifest),
        "ok": not errors,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        return 1

    run_dir = args.output_root / args.run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "provenance.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
