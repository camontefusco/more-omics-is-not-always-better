#!/usr/bin/env python3
"""Validate the project dataset manifest before data acquisition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {"project", "manifest_status", "as_of", "response_resources", "modalities", "harmonization", "validation"}
REQUIRED_RESOURCE = {"id", "name", "role", "response_metric", "source_url", "release"}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("PyYAML is required: install it in the project environment") from exc
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("Manifest root must be a mapping")
    return value


def audit(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL - set(manifest)
    errors.extend(f"missing top-level field: {field}" for field in sorted(missing))

    resources = manifest.get("response_resources")
    if not isinstance(resources, list) or not resources:
        errors.append("response_resources must be a non-empty list")
    else:
        ids: set[str] = set()
        for index, resource in enumerate(resources):
            if not isinstance(resource, dict):
                errors.append(f"resource {index} must be a mapping")
                continue
            errors.extend(f"resource {index} missing field: {field}" for field in sorted(REQUIRED_RESOURCE - set(resource)))
            resource_id = resource.get("id")
            if resource_id in ids:
                errors.append(f"duplicate resource id: {resource_id}")
            ids.add(str(resource_id))
            for field in ("release", "response_metric"):
                if resource.get(field) in (None, "", "to_record", "to_lock"):
                    errors.append(f"resource {resource_id} has unresolved {field}")

    modalities = manifest.get("modalities")
    for modality in ("transcriptomics", "mutation", "copy_number"):
        if not isinstance(modalities, dict) or modality not in modalities:
            errors.append(f"missing modality definition: {modality}")

    validation = manifest.get("validation")
    if not isinstance(validation, dict) or not validation.get("splits"):
        errors.append("validation.splits must be a non-empty list")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    errors = audit(load_manifest(args.manifest))
    result = {"manifest": str(args.manifest), "ok": not errors, "errors": errors}
    print(json.dumps(result, indent=2))
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
