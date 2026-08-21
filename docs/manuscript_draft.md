# When More Omics Is Not Always Better: Drug- and Dataset-Conditional Value of Multimodal Cancer Pharmacogenomics

# Abstract

Multimodal molecular profiles are often assumed to improve cancer drug-response prediction simply by adding information. We developed an evidence-bounded DepMap workflow to test that assumption across expression, copy-number, and mutation features. The prespecified evaluation universe contained 15 compounds from GDSC1, GDSC2, and CTD². Models used fold-local feature selection and Ridge regression, with drug-held-out and leave-one-dataset-out validation.

In drug-held-out validation, fusion improved RMSE on two of three repeated splits, with mean RMSE 0.2005 versus 0.2063 for expression alone. In cross-study validation, fusion degraded RMSE on all three held-out datasets: CTD2 0.5649 versus 0.3276, GDSC1 0.3101 versus 0.2585, and GDSC2 0.2870 versus 0.2291. Structured missingness and weak-to-moderate row-level modality correlations indicate that additional modalities can introduce both incomplete observations and redundant or domain-sensitive signal. These findings support evaluating multimodal models by incremental value, transferability, and failure modes rather than assuming that more omics is always better.

**Keywords:** information fusion; drug response; multi-omics; cancer; missing data; cross-study validation

# 1. Introduction

Cancer pharmacogenomics increasingly combines multiple molecular assays to predict drug response. More measurements can capture complementary biology, but they also increase dimensionality, missingness, and sensitivity to study-specific measurement processes. We therefore prespecified a workflow that treats incremental predictive value, missingness, calibration, and modality conflict as joint evaluation targets.

## 1.1. Brief literature context

Large cell-line resources established the empirical basis for this task. The Cancer Cell Line Encyclopedia and the Genomics of Drug Sensitivity in Cancer linked molecular profiles to pharmacologic response across large panels, while later DepMap releases expanded standardized molecular and dependency data [1–3]. These resources also show why response prediction is not purely a genomic problem: lineage and multiple molecular data types contribute to drug sensitivity associations [2].

Prior computational work has used classical machine learning, deep learning, and multimodal integration for drug-response prediction [4–6]. MOLI is a prominent late-integration example that combines expression, copy-number, and mutation features and reported gains in external validations [5]. However, published comparisons often differ in response metric, drug universe, feature processing, split design, and external-study transfer. The present study addresses a narrower methodological question: whether adding modalities improves a fixed, leakage-controlled baseline under drug-heldout and cross-study evaluation. It is intended as a validation benchmark, not as a competing deep-learning model.

## 1.2. Research questions and hypotheses

We asked three questions: (Q1) Does feature-level fusion improve prediction when drugs, rather than cell lines alone, are held out? (Q2) Does any improvement transfer when an entire response dataset is held out? (Q3) Are fusion effects accompanied by structured missingness or modality redundancy? We preregistered the following directional expectations for interpretation: H1, fusion may improve drug-heldout prediction relative to expression alone; H2, fusion gains may not transfer across datasets; and H3, missingness and redundancy may vary across source datasets and coincide with unstable fusion effects. These are benchmark hypotheses, not claims of biological causality.

# 2. Methods

We harmonized DepMap response and molecular data from GDSC1, GDSC2, and CTD² using locked release identifiers. Expression, copy-number, and damaging-mutation features were evaluated separately and in concatenated fusion models. Within each held-out fold, the top 2,000 features per modality were selected using training rows only. Models used median imputation, standardization, and Ridge regression. Drug-held-out splits grouped rows by drug; leave-one-dataset-out folds held out each source dataset in turn. Outer joins were retained for structured missingness analyses.

## 2.1. Evaluation scope

The declared evaluation universe contains 15 compounds: five from GDSC1, five from GDSC2, and five from CTD². This is a prespecified cross-dataset subset, not the complete drug universe available in any one portal release. Because the datasets do not contain a broad common set of identical compounds, leave-one-dataset-out results measure cross-study transfer rather than same-drug replication.

## 2.2. Metrics and interpretation

