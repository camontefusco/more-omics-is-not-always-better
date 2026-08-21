import importlib.util
from pathlib import Path

import pandas as pd


SCRIPT = Path(__file__).parents[1] / "scripts" / "evaluate_modalities.py"
SPEC = importlib.util.spec_from_file_location("evaluate_modalities", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_modalities_share_split_and_report_delta(tmp_path):
    path = tmp_path / "table.csv"
    pd.DataFrame({
        "cell_line_id_raw": ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E"],
        "response_value": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
        "expr_1": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
        "mut_1": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    }).to_csv(path, index=False)
    result = MODULE.evaluate(path, "response_value", "cell_line_id_raw", {"expression": ["expr_1"], "fusion": ["expr_1", "mut_1"]})
    assert set(result["scores"]) == {"expression", "fusion"}
    assert result["rmse_delta_vs_first"]["expression"] == 0.0
