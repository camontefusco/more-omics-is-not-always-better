import csv
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "harmonize_identifiers.py"
SPEC = importlib.util.spec_from_file_location("harmonize_identifiers", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_mapping_preserves_raw_and_reports_unmatched(tmp_path):
    source = tmp_path / "source.csv"
    source.write_text("cell_line_id_raw,response_value\nA,1.2\nB,2.3\n", encoding="utf-8")
    output = tmp_path / "output.csv"
    counts = MODULE.harmonize(source, output, {"cell_line_id_raw": {"A": "cellosaurus_id"}})
    assert counts["rows"] == 2
    assert counts["cell_line_id_raw_unmatched"] == 1
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["cell_line_id_raw"] == "A"
    assert rows[0]["cellosaurus_id"] == "cellosaurus_id"
    assert rows[1]["cellosaurus_id"] == ""
