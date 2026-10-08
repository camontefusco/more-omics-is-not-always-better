from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / "submission" / "graphical_abstract.png"
fig, ax = plt.subplots(figsize=(5.31, 13.28), dpi=100)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def box(y, text, color="#EAF2F8", edge="#1F4E79", size=15, height=.12):
    p = FancyBboxPatch((.08, y), .84, height, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor=color, edgecolor=edge, linewidth=2)
    ax.add_patch(p); ax.text(.5, y+height/2, text, ha="center", va="center", wrap=True, fontsize=size, color="#111111")

ax.text(.5, .96, "When More Omics Is Not Always Better", ha="center", va="center", fontsize=20, weight="bold", wrap=True)
ax.text(.5, .915, "A leakage-controlled information-fusion benchmark", ha="center", va="center", fontsize=12)
box(.78, "15 compounds\nGDSC1 • GDSC2 • CTD²", "#F3F6FA")
box(.61, "Full raw feature universe\nExpression • copy number • mutation", "#F3F6FA")
box(.44, "Fold-local top-2,000 selection\nMedian imputation • scaling • Ridge", "#F3F6FA")
for y in [.765, .595, .425]: ax.add_patch(FancyArrowPatch((.5, y), (.5, y-.045), arrowstyle="-|>", mutation_scale=18, linewidth=1.8, color="#555555"))
box(.24, "Drug-held-out validation\nFusion RMSE: 0.2322\nExpression RMSE: 0.2328\n4/5 splits favored fusion", "#E8F5E9", "#2E7D32", 14, .14)
box(.05, "Cross-study LOOD\nFusion slightly worse in all 3 folds\nTransfer remains dataset-sensitive", "#FDEDEC", "#A93226", 14, .14)
ax.text(.5, .215, "Small within-study gain", ha="center", va="center", fontsize=13, weight="bold", color="#2E7D32")
ax.text(.5, .005, "Conclusion: evaluate fusion by incremental value, transferability, and failure modes.", ha="center", va="bottom", fontsize=10, wrap=True)
fig.savefig(OUT, dpi=100, bbox_inches=None, facecolor="white")
print(OUT)
