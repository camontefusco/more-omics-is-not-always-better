import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "prepare_ingestion.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("prepare_ingestion", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_draft_manifest_is_blocked(tmp_path, monkeypatch, capsys):
    manifest_path = Path(__file__).parents[1] / "configs" / "dataset_manifest.yaml"
    monkeypatch.setattr("sys.argv", ["prepare_ingestion.py", str(manifest_path), "--run-id", "test", "--output-root", str(tmp_path)])
    assert MODULE.main() == 1
    assert not (tmp_path / "test").exists()
    assert '"ok": false' in capsys.readouterr().out
