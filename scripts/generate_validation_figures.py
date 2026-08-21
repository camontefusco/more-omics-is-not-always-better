#!/usr/bin/env python3
"""Generate compact publication-source figures from frozen validation JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lood", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.lood.read_text())
    datasets = list(result["folds"])
    modalities = ["expression", "copy_number", "mutation", "fusion"]
    values = np.array([[result["folds"][d]["metrics"][m]["rmse"] for d in datasets] for m in modalities])

    args.output.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.8), constrained_layout=True)
    x = np.arange(len(datasets))
    width = 0.19
    for i, modality in enumerate(modalities):
        ax.bar(x + (i - 1.5) * width, values[i], width, label=modality.replace("_", " "))
    ax.set_xticks(x, datasets)
    ax.set_ylabel("RMSE")
    ax.set_title("Leave-one-dataset-out performance")
    ax.legend(frameon=False, ncol=2)
    ax.text(0, -0.22, "Fold-local top-2,000 features from full raw modality universes; Ridge; outer-joined table", transform=ax.transAxes, fontsize=8)
    fig.savefig(args.output / "lood_rmse.png", dpi=300)
    fig.savefig(args.output / "lood_rmse.pdf")
    plt.close(fig)
    (args.output / "lood_rmse_source.json").write_text(json.dumps({"source": str(args.lood), "datasets": datasets, "modalities": modalities, "rmse": values.tolist(), "feature_budget": 2000, "model": "Ridge alpha=1.0"}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
