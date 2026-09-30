from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path('/Users/cmontefusco/Coding_projects/more-omics-is-not-always-better')
OUT = ROOT / 'outputs/figures/decision_tree_benchmark.png'
plt.rcParams['font.family'] = 'Arial'

fig, ax = plt.subplots(figsize=(16, 10), dpi=600)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

NAVY = '#183B66'
BLUE = '#DDEAF7'
TEAL = '#E5F4F1'
GOLD = '#FFF3D6'
PALE = '#EAF3FF'
DARK = '#111111'
GREY = '#667085'


def box(x, y, w, h, text, face=BLUE, edge=NAVY, size=12, bold=False):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.16,rounding_size=0.12',
        facecolor=face, edgecolor=edge, linewidth=1.8,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha='center', va='center', color=DARK,
        fontsize=size, fontweight='bold' if bold else 'normal',
        linespacing=1.22, wrap=True,
    )


def arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops={'arrowstyle': '-|>', 'lw': 1.8, 'color': GREY})

# Four primary questions.
xs = [0.35, 4.25, 8.15, 12.05]
headers = [
    '1. Intended use',
    '2. Drug information',
    '3. Data coverage',
    '4. Validation target',
]
for x, text in zip(xs, headers):
    box(x, 8.35, 3.6, 1.15, text, face=BLUE, size=14, bold=True)
for x1, x2 in [(3.95, 4.25), (7.85, 8.15), (11.75, 12.05)]:
    arrow(x1, 8.92, x2, 8.92)

# Decision branches.
box(0.35, 6.35, 3.6, 1.35,
    'Drug descriptors available\n(structure, target, or MOA)?',
    face=PALE, size=12, bold=True)
box(4.25, 6.35, 3.6, 1.35,
    'Yes: use a drug-aware\nmodel and define compound-level\ntransfer explicitly',
    face=TEAL, edge='#157A7A', size=11)
box(8.15, 6.35, 3.6, 1.35,
    'No: cell-line-only transfer\nwith narrow claims about\nthe declared drug universe',
    face=GOLD, edge='#B8860B', size=11)
arrow(2.15, 8.35, 2.15, 7.70)
arrow(2.15, 6.35, 6.05, 7.70)

box(12.05, 6.35, 3.6, 1.35,
    'Are modalities similarly\navailable across the\nevaluation population?',
    face=PALE, size=12, bold=True)
arrow(13.85, 8.35, 13.85, 7.70)

# Coverage outcomes.
box(10.35, 4.25, 3.6, 1.35,
    'No: retain missingness\nstrata and test whether\ncoverage changes conclusions',
    face=GOLD, edge='#B8860B', size=11)
box(14.15, 4.25, 1.5, 1.35,
    'Yes:\nproceed',
    face=TEAL, edge='#157A7A', size=11, bold=True)
arrow(13.85, 6.35, 12.15, 5.60)
arrow(13.85, 6.35, 14.90, 5.60)

# Validation workflow.
box(0.35, 3.90, 3.6, 1.35,
    'Within-source\ngrouped drug splits',
    face=BLUE, size=12, bold=True)
box(4.25, 3.90, 3.6, 1.35,
    'Source-held-out transfer\ninterpret as a portability\nstress test',
    face=BLUE, size=11, bold=True)
box(8.15, 3.90, 3.6, 1.35,
    'Select features, impute,\nand standardize inside\neach training fold',
    face=BLUE, size=11, bold=True)
box(12.05, 3.90, 3.6, 1.35,
    'Report baseline, delta,\nvariability, response scale,\nand modality coverage',
    face=BLUE, size=11, bold=True)
for x1, x2 in [(3.95, 4.25), (7.85, 8.15), (11.75, 12.05)]:
    arrow(x1, 4.58, x2, 4.58)

# Bottom conclusion.
box(0.75, 0.90, 14.5, 1.65,
    'Decision in this study\nThe multimodal gain was small, variable, and conditional.\nAdditional assays should be retained only when their incremental value is stable, available, and relevant to the intended use.',
    face=PALE, size=14, bold=True)
arrow(8.0, 3.90, 8.0, 2.55)

fig.savefig(OUT, dpi=600, bbox_inches='tight', pad_inches=0.25, facecolor='white')
plt.close(fig)
