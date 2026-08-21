# When More Omics Is Not Always Better: Drug- and Dataset-Conditional Value of Multimodal Cancer Pharmacogenomics

# Abstract

Multimodal molecular profiles are often assumed to improve cancer drug-response prediction simply by adding information. We developed an evidence-bounded DepMap workflow to test that assumption across expression, copy-number, and mutation features. The prespecified evaluation universe contained 15 compounds from GDSC1, GDSC2, and CTD². Models used fold-local feature selection and Ridge regression, with drug-held-out and leave-one-dataset-out validation.

In full-universe drug-held-out validation, fusion produced a small RMSE improvement in all three repeated splits, with mean RMSE 0.2175 versus 0.2188 for expression alone. In cross-study validation, fusion was slightly worse in all three held-out datasets: CTD² 0.3238 versus 0.3231, GDSC1 0.2339 versus 0.2322, and GDSC2 0.2387 versus 0.2347. Structured missingness and weak-to-moderate row-level modality correlations indicate that additional modalities can introduce incomplete observations and domain-sensitive signal. These findings support evaluating multimodal models by incremental value, transferability, and failure modes rather than assuming that more omics is always better.

**Keywords:** information fusion; drug response; multi-omics; cancer; missing data; cross-study validation

# 1. Introduction

Cancer pharmacogenomics increasingly combines multiple molecular assays to predict drug response. More measurements can capture complementary biology, but they also increase dimensionality, missingness, and sensitivity to study-specific measurement processes. We therefore specified a workflow that treats incremental predictive value, missingness, and modality conflict as joint evaluation targets.

## 1.1. Brief literature context

Drug response is a heterogeneous phenotype shaped by lineage, genomic alterations, transcriptional state, assay conditions, and drug-specific mechanisms. The Cancer Cell Line Encyclopedia established a large-scale link between cancer cell-line molecular profiles and pharmacologic sensitivity [1]. The Genomics of Drug Sensitivity in Cancer subsequently provided a broad pharmacogenomic map across drugs and cell lines, showing that response associations are distributed across tissue context and molecular features rather than being reducible to a single biomarker class [2]. DepMap and related resources further consolidated molecular and functional measurements for systematic cancer-model analysis [3]. These resources made computational response prediction possible, but they also made the data-integration problem more visible: assays are not uniformly measured across all models, and response data are generated under source-specific experimental protocols.

The literature contains several complementary modeling strategies. Expression-only models have often been competitive because transcriptomic state captures pathway activity and lineage context, whereas mutation and copy-number features can provide sparse but mechanistically informative signals. Multimodal models combine these signals through early concatenation, late integration, multitask learning, or biologically structured architectures. MOLI, for example, integrates expression, copy-number, and mutation information through modality-specific encoders and reported gains in external validation [5]. DrugCell uses a biologically structured neural network and drug representations to model response and synergy [8], while other deep-learning frameworks have reported strong performance in cell-line settings and more variable transfer to clinical or external cohorts [9,10]. These results motivate multimodal integration, but they do not imply that adding an assay is beneficial under every population, response definition, or validation design.

There are three reasons to be cautious when comparing such results. First, the prediction target can change from continuous viability or IC50 to a binary responder label, making error metrics and biological interpretations non-equivalent [4,5]. Second, random splitting of cell-line–drug pairs can place related observations, or the same cell-line molecular profile, on both sides of a split; this can answer an easier question than prediction for an unseen drug or a new study. Recent work has explicitly identified leakage risks from random tuple splits in drug-response modeling [9]. Third, feature selection and preprocessing performed before validation can leak information from held-out observations even when model fitting itself is separated. These concerns are particularly important in high-dimensional multi-omics data, where dimensionality and preprocessing choices materially affect model behavior [6,7].

Published comparisons therefore leave a practical gap: it remains difficult to tell whether a reported multimodal gain reflects complementary biology, a favorable split, source-specific assay coverage, or preprocessing choices. Cross-study transfer is also less frequently treated as a primary test than within-dataset cross-validation, despite differences in response scales, cell-line coverage, and molecular measurement between screening resources. We address this gap with a deliberately modest benchmark: the same Ridge learner, the same feature budget, fold-local selection from the full raw modality universe, explicit single-modality baselines, drug-held-out evaluation, and leave-one-dataset-out transfer. The aim is not to outperform deep-learning systems, but to estimate the incremental value of adding modalities under a transparent and leakage-controlled comparison.

## 1.2. Research questions and hypotheses

