#!/usr/bin/env python3
"""Create a compact composite panel for the main scientific story."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs/figures/composite_validation.png"
out.parent.mkdir(parents=True, exist_ok=True)
lood = json.loads((ROOT / "data/processed/full_universe_lood_results.json").read_text())
conflict = json.loads((ROOT / "data/processed/modality_conflict_summary.json").read_text())
datasets = list(lood["folds"])
models = ["expression", "copy_number", "mutation", "fusion"]
colors = ["#377eb8", "#ff7f00", "#4daf4a", "#e41a1c"]
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), constrained_layout=True)
ax = axes[0]
x = np.arange(len(datasets)); width = 0.18
for i, model in enumerate(models):
    vals = [lood["folds"][d]["metrics"][model]["rmse"] for d in datasets]
    ax.bar(x + (i - 1.5) * width, vals, width, label=model.replace("_", " "), color=colors[i])
ax.set_title("A  Cross-study transfer"); ax.set_ylabel("RMSE"); ax.set_xticks(x, datasets); ax.legend(fontsize=7, frameon=False)
ax = axes[1]
rows = conflict["rows"]; labels = [str(r["held_out"]) for r in rows]; vals = [r["fusion_delta_rmse"] for r in rows]
ax.bar(np.arange(len(vals)), vals, color=["#2166ac" if v < 0 else "#b2182b" for v in vals]); ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("B  Fusion − expression"); ax.set_ylabel("RMSE delta"); ax.set_xticks(np.arange(len(vals)), labels, rotation=55, ha="right", fontsize=7)
ax.text(0.02, 0.02, "blue = fusion favored\nred = expression favored", transform=ax.transAxes, fontsize=7)
ax = axes[2]
mods = ["Expression", "Copy number", "Mutation", "All complete"]; availability = [0.827, 0.594, 0.995, 0.591]
ax.bar(mods, availability, color=["#377eb8", "#ff7f00", "#4daf4a", "#984ea3"]); ax.set_title("C  Outer-join availability"); ax.set_ylabel("Fraction of rows"); ax.set_ylim(0, 1.05); ax.tick_params(axis="x", labelrotation=35)
for i, v in enumerate(availability): ax.text(i, v + 0.025, f"{v:.3f}", ha="center", fontsize=8)
fig.suptitle("Incremental value, transferability, and structured availability", fontsize=13)
fig.savefig(out, dpi=300, facecolor="white"); fig.savefig(out.with_suffix(".pdf")); print(out)
