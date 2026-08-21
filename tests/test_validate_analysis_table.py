import csv
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_analysis_table.py"
SPEC = importlib.util.spec_from_file_location("validate_analysis_table", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


HEADER = "cell_line_id_raw,drug_id_raw,response_value,response_metric,dataset_id,release_id,download_date\n"


def test_valid_table_passes(tmp_path):
    path = tmp_path / "valid.csv"
    path.write_text(HEADER + "A,D,1.5,AUC,test,v1,2026-08-21\n", encoding="utf-8")
    result = MODULE.validate(path)
    assert result["ok"] is True
    assert result["rows"] == 1


def test_duplicate_and_missing_provenance_fail(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(HEADER + "A,D,1.5,AUC,test,,2026-08-21\nA,D,2.0,AUC,test,v1,\n", encoding="utf-8")
    result = MODULE.validate(path)
    assert result["ok"] is False
    assert result["duplicate_count"] == 1
    assert any("release_id" in error for error in result["errors"])
    assert any("download_date" in error for error in result["errors"])
