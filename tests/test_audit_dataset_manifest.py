import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_dataset_manifest.py"
SPEC = importlib.util.spec_from_file_location("audit_dataset_manifest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_current_manifest_passes_initial_lock():
    manifest = MODULE.load_manifest(Path(__file__).parents[1] / "configs" / "dataset_manifest.yaml")
    errors = MODULE.audit(manifest)
    assert errors == []


def test_complete_minimal_manifest_passes():
    manifest = {
        "project": "test",
        "manifest_status": "locked",
        "as_of": "2026-08-21",
        "response_resources": [{
            "id": "example",
            "name": "Example",
            "role": "primary",
            "response_metric": "AUC",
            "source_url": "https://example.org",
            "release": "v1",
        }],
        "modalities": {"transcriptomics": {}, "mutation": {}, "copy_number": {}},
        "harmonization": {},
        "validation": {"splits": ["pair_held_out"]},
    }
    assert MODULE.audit(manifest) == []
