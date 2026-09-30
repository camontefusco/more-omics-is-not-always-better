from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path('/Users/cmontefusco/Coding_projects/more-omics-is-not-always-better'); out=ROOT/'outputs/figures/decision_tree_benchmark.png'
plt.rcParams['font.family']='Arial'
fig,ax=plt.subplots(figsize=(14,8.5),dpi=600); ax.set_xlim(0,14); ax.set_ylim(0,8.5); ax.axis('off')
def box(x,y,w,h,text,fc='#EEF4FA',ec='#183B66',fs=11,bold=False):
 p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.10,rounding_size=.10',facecolor=fc,edgecolor=ec,lw=1.5); ax.add_patch(p); ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,weight='bold' if bold else 'normal',wrap=True,color='#111',linespacing=1.15)
def ar(x1,y1,x2,y2): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops={'arrowstyle':'-|>','lw':1.5,'color':'#5B6573'})
xs=[.25,3.45,6.65,9.85]
for x,t in zip(xs,['1. Define intended use','2. Drug features available?','3. Audit coverage and missingness','4. Choose validation estimand']): box(x,6.35,3.0,1.05,t,fc='#DDEAF7',fs=11,bold=True)
for a,b in [(3.25,3.45),(6.45,6.65),(9.65,9.85)]: ar(a,6.88,b,6.88)
box(0.85,4.70,3.1,1.25,'Yes: use drug-aware\nmodeling',fc='#E5F4F1',ec='#157A7A'); box(4.15,4.70,3.1,1.25,'No: cell-line-only\ntransfer with narrow claims',fc='#FFF3D6',ec='#B8860B'); ar(4.85,6.45,2.4,5.85); ar(4.85,6.45,5.65,5.85)
box(7.0,4.70,3.1,1.25,'Unequal availability:\nretain audit and test robustness',fc='#FFF3D6',ec='#B8860B'); box(10.35,4.70,2.7,1.25,'Comparable coverage:\nproceed',fc='#E5F4F1',ec='#157A7A'); ar(8.05,6.45,8.4,5.85); ar(8.05,6.45,11.35,5.85)
box(.35,2.65,3.0,1.25,'Within-source\ngrouped drug splits'); box(3.55,2.65,3.0,1.25,'Source transfer\nLOOD, interpreted cautiously'); box(6.75,2.65,3.0,1.25,'Fold-local selection,\nimputation, and scaling'); box(9.95,2.65,3.0,1.25,'Report baseline, delta,\nvariability, and coverage')
for a,b in [(3.35,3.55),(6.55,6.75),(9.75,9.95)]: ar(a,3.28,b,3.28)
box(.8,.65,12.4,1.35,'Decision in this study: the fusion gain was small, variable, and conditional.\nRetain additional modalities only when their benefit is stable, available, and relevant to the intended use case.',fc='#EAF3FF',ec='#183B66',fs=12,bold=True); ar(6.5,2.65,6.5,2.0)
fig.savefig(out,bbox_inches='tight',pad_inches=.2,facecolor='white'); plt.close(fig)
