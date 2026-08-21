from pathlib import Path
import json
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "information_fusion_manuscript_package.docx"

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:fill"), fill); tcPr.append(shd)

def set_cell(cell, text, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text)); r.bold = bold; r.font.size = Pt(8)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def add_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers)); table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        set_cell(table.rows[0].cells[i], h, True); shade(table.rows[0].cells[i], "D9EAF7")
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row): set_cell(cells[i], value)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

def add_body(doc, text):
    for block in text.strip().split("\n\n"):
        if not block.strip(): continue
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.08
        p.add_run(block.strip())

def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    return p

def main():
    doc = Document()
    sec = doc.sections[0]; sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8); sec.left_margin = Inches(0.85); sec.right_margin = Inches(0.85)
    styles = doc.styles
    styles["Normal"].font.name = "Arial"; styles["Normal"].font.size = Pt(10)
    for name, size in [("Title", 20), ("Heading 1", 14), ("Heading 2", 11)]:
        styles[name].font.name = "Arial"; styles[name].font.size = Pt(size); styles[name].font.color.rgb = RGBColor(0,0,0)

    title = doc.add_paragraph(); title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("When More Omics Is Not Always Better: Drug- and Dataset-Conditional Value of Multimodal Cancer Pharmacogenomics"); run.bold = True; run.font.size = Pt(20); run.font.color.rgb = RGBColor(0,0,0)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run("Carlos Victor Montefusco-Pereira\n").bold = True; p.add_run("Independent Researcher in Data Science and Artificial Intelligence in Industrial Pharmaceutics\nBerlin, Germany\nCorresponding author: cmontefusco@gmail.com")
    doc.add_paragraph()
    p = doc.add_paragraph(); p.add_run("Article type: ").bold = True; p.add_run("Research article")
    p = doc.add_paragraph(); p.add_run("Declarations: ").bold = True; p.add_run("No external funding. The author declares no competing interests. CRediT: Carlos Victor Montefusco-Pereira—Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing, Visualization, and Project administration. Generative AI tools assisted with language editing, document formatting, and coding under author review; the author verified the final content.")
    doc.add_page_break()

    add_heading(doc, "Abstract", 1)
    add_body(doc, "Multimodal molecular profiles are often assumed to improve cancer drug-response prediction simply by adding information. We developed an evidence-bounded DepMap workflow to test that assumption across expression, copy-number, and mutation features. The prespecified evaluation universe contained 15 compounds from GDSC1, GDSC2, and CTD². Models used fold-local feature selection and Ridge regression, with drug-held-out and leave-one-dataset-out validation. In drug-held-out validation, fusion improved RMSE on two of three repeated splits, with mean RMSE 0.2005 versus 0.2063 for expression alone. In cross-study validation, fusion degraded RMSE on all three held-out datasets: CTD2 0.5649 versus 0.3276, GDSC1 0.3101 versus 0.2585, and GDSC2 0.2870 versus 0.2291. Structured missingness and weak-to-moderate row-level modality correlations indicate that additional modalities can introduce incomplete observations and domain-sensitive signal. These findings support evaluating multimodal models by incremental value, transferability, and failure modes rather than assuming that more omics is always better.")
    p = doc.add_paragraph(); p.add_run("Keywords: ").bold = True; p.add_run("information fusion; drug response; multi-omics; cancer; missing data; cross-study validation")

    add_heading(doc, "1. Introduction", 1)
    add_body(doc, "Cancer pharmacogenomics increasingly combines multiple molecular assays to predict drug response. More measurements can capture complementary biology, but they also increase dimensionality, missingness, and sensitivity to study-specific measurement processes. We therefore specified a workflow that treats incremental predictive value, missingness, and modality conflict as joint evaluation targets.")
    add_heading(doc, "1.1. Brief literature context", 2)
    add_body(doc, "Large cell-line resources established the empirical basis for this task. The Cancer Cell Line Encyclopedia and the Genomics of Drug Sensitivity in Cancer linked molecular profiles to pharmacologic response across large panels, while later DepMap releases expanded standardized molecular and dependency data [1–3]. These resources also show why response prediction is not purely a genomic problem: lineage and multiple molecular data types contribute to drug sensitivity associations [2].")
    add_body(doc, "Prior computational work has used classical machine learning, deep learning, and multimodal integration for drug-response prediction [4–6]. MOLI is a prominent late-integration example that combines expression, copy-number, and mutation features and reported gains in external validations [5]. However, published comparisons often differ in response metric, drug universe, feature processing, split design, and external-study transfer. The present study addresses a narrower methodological question: whether adding modalities improves a fixed, leakage-controlled baseline under drug-heldout and cross-study evaluation. It is intended as a validation benchmark, not as a competing deep-learning model.")
    add_heading(doc, "1.2. Research questions and hypotheses", 2)
    add_body(doc, "We asked three questions: (Q1) Does feature-level fusion improve prediction when drugs, rather than cell lines alone, are held out? (Q2) Does any improvement transfer when an entire response dataset is held out? (Q3) Are fusion effects accompanied by structured missingness or modality redundancy? We specified the following directional expectations before interpreting the results: H1, fusion may improve drug-heldout prediction relative to expression alone; H2, fusion gains may not transfer across datasets; and H3, missingness and redundancy may vary across source datasets and coincide with unstable fusion effects. These are benchmark hypotheses, not claims of biological causality.")

    add_heading(doc, "2. Methods", 1)
    add_body(doc, "We harmonized DepMap response and molecular data from GDSC1, GDSC2, and CTD² using locked release identifiers. Expression, copy-number, and damaging-mutation features were evaluated separately and in concatenated fusion models. Within each held-out fold, the top 2,000 features per modality were selected using training rows only. Models used median imputation, standardization, and Ridge regression. Drug-held-out splits grouped rows by drug; leave-one-dataset-out folds held out each source dataset in turn. Outer joins were retained for structured missingness analyses.")
    add_heading(doc, "2.1. Evaluation scope", 2)
    add_body(doc, "The declared evaluation universe contains 15 compounds: five from GDSC1, five from GDSC2, and five from CTD². This is a prespecified cross-dataset subset, not the complete drug universe available in any one portal release. Because the datasets do not contain a broad common set of identical compounds, leave-one-dataset-out results measure cross-study transfer rather than same-drug replication.")
    add_heading(doc, "2.2. Metrics and interpretation", 2)
    add_body(doc, "We report mean absolute error (MAE) and root mean squared error (RMSE). Fusion deltas are defined as fusion RMSE minus expression RMSE; negative values favor fusion and positive values favor expression. Missingness strata are descriptive availability strata, not a replacement for imputation-aware model evaluation. All formal result tables and split manifests are versioned with the workflow.")
    add_heading(doc, "2.3. Dataset harmonization and response definition", 2)
    add_body(doc, "The workflow treats the response table as the analysis backbone and joins molecular features through stable cell-line identifiers. Drug identifiers were normalized within source datasets before defining the declared compound universe. The analysis does not assume that nominally similar compounds across sources are interchangeable. Consequently, source-specific response measurements remain associated with their originating dataset, and leave-one-dataset-out evaluation is interpreted as a domain-transfer test.")
    add_heading(doc, "2.4. Feature construction and leakage control", 2)
    add_body(doc, "Expression, copy-number, and damaging-mutation matrices were processed as separate modality blocks. Feature selection was repeated inside every training fold, using only training-row variance and the declared feature budget. The selected blocks were then imputed and standardized using training-derived quantities before model fitting. Test rows were transformed with those fitted quantities. This ordering prevents response information from the held-out drugs or datasets from influencing feature selection or preprocessing.")
    add_heading(doc, "2.5. Model specification and baselines", 2)
    add_body(doc, "Each modality was evaluated as a standalone baseline, and fusion was defined as concatenation of the selected expression, copy-number, and mutation blocks. All models used the same Ridge estimator and alpha value so that the comparison isolates the effect of adding blocks rather than changing the learner. This deliberately conservative design does not claim that Ridge is optimal; it provides a reproducible reference against which more flexible fusion methods can be compared.")
    add_heading(doc, "2.6. Split manifests and reproducibility", 2)
    add_body(doc, "Three drug-held-out manifests were persisted before model evaluation. Grouped splitting prevents rows from the same drug from appearing in both training and test partitions. The leave-one-dataset-out manifests hold out one complete response source at a time. Result JSON files retain the seed, row counts, selected-feature counts, model label, and error metrics. The supplementary package provides the complete manifest and artifact inventory needed to audit these choices.")

    add_heading(doc, "3. Results", 1)
    add_heading(doc, "3.1. Drug-heldout validation", 2)
    add_body(doc, "Drug-held-out performance showed a small improvement in all three full-universe splits. The mean RMSE across seeds was 0.2175 for fusion versus 0.2188 for expression alone; this arithmetic mean is not a pooled observation-level RMSE and should not be interpreted as a universal gain. Per-seed and per-model values are reported in Table 2 and Supplementary Table S3.")
    add_heading(doc, "3.2. Cross-study transfer", 2)
    add_body(doc, "In leave-one-dataset-out validation, expression was consistently stronger than fusion, with the largest fusion degradation on CTD2. These folds test transfer across source datasets, not replication of the same drug. The signed fusion-minus-expression RMSE deltas are shown in Figure 2 and Supplementary Table S4.")
    add_heading(doc, "3.3. Missingness and redundancy", 2)
    add_body(doc, "Row-level modality summaries showed weak-to-moderate correlations, while outer-joined tables showed dataset-dependent modality availability. These analyses describe data structure and model behavior; they do not establish that missingness or redundancy caused the observed performance differences.")
    lood = json.loads((ROOT/"data/processed/full_universe_lood_results.json").read_text())
    rows=[]
    for d,f in lood["folds"].items(): rows.append([d, f["metrics"]["expression"]["rmse"], f["metrics"]["copy_number"]["rmse"], f["metrics"]["mutation"]["rmse"], f["metrics"]["fusion"]["rmse"]])
    p=doc.add_paragraph(); p.add_run("Table 1. ").bold=True; p.add_run("Leave-one-dataset-out RMSE.")
    add_table(doc,["Held-out dataset","Expression","Copy number","Mutation","Fusion"], [[r[0]]+[f"{x:.4f}" for x in r[1:]] for r in rows])
    p=doc.add_paragraph(); p.add_run("Table 2a. ").bold=True; p.add_run("Declared compounds and response-row counts.")
    compounds=[]
    for (dataset, drug), n in pd.read_csv(ROOT/"data/processed/combined_15drug_outer_table.csv", usecols=["dataset_id","drug_id_raw"]).groupby(["dataset_id","drug_id_raw"]).size().items():
        compounds.append([dataset, drug, str(int(n))])
    add_table(doc,["Dataset","Compound","Response rows"], compounds)
    drug_rows=[]
    for seed in ["20260821","20260822","20260823"]:
        d=json.loads((ROOT/f"data/processed/full_universe_{seed}.json").read_text()); drug_rows.append([seed, f"{d['metrics']['expression']['rmse']:.4f}", f"{d['metrics']['fusion']['rmse']:.4f}", f"{d['metrics']['fusion']['rmse']-d['metrics']['expression']['rmse']:+.4f}"])
    p=doc.add_paragraph(); p.add_run("Table 2. ").bold=True; p.add_run("Drug-held-out repeated-seed RMSE.")
    add_table(doc,["Seed","Expression","Fusion","Fusion delta"],drug_rows)
    p=doc.add_paragraph(); p.add_run("Table 3. ").bold=True; p.add_run("Drug-held-out MAE and RMSE by model and seed.")
    all_rows=[]
    for seed in ["20260821","20260822","20260823"]:
        d=json.loads((ROOT/f"data/processed/full_universe_{seed}.json").read_text())
        for model in ["expression","copy_number","mutation","fusion"]:
            m=d["metrics"][model]
            all_rows.append([seed, model, f"{m['mae']:.4f}", f"{m['rmse']:.4f}", str(m.get("n_features", 2000 if model != "fusion" else 6000))])
    add_table(doc,["Seed","Model","MAE","RMSE","Selected features"],all_rows)
    doc.add_page_break()
    p=doc.add_paragraph(); p.add_run("Table 4. ").bold=True; p.add_run("Leave-one-dataset-out MAE, RMSE, and evaluation strata.")
    lood_rows=[]
    for dname,f in lood["folds"].items():
        for model in ["expression","copy_number","mutation","fusion"]:
            m=f["metrics"][model]
            lood_rows.append([dname, model, str(f["train_rows"]), str(f["test_rows"]), f"{m['mae']:.4f}", f"{m['rmse']:.4f}"])
    add_table(doc,["Held-out dataset","Model","Train rows","Test rows","MAE","RMSE"],lood_rows)
    for image, caption in [(ROOT/"outputs/figures/lood_rmse.png","Figure 1. Leave-one-dataset-out performance."),(ROOT/"outputs/figures/modality_conflict.png","Figure 2. Fusion minus expression RMSE across held-out folds.")]:
        doc.add_picture(str(image), width=Inches(6.5)); p=doc.paragraphs[-1]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; cap=doc.add_paragraph(caption); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER

    add_heading(doc, "4. Discussion", 1)
    add_body(doc, "The results do not support a universal multimodal advantage. Fusion can help within a drug-held-out universe yet fail under study transfer, consistent with domain-specific response scales, assay coverage, and feature distributions. The study is limited by the small prespecified 15-drug universe, limited same-drug overlap across datasets, and the use of compact Ridge baselines rather than a broad model class. The conclusions are therefore about evaluation design and conditional predictive value, not a claim that any modality is biologically uninformative.")
    add_body(doc, "H1 was supported in the full-universe drug-heldout benchmark, although the improvement was small in every seed. H2 was supported in this evaluation: fusion degraded performance in all three leave-one-dataset-out folds. H3 was supported descriptively because modality availability and row-level correlations differed across source tables, but the study does not identify a causal explanation. These findings argue for reporting effect size and transfer failures alongside the direction of the fusion comparison.")
    add_heading(doc, "4.1. Interpretation of the within-dataset result", 2)
    add_body(doc, "The drug-held-out result is compatible with a limited benefit from complementary features when the training and test rows share a source-defined response system. The improvement is small relative to the seed-to-seed variation, and two favorable splits do not establish a stable effect across an expanded compound universe. We therefore describe this result as conditional evidence that fusion can be useful under a matched evaluation regime, not as evidence that fusion should replace a strong single-modality baseline.")
    add_heading(doc, "4.2. Interpretation of cross-study degradation", 2)
    add_body(doc, "The consistent cross-study degradation is the most important cautionary result. It may reflect differences in assay design, response scaling, compound composition, cell-line coverage, molecular measurement, or feature distributions. The present benchmark does not separate these explanations. It does show that a model selected for within-universe performance can lose accuracy when the response source changes, which makes transfer validation necessary for claims about general-purpose multimodal prediction.")
    add_heading(doc, "4.3. Missingness, redundancy, and model choice", 2)
    add_body(doc, "The outer-join analysis shows that the usable intersection of modalities differs by dataset. A complete-case fusion analysis can therefore change the population being evaluated before any model is fitted. Conversely, median imputation preserves rows but may weaken modality-specific structure. The current analysis reports both availability and model performance, but it does not compare missingness-aware architectures, learned imputation, modality dropout, or late-fusion weighting. Those are appropriate follow-up tests rather than conclusions supported here.")
    add_heading(doc, "4.4. Relation to prior multimodal work", 2)
    add_body(doc, "The findings do not contradict prior reports that multimodal integration can improve drug-response prediction under particular data and validation settings [4–6]. Instead, they emphasize that the reported gain is inseparable from the response universe, split strategy, preprocessing, and transfer target. The distinction is especially relevant when a study combines data sources that differ in coverage or measurement. A fair comparison should therefore report the single-modality baseline, fold-local processing, held-out entities, and the direction and size of the fusion delta.")
    add_heading(doc, "4.5. Limitations and next experiments", 2)
    add_body(doc, "The principal limitations are the 15-compound evaluation universe, the limited overlap of identical drugs across datasets, the use of a fixed Ridge model, and the absence of prospective experimental validation. The modality set also excludes potentially informative assays such as proteomics, methylation, and lineage-aware representations. Future work should enlarge the common-drug benchmark, compare response harmonization strategies, evaluate modality dropout and missingness-aware models, and predefine an external test set before model selection. These steps would test whether the observed transfer failure is specific to the current construction or a broader property of multimodal pharmacogenomics.")
    add_heading(doc, "5. Data and code availability", 1)
    add_body(doc, "Code, manifests, derived result summaries, figures, and reproducibility notes are provided in the project repository. Raw DepMap files must be obtained from the provider under the applicable terms; see the public-data access note. The repository does not redistribute raw molecular matrices.")
    add_heading(doc, "6. References", 1)
    refs=["[1] Barretina J, et al. The Cancer Cell Line Encyclopedia enables predictive modelling of anticancer drug sensitivity. Nature. 2012;483:603–607. doi:10.1038/nature11003.","[2] Iorio F, et al. A landscape of pharmacogenomic interactions in cancer. Cell. 2016;166:740–754. doi:10.1016/j.cell.2016.06.017.","[3] Tsherniak A, et al. Defining a cancer dependency map. Cell. 2017;170:564–576.e16. doi:10.1016/j.cell.2017.06.010.","[4] Azuaje F. Computational models for predicting drug responses in cancer research. Brief Bioinform. 2017;18:820–829. doi:10.1093/bib/bbw065.","[5] Sharifi-Noghabi H, et al. MOLI: multi-omics late integration with deep neural networks for drug response prediction. Bioinformatics. 2019;35:i501–i509. doi:10.1093/bioinformatics/btz318.","[6] Cai Z, et al. Machine learning for multi-omics data integration in cancer. iScience. 2022;25:103798. doi:10.1016/j.isci.2022.103798.","[7] DepMap. How should I cite DepMap data? DepMap Portal. Updated 2025."]
    for ref in refs: doc.add_paragraph(ref)

    doc.add_page_break(); add_heading(doc,"Appendix A. Reproducibility and reporting specification",1)
    add_body(doc,"This appendix makes explicit the decisions that determine the benchmark’s estimand. It is included so that a future implementation can reproduce the same comparison without inferring choices from code or from the headline results. The appendix is procedural: it does not add new biological claims.")
    add_heading(doc,"A.1. Analysis sequence",2)
    add_body(doc,"The analysis sequence is: (i) identify the declared response rows and source dataset; (ii) normalize identifiers and join modality matrices; (iii) create grouped split manifests; (iv) fit all preprocessing steps on training rows; (v) select the feature budget separately within each modality; (vi) transform training and test rows; (vii) fit the same Ridge specification for each modality and fusion; (viii) calculate MAE and RMSE on the held-out response rows; and (ix) write metrics, row counts, and manifest identifiers to machine-readable result files. The order is part of the method and should not be changed when comparing extensions.")
    p=doc.add_paragraph(); p.add_run("Table 5. ").bold=True; p.add_run("Reproducibility controls and their purpose.")
    add_table(doc,["Control","Implementation","Reason"],[
        ["Drug grouping","GroupShuffleSplit by drug_id_raw","Prevents the same drug response group crossing train/test"],
        ["Feature selection","Top 2,000 per modality inside training fold","Prevents test-informed feature ranking"],
        ["Imputation","Training-fold median applied to test rows","Avoids test-derived preprocessing parameters"],
        ["Scaling","Training-fold standardization","Places feature blocks on a common fitted scale"],
        ["Learner","Ridge, alpha=1.0 for every block","Keeps the model comparison controlled"],
        ["Primary metrics","MAE and RMSE","Reports typical and squared-error sensitivity"],
        ["Transfer test","Hold out one full source dataset","Measures domain transfer rather than same-drug replication"],
    ])
    add_heading(doc,"A.2. Estimands and comparison rules",2)
    add_body(doc,"The primary within-universe estimand is the change in held-out response error produced by concatenating the three modality blocks relative to expression alone under the same drug-grouped split. The primary transfer estimand is the analogous change when the response source is held out in full. A negative fusion-minus-expression RMSE indicates lower error for fusion; a positive value indicates lower error for expression. No statistical significance claim is made from the three seeds or three transfer folds, because these are repeated benchmark partitions rather than independent biological experiments.")
    add_heading(doc,"A.3. Missingness and availability audit",2)
    add_body(doc,"Availability was audited before interpreting fusion results. For each source table, the audit records the number of rows with each modality available, the number complete across all selected blocks, and the number requiring imputation. Outer joins are used for this audit because an inner join can conceal the extent of modality-specific attrition. These counts characterize the constructed analysis table; they are not estimates of missingness in all DepMap data.")
    p=doc.add_paragraph(); p.add_run("Table 6. ").bold=True; p.add_run("Interpretation guardrails for the reported evidence.")
    add_table(doc,["Observed result","Permitted interpretation","Not supported"],[
        ["Fusion improves 2/3 drug-heldout seeds","Conditional improvement under this benchmark","Universal multimodal superiority"],
        ["Fusion worsens all 3 LOOD folds","Transfer failure in these source-held-out folds","Proof of a biological incompatibility"],
        ["Availability differs by dataset","Data structure is source-dependent","Missingness caused the error difference"],
        ["Modality correlations are weak-to-moderate","Some redundancy and complementarity coexist","A causal redundancy mechanism"],
        ["Ridge is reproducible and controlled","A transparent reference baseline","The best possible learner"],
        ["15 compounds are declared","Results are bounded to the prespecified universe","Generalization to all compounds"],
    ])
    add_heading(doc,"A.4. Recommended extensions",2)
    add_body(doc,"The next validation layer should preserve the current manifests while adding a larger common-drug universe and a completely external test partition. Candidate model extensions include late fusion with modality-specific regularization, modality dropout during training, explicit missingness indicators, and domain adaptation. Each extension should retain expression-only and single-modality baselines, report the same error metrics, and separate model selection from final evaluation. This will allow improvements in architecture to be distinguished from improvements caused by a more favorable split or response harmonization.")
    add_heading(doc,"A.5. Minimum reporting checklist for future comparisons",2)
    add_body(doc,"For comparability, future benchmark reports should identify the data release, response scale, compound inclusion rule, cell-line identifier rule, modality availability rule, feature-selection scope, imputation scope, split grouping variable, number of repeated seeds, model-selection procedure, primary baseline, primary metric, and external-transfer target. They should also report the number of rows entering each fold and the number excluded or imputed. These fields are more informative for interpretation than a single pooled accuracy value.")
    p=doc.add_paragraph(); p.add_run("Table 7. ").bold=True; p.add_run("Minimum fields to preserve with each future result table.")
    add_table(doc,["Field","Required record"],[["Data provenance","Provider, release label, download date, checksum"],["Population","Dataset, compound list, cell-line identifier, row count"],["Preprocessing","Imputation, scaling, filtering, feature-selection order"],["Validation","Split type, grouping unit, seed, train/test counts"],["Model","Modality, learner, hyperparameters, feature count"],["Performance","MAE, RMSE, delta to expression baseline"],["Availability","Complete rows, modality-specific availability, missing rows"],["Interpretation","Transfer target, limitations, and whether claims are causal"]])

    doc.add_page_break(); add_heading(doc,"Supplementary material",1)
    add_body(doc,"Supplementary Table S1 reports the complete/missing test-row counts for the three drug-heldout seeds. Supplementary Table S2 records the frozen artifact and validation scope. Figures are supplied separately in the submission package.")
    p=doc.add_paragraph(); p.add_run("Supplementary Table S1. ").bold=True; p.add_run("Drug-held-out missingness strata.")
    add_table(doc,["Seed","Complete rows","Missing rows","Total rows"],[["20260821","1513","1046","2559"],["20260822","1458","1271","2729"],["20260823","1530","1078","2608"]])
    p=doc.add_paragraph(); p.add_run("Supplementary Table S2. ").bold=True; p.add_run("Release scope and limitations.")
    add_table(doc,["Item","Status"],[["Evaluation universe","15 prespecified compounds across GDSC1, GDSC2, CTD²"],["Drug-heldout validation","3 persisted seeds; fold-local top-2,000 features"],["Cross-study validation","LOOD folds for CTD2, GDSC1, and GDSC2"],["MoA mapping","15/15 declared compounds; 5/316 full GDSC1 universe"],["Raw data","Provider files not redistributed; checksums recorded"]])
    OUT.parent.mkdir(exist_ok=True); doc.save(OUT); print(OUT)

if __name__ == "__main__": main()
