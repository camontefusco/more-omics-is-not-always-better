from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "information_fusion_supplementary.docx"

def cell(c, value, bold=False):
    c.text = ""; p=c.paragraphs[0]; p.paragraph_format.space_after=Pt(0)
    r=p.add_run(str(value)); r.bold=bold; r.font.size=Pt(8); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
def shade(c):
    tcPr=c._tc.get_or_add_tcPr(); shd=OxmlElement("w:shd"); shd.set(qn("w:fill"),"D9EAF7"); tcPr.append(shd)
def table(doc, headers, rows):
    t=doc.add_table(rows=1, cols=len(headers)); t.style="Table Grid"; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,h in enumerate(headers): cell(t.rows[0].cells[i],h,True); shade(t.rows[0].cells[i])
    for row in rows:
        cs=t.add_row().cells
        for i,v in enumerate(row): cell(cs[i],v)
    doc.add_paragraph(); return t
def heading(doc, text, level=1):
    p=doc.add_heading(text,level); p.paragraph_format.keep_with_next=True; return p
def para(doc, text):
    p=doc.add_paragraph(text); p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.05
def main():
    doc=Document(); s=doc.sections[0]; s.top_margin=Inches(.7); s.bottom_margin=Inches(.7); s.left_margin=Inches(.7); s.right_margin=Inches(.7)
    doc.styles["Normal"].font.name="Arial"; doc.styles["Normal"].font.size=Pt(9)
    for n,z in [("Title",18),("Heading 1",14),("Heading 2",11)]: doc.styles[n].font.name="Arial"; doc.styles[n].font.size=Pt(z); doc.styles[n].font.color.rgb=RGBColor(0,0,0)
    title=doc.add_paragraph(); title.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=title.add_run("Supplementary material\nWhen More Omics Is Not Always Better"); r.bold=True; r.font.size=Pt(18); r.font.color.rgb=RGBColor(0,0,0)
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run("Carlos Victor Montefusco-Pereira\nInformation Fusion submission package")
    heading(doc,"S1. Reproducibility protocol",1)
    para(doc,"All formal results use the declared 15-compound universe: five GDSC1 compounds, five GDSC2 compounds, and five CTD² compounds. Molecular features are expression, copy number, and damaging mutations. For each training fold, the top 2,000 features per modality are selected by training-set variance only. The model pipeline is median imputation, standardization, and Ridge regression with alpha=1.0. Fusion concatenates the three selected modality blocks (6,000 features).")
    para(doc,"Drug-heldout splits use GroupShuffleSplit with drug_id_raw as the grouping variable, test fraction 0.2, and persisted seeds 20260821, 20260822, and 20260823. Leave-one-dataset-out folds hold out CTD2, GDSC1, or GDSC2 in turn. RMSE and MAE are calculated on held-out response rows. The full-universe benchmark records model metrics and feature manifests; strict all-selected-feature missingness counts are not used as a performance filter, and model fitting uses median imputation.")
    heading(doc,"S2. Drug-heldout split manifests",1)
    table(doc,["Seed","Train drugs","Test drugs","Manifest"],[["20260821","12","3","drug_split_20260821.json"],["20260822","12","3","drug_split_20260822.json"],["20260823","12","3","drug_split_20260823.json"]])
    heading(doc,"S3. Drug-heldout results",1)
    rows=[]
    for seed in ["20260821","20260822","20260823"]:
        d=json.loads((ROOT/f"data/processed/full_universe_{seed}.json").read_text())
        for m in ["expression","copy_number","mutation","fusion"]:
            x=d["metrics"][m]; rows.append([seed,m,f"{x['mae']:.4f}",f"{x['rmse']:.4f}",x["feature_count"],x.get("complete_case_rows","not computed"),x.get("missing_case_rows","not computed")])
    table(doc,["Seed","Model","MAE","RMSE","Features","Complete","Missing"],rows)
    heading(doc,"S4. Leave-one-dataset-out results",1)
    d=json.loads((ROOT/"data/processed/full_universe_lood_results.json").read_text())
    rows=[]
    for held,fold in d["folds"].items():
        for m in ["expression","copy_number","mutation","fusion"]:
            x=fold["metrics"][m]; rows.append([held,m,fold["train_rows"],fold["test_rows"],f"{x['mae']:.4f}",f"{x['rmse']:.4f}",x.get("complete_case_rows","not computed"),x.get("missing_case_rows","not computed")])
    table(doc,["Held-out","Model","Train rows","Test rows","MAE","RMSE","Complete","Missing"],rows)
    heading(doc,"S5. Structured missingness and redundancy",1)
    para(doc,"The outer-joined tables preserve modality availability instead of silently restricting the analysis to complete cases. The summary below reports row-level availability and correlations between row means. These correlations are a compact redundancy audit, not a feature-level independence test.")
    d=json.loads((ROOT/"data/processed/structured_missingness_outer.json").read_text()); rows=[]
    for drug,x in d.items():
        c=x["row_mean_modality_correlations"]; rows.append([drug,x["rows"],f"{x['modality_row_availability']['expression']:.3f}",f"{x['modality_row_availability']['copy_number']:.3f}",f"{x['modality_row_availability']['mutation']:.3f}",f"{x['all_modality_complete_case_fraction']:.3f}",f"{c.get('copy_number__expression',0):+.3f}",f"{c.get('expression__mutation',0):+.3f}",f"{c.get('copy_number__mutation',0):+.3f}"])
    table(doc,["Drug","Rows","Expr avail.","CN avail.","Mut. avail.","All complete","CN–Expr","Expr–Mut.","CN–Mut."],rows)
    heading(doc,"S6. Exploratory uncertainty calibration",1)
    d=json.loads((ROOT/"data/processed/cross_dataset_missingness_summary.json").read_text()); rows=[]
    for ds,x in d["datasets"].items(): rows.append([ds,x["drugs"],f"{x['mean_coverage']:.3f}",f"{x['min_coverage']:.3f}",f"{x['max_coverage']:.3f}",x["at_or_above_nominal_90"]])
    table(doc,["Dataset","Drugs","Mean coverage","Min","Max","≥90%"],rows)
    para(doc,"This analysis is exploratory and is not part of the primary fusion benchmark. A nominal 90% coverage target was evaluated using fit/calibration/test partitions and 25% feature masking. Mean coverage was 0.911 across 15 drug evaluations, but coverage was not uniformly at or above nominal for every drug. These results do not establish a guaranteed interval and are not used for the primary performance claims.")
    heading(doc,"S7. Artifact and software manifest",1)
    table(doc,["Artifact","Role"],[["configs/dataset_manifest.yaml","Locked data releases and provenance"],["configs/requirements-release.txt","Runtime version pins"],["data/processed/drug_heldout_splits/","Persisted grouped split manifests"],["data/processed/drug_heldout_results_*.json","Formal repeated-seed metrics"],["data/processed/leave_one_dataset_out_results.json","Cross-study metrics"],["data/processed/modality_conflict_summary.json","Signed fusion-minus-expression deltas"],["scripts/run_drug_heldout_benchmark.py","Drug-heldout runner"],["scripts/run_leave_one_dataset_out.py","LOOD runner"],["scripts/audit_structured_missingness.py","Availability/redundancy audit"],["scripts/summarize_modality_conflict.py","Conflict summary"],["tests/","13 automated tests"]])
    heading(doc,"S8. Limitations and interpretation guardrails",1)
    para(doc,"The evaluation universe is small and prespecified rather than a complete drug screen. Drug identities do not broadly overlap across GDSC1, GDSC2, and CTD², so leave-one-dataset-out validation is cross-study transfer, not same-drug replication. The Ridge baseline is intentionally simple and does not establish the behavior of all fusion architectures. Outer-join availability reflects the prepared tables and should not be interpreted as a clinical assay-availability estimate. MoA mapping is complete for the declared 15 compounds but not for all 316 GDSC1 response compounds. No causal biological mechanism is inferred from the predictive comparisons.")
    OUT.parent.mkdir(exist_ok=True); doc.save(OUT); print(OUT)
if __name__ == "__main__": main()
