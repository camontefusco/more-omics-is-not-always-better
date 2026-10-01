from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path('/Users/cmontefusco/Coding_projects/more-omics-is-not-always-better')
OUT = ROOT / 'outputs/figures/decision_tree_benchmark.png'
plt.rcParams['font.family'] = 'Arial'

fig, ax = plt.subplots(figsize=(18, 10), dpi=600)
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')

NAVY = '#17365D'
BLUE = '#EAF2F8'
TEAL = '#E7F5F2'
AMBER = '#FFF4D6'
INK = '#111111'
GREY = '#657184'


def rounded(x, y, w, h, text, face=BLUE, edge=NAVY, size=15, weight='normal'):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.18,rounding_size=0.12',
        linewidth=2.0, edgecolor=edge, facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=size, color=INK, fontweight=weight, linespacing=1.25)


def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=22, linewidth=2.2, color=GREY))

# Main three-stage structure.
columns = [(0.5, '1  DEFINE THE CLAIM'), (6.15, '2  AUDIT THE DATA'), (11.8, '3  VALIDATE THE MODEL')]
for x, label in columns:
    rounded(x, 8.35, 5.0, 0.85, label, face=NAVY, edge=NAVY, size=17, weight='bold')

arrow(5.55, 8.78, 6.0, 8.78)
arrow(11.2, 8.78, 11.65, 8.78)

# Stage 1.
rounded(0.7, 6.25, 4.6, 1.35,
        'What is the intended use?\n\nWithin-source comparison\nor transfer to another source?',
        face=BLUE, size=15, weight='bold')
rounded(0.7, 4.25, 4.6, 1.35,
        'Are drug descriptors available?\n\nStructure, target, or mechanism',
        face=AMBER, edge='#B07D00', size=15)
rounded(0.7, 2.25, 4.6, 1.35,
        'If not: use cell-line features only\nand limit claims to the declared\ncompound universe',
        face=TEAL, edge='#147D73', size=14)
arrow(3.0, 6.25, 3.0, 5.65)
arrow(3.0, 4.25, 3.0, 3.65)

# Stage 2.
rounded(6.35, 6.25, 4.6, 1.35,
        'Are modalities available\nfor the same population?',
        face=BLUE, size=16, weight='bold')
rounded(6.35, 4.25, 4.6, 1.35,
        'Audit missingness before modeling\n\nDo not silently use complete cases',
        face=AMBER, edge='#B07D00', size=14)
rounded(6.35, 2.25, 4.6, 1.35,
        'Report modality coverage\nand test whether availability\nchanges the evaluated population',
        face=TEAL, edge='#147D73', size=14)
arrow(8.65, 6.25, 8.65, 5.65)
arrow(8.65, 4.25, 8.65, 3.65)

# Stage 3.
rounded(11.95, 6.25, 5.35, 1.35,
        'Choose a validation design\nthat matches the claim',
        face=BLUE, size=16, weight='bold')
rounded(11.95, 4.25, 2.45, 1.35,
        'Drug-grouped\nsplits',
        face=BLUE, size=15, weight='bold')
rounded(14.85, 4.25, 2.45, 1.35,
        'Source-held-out\ntransfer',
        face=BLUE, size=15, weight='bold')
arrow(14.62, 6.25, 13.18, 5.65)
arrow(14.62, 6.25, 16.08, 5.65)
rounded(11.95, 2.25, 5.35, 1.35,
        'Inside each training fold:\nselect features, impute, standardize,\nfit, and report uncertainty',
        face=TEAL, edge='#147D73', size=14)
arrow(14.62, 4.25, 14.62, 3.65)

# Bottom conclusion.
rounded(1.0, 0.45, 16.0, 1.2,
        'Study conclusion: additional omics produced a small, variable, validation-dependent gain.\nKeep an added modality only when its benefit is reproducible, available, and relevant to the intended use.',
        face=NAVY, edge=NAVY, size=16, weight='bold')
arrow(8.65, 2.25, 8.65, 1.7)

fig.savefig(OUT, dpi=600, bbox_inches='tight', pad_inches=0.3, facecolor='white')
plt.close(fig)
