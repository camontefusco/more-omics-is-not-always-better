#!/usr/bin/env python3
"""Render signed fusion-minus-expression RMSE deltas."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.summary.read_text())
    rows = data["rows"]
    labels = [f"LOOD\n{r['held_out']}" if r["validation"] == "leave_one_dataset_out" else f"Drug-heldout\n{r['held_out']}" for r in rows]
    deltas = [r["fusion_delta_rmse"] for r in rows]
    colors = ["#b2182b" if x > 0 else "#2166ac" for x in deltas]
    fig, ax = plt.subplots(figsize=(9, 5.2), constrained_layout=True)
    ax.bar(range(len(rows)), deltas, color=colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(range(len(rows)), labels, fontsize=8)
    ax.set_ylabel("Fusion − expression RMSE")
    ax.set_title("Conditional multimodal value across held-out folds")
    ax.text(0, -0.18, "Negative values favor fusion; positive values favor expression", transform=ax.transAxes, fontsize=8)
    args.output.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output / "modality_conflict.png", dpi=300)
    fig.savefig(args.output / "modality_conflict.pdf")
    plt.close(fig)
    (args.output / "modality_conflict_source.json").write_text(json.dumps(data, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
