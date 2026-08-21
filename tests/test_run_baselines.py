import importlib.util
from pathlib import Path

import pandas as pd


SCRIPT = Path(__file__).parents[1] / "scripts" / "run_baselines.py"
SPEC = importlib.util.spec_from_file_location("run_baselines", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_baseline_runs_with_grouped_split(tmp_path):
    path = tmp_path / "table.csv"
    pd.DataFrame({
        "cell_line_id_raw": ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E"],
        "response_value": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
        "expr_1": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
    }).to_csv(path, index=False)
    result = MODULE.run(path, "response_value", "cell_line_id_raw", ["expr_1"])
    assert result["model"] == "ridge"
    assert result["test_rows"] > 0
    assert result["rmse"] >= 0