We report mean absolute error (MAE) and root mean squared error (RMSE). Fusion deltas are defined as fusion RMSE minus expression RMSE; negative values favor fusion and positive values favor expression. Missingness strata are descriptive availability strata, not a replacement for imputation-aware model evaluation. All formal result tables and split manifests are versioned with the workflow.

# 3. Results

### 3.1. Drug-heldout validation

Drug-held-out performance was split-sensitive: fusion improved two of three seeds and worsened slightly on one. The mean RMSE difference was modest and should not be interpreted as a universal gain. Per-seed and per-model values are reported in Table 2 and Supplementary Table S3.

### 3.2. Cross-study transfer

In leave-one-dataset-out validation, expression was consistently stronger than fusion, with the largest fusion degradation on CTD2. These folds test transfer across source datasets, not replication of the same drug. The signed fusion-minus-expression RMSE deltas are shown in Figure 2 and Supplementary Table S4.

### 3.3. Missingness and redundancy

Row-level modality summaries showed weak-to-moderate correlations, while outer-joined tables showed dataset-dependent modality availability. These analyses describe data structure and model behavior; they do not establish that missingness or redundancy caused the observed performance differences.

# 4. Discussion

The results do not support a universal multimodal advantage. Fusion can help within a drug-held-out universe yet fail under study transfer, consistent with domain-specific response scales, assay coverage, and feature distributions. The study is limited by the small prespecified 15-drug universe, limited same-drug overlap across datasets, and the use of compact Ridge baselines rather than a broad model class. The conclusions are therefore about evaluation design and conditional predictive value, not a claim that any modality is biologically uninformative.

H1 was partially supported: fusion improved two of three drug-heldout seeds, but the effect was small and split-sensitive. H2 was supported in this evaluation: fusion degraded performance in all three leave-one-dataset-out folds. H3 was supported descriptively because modality availability and row-level correlations differed across source tables, but the study does not identify a causal explanation. These findings argue for reporting fusion failures alongside gains and for treating cross-study validation as a separate target from within-dataset drug generalization.

# 5. Data and code availability

Code, manifests, derived result summaries, figures, and reproducibility notes are provided in the private project repository. Raw DepMap files must be obtained from the provider under the applicable terms; see `docs/public_data_access_note.md`.

# 6. References

1. Barretina J, Caponigro G, Stransky N, et al. The Cancer Cell Line Encyclopedia enables predictive modelling of anticancer drug sensitivity. *Nature*. 2012;483:603–607. doi: [10.1038/nature11003](https://doi.org/10.1038/nature11003).
2. Iorio F, Knijnenburg TA, Vis DJ, et al. A landscape of pharmacogenomic interactions in cancer. *Cell*. 2016;166:740–754. doi: [10.1016/j.cell.2016.06.017](https://doi.org/10.1016/j.cell.2016.06.017).
3. Tsherniak A, Vazquez F, Montgomery PG, et al. Defining a cancer dependency map. *Cell*. 2017;170:564–576.e16. doi: [10.1016/j.cell.2017.06.010](https://doi.org/10.1016/j.cell.2017.06.010).
4. Azuaje F. Computational models for predicting drug responses in cancer research. *Brief Bioinform*. 2017;18:820–829. doi: [10.1093/bib/bbw065](https://doi.org/10.1093/bib/bbw065).
5. Sharifi-Noghabi H, Zolotareva O, Collins CC, Ester M. MOLI: multi-omics late integration with deep neural networks for drug response prediction. *Bioinformatics*. 2019;35:i501–i509. doi: [10.1093/bioinformatics/btz318](https://doi.org/10.1093/bioinformatics/btz318).
6. Cai Z, Poulos RC, Liu J, Zhong Q. Machine learning for multi-omics data integration in cancer. *iScience*. 2022;25:103798. doi: [10.1016/j.isci.2022.103798](https://doi.org/10.1016/j.isci.2022.103798).
7. DepMap. How should I cite DepMap data? DepMap Portal, updated 7 February 2025. [https://depmap.org/portal/resources](https://depmap.org/portal/resources?subcategory=commonly-asked-questions&topic=how-should-i-cite-depmap-data).
