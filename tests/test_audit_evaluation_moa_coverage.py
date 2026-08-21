import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_evaluation_moa_coverage.py"
SPEC = importlib.util.spec_from_file_location("audit_eval_moa", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_evaluation_universe_mapping_is_complete(tmp_path):
    results = tmp_path / "results.json"
    results.write_text(json.dumps({"DRUG_A": {}, "DRUG_B": {}}), encoding="utf-8")
    mapping = tmp_path / "mapping.csv"
    mapping.write_text("drug_id_raw\nDRUG_A\nDRUG_B\n", encoding="utf-8")
    result = MODULE.audit([results], mapping)
    assert result["evaluation_drug_count"] == 2
    assert result["mapped_evaluation_drug_count"] == 2
    assert result["ok"] is True
