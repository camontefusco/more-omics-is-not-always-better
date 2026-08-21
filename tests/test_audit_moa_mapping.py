import csv
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_moa_mapping.py"
SPEC = importlib.util.spec_from_file_location("audit_moa_mapping", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_moa_audit_reports_unmapped_drugs(tmp_path):
    response = tmp_path / "responses.csv"
    response.write_text("drug_id_raw\nA\nB\n", encoding="utf-8")
    mapping = tmp_path / "mapping.csv"
    mapping.write_text("drug_id_raw,moa_primary,confidence\nA,EGFR inhibitor,high\n", encoding="utf-8")
    result = MODULE.audit(response, mapping)
    assert result["ok"] is False
    assert result["unmapped_drugs"] == ["B"]
    assert result["coverage_fraction"] == 0.5
