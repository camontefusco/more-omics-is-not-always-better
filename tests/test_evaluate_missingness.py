import importlib.util
from pathlib import Path

import pandas as pd


SCRIPT = Path(__file__).parents[1] / "scripts" / "evaluate_missingness.py"
SPEC = importlib.util.spec_from_file_location("evaluate_missingness", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_missingness_evaluation_returns_interval_metrics(tmp_path):
    path = tmp_path / "table.csv"
    pd.DataFrame({
        "cell_line_id_raw": list("AABBCCDDEE"),
        "response_value": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
        "expr_1": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
    }).to_csv(path, index=False)
    result = MODULE.evaluate(path, "response_value", "cell_line_id_raw", ["expr_1"], 0.5)
    assert 0 <= result["interval_coverage"] <= 1
    assert result["interval_radius_90"] >= 0