We asked three questions: (Q1) Does feature-level fusion improve prediction when drugs, rather than cell lines alone, are held out? (Q2) Does any improvement transfer when an entire response dataset is held out? (Q3) Are fusion effects accompanied by structured missingness or modality redundancy? We specified the following directional expectations before interpreting the results: H1, fusion may improve drug-heldout prediction relative to expression alone; H2, fusion gains may not transfer across datasets; and H3, missingness and redundancy may vary across source datasets and coincide with unstable fusion effects. These are benchmark hypotheses, not claims of biological causality.

# 2. Methods

We harmonized DepMap response and molecular data from GDSC1, GDSC2, and CTD² using locked release identifiers. Expression, copy-number, and damaging-mutation features were evaluated separately and in concatenated early-fusion models. Within each held-out fold, the top 2,000 features per modality were selected from the full raw modality universe using training rows only. Models used median imputation, standardization, and Ridge regression. Drug-held-out splits grouped rows by drug; leave-one-dataset-out folds held out each source dataset in turn. Outer joins were retained for structured missingness analyses.

## 2.1. Evaluation scope

The declared evaluation universe contains 15 compounds: five from GDSC1, five from GDSC2, and five from CTD². This is a prespecified cross-dataset subset, not the complete drug universe available in any one portal release. Because the datasets do not contain a broad common set of identical compounds, leave-one-dataset-out results measure cross-study transfer rather than same-drug replication.

## 2.2. Metrics and interpretation

We report mean absolute error (MAE) and root mean squared error (RMSE). Fusion deltas are defined as fusion RMSE minus expression RMSE; negative values favor fusion and positive values favor expression. Missingness strata are descriptive availability strata, not a replacement for imputation-aware model evaluation. All formal result tables and split manifests are versioned with the workflow.

# 3. Results

### 3.1. Drug-heldout validation

Drug-held-out performance showed a small improvement in all three full-universe splits. Mean RMSE across seeds was 0.2175 for fusion versus 0.2188 for expression alone; this is an arithmetic mean of split-level RMSE values, not a pooled observation-level RMSE. Per-seed and per-model values are reported in Table 2 and Supplementary Table S3.

### 3.2. Cross-study transfer

In leave-one-dataset-out validation, expression was consistently stronger than fusion, with the largest fusion degradation on CTD2. These folds test transfer across source datasets, not replication of the same drug. The signed fusion-minus-expression RMSE deltas are shown in Figure 2 and Supplementary Table S4.

### 3.3. Missingness and redundancy

Row-level modality summaries showed weak-to-moderate correlations, while outer-joined tables showed dataset-dependent modality availability. These analyses describe data structure and model behavior; they do not establish that missingness or redundancy caused the observed performance differences.

# 4. Discussion

The results do not support a universal multimodal advantage. Fusion can help within a drug-held-out universe yet fail under study transfer, consistent with domain-specific response scales, assay coverage, and feature distributions. This pattern is compatible with prior reports that multimodal integration can improve prediction under particular data and validation settings [5,8], while benchmarking work shows variation across algorithms, drugs, and transfer targets [9,10]. Our controlled comparison adds a more modest observation: the incremental fusion effect is small within the declared drug-held-out benchmark and reverses direction under source-dataset transfer. This does not refute multimodal modeling; it shows why a gain observed in one validation regime should not be generalized to another without direct testing. The study is limited by the small prespecified 15-drug universe, limited same-drug overlap across datasets, and the use of compact Ridge baselines rather than a broad model class.

H1 was supported in the full-universe drug-heldout benchmark, although the improvement was small in every seed. H2 was supported in this evaluation: fusion degraded performance in all three leave-one-dataset-out folds. H3 was supported descriptively because modality availability and row-level correlations differed across source tables, but the study does not identify a causal explanation. These findings argue for reporting effect size and transfer failures alongside the direction of the fusion comparison.

The methodological implication is that validation design is part of the scientific claim. A random cell-line–drug split can estimate interpolation within an existing response system, whereas a drug-held-out split asks whether molecular features support prediction for compounds not represented in training. A leave-one-dataset-out split adds a different stress test: it asks whether the learned relationship survives a change in source, assay, and coverage. These estimands should not be conflated. Our study uses them sequentially to show that the answer to “does fusion help?” depends on which generalization target is intended.

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
8. Kuenzi BM, Park J, Fong SH, et al. Predicting drug response and synergy using a deep learning model of human cancer cells. *Cancer Cell*. 2020;38:672–684.e6. doi:10.1016/j.ccell.2020.09.014.
9. Chawla S, Rockstroh A, Lehman M, et al. Gene expression based inference of cancer drug sensitivity. *Nat Commun*. 2022;13:5680. doi:10.1038/s41467-022-33291-z.
10. Baptista D, Ferreira PG, Rocha M. Deep learning for drug response prediction in cancer. *Brief Bioinform*. 2023;24:bbac605. doi:10.1093/bib/bbac605.
