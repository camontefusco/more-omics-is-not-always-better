import importlib.util
from pathlib import Path

import pandas as pd


SCRIPT = Path(__file__).parents[1] / "scripts" / "select_features_train_only.py"
SPEC = importlib.util.spec_from_file_location("select_features_train_only", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_feature_selection_uses_training_ids(tmp_path):
    source = tmp_path / "features.csv"
    pd.DataFrame({"depmap_id": ["A", "B", "C"], "g1": [1, 2, 3], "g2": [1, 1, 1]}).to_csv(source, index=False)
    output = tmp_path / "selected.csv"
    result = MODULE.select(source, {"A", "B"}, output, top_k=1)
    assert result["matched_train_ids"] == 2
    assert result["features"] == ["g1"]
    assert list(pd.read_csv(output).columns) == ["depmap_id", "g1"]
