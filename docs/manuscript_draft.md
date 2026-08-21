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

# 2. Methods

We harmonized DepMap response and molecular data from GDSC1, GDSC2, and CTD² using locked release identifiers. Expression, copy-number, and damaging-mutation features were evaluated separately and in concatenated fusion models. Within each held-out fold, the top 2,000 features per modality were selected using training rows only. Models used median imputation, standardization, and Ridge regression. Drug-held-out splits grouped rows by drug; leave-one-dataset-out folds held out each source dataset in turn. Outer joins were retained for structured missingness analyses.

# 3. Results

Drug-held-out performance was split-sensitive: fusion improved two of three seeds and worsened slightly on one. In leave-one-dataset-out validation, expression was consistently stronger than fusion, with the largest fusion degradation on CTD2. The signed fusion-minus-expression RMSE deltas and all frozen metrics are available in the machine-readable result tables. Row-level modality summaries showed weak-to-moderate correlations, while outer-joined tables showed dataset-dependent modality availability.

# 4. Discussion

The results do not support a universal multimodal advantage. Fusion can help within a drug-held-out universe yet fail under study transfer, consistent with domain-specific response scales, assay coverage, and feature distributions. The study is limited by the small prespecified 15-drug universe, limited same-drug overlap across datasets, and the use of compact Ridge baselines rather than a broad model class. The conclusions are therefore about evaluation design and conditional predictive value, not a claim that any modality is biologically uninformative.

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
