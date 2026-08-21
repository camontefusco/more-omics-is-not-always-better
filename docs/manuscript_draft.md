# When More Omics Is Not Always Better: Drug- and Dataset-Conditional Value of Multimodal Cancer Pharmacogenomics

## Abstract

Multimodal molecular profiles are often assumed to improve cancer drug-response prediction simply by adding information. We developed an evidence-bounded DepMap workflow to test that assumption across expression, copy-number, and mutation features. The prespecified evaluation universe contained 15 compounds from GDSC1, GDSC2, and CTD². Models used fold-local feature selection and Ridge regression, with drug-held-out and leave-one-dataset-out validation.

In drug-held-out validation, fusion improved RMSE on two of three repeated splits, with mean RMSE 0.2005 versus 0.2063 for expression alone. In cross-study validation, fusion degraded RMSE on all three held-out datasets: CTD2 0.5649 versus 0.3276, GDSC1 0.3101 versus 0.2585, and GDSC2 0.2870 versus 0.2291. Structured missingness and weak-to-moderate row-level modality correlations indicate that additional modalities can introduce both incomplete observations and redundant or domain-sensitive signal. These findings support evaluating multimodal models by incremental value, transferability, and failure modes rather than assuming that more omics is always better.

## Introduction

Cancer pharmacogenomics increasingly combines multiple molecular assays to predict drug response. More measurements can capture complementary biology, but they also increase dimensionality, missingness, and sensitivity to study-specific measurement processes. We therefore prespecified a workflow that treats incremental predictive value, missingness, calibration, and modality conflict as joint evaluation targets.

## Methods

We harmonized DepMap response and molecular data from GDSC1, GDSC2, and CTD² using locked release identifiers. Expression, copy-number, and damaging-mutation features were evaluated separately and in concatenated fusion models. Within each held-out fold, the top 2,000 features per modality were selected using training rows only. Models used median imputation, standardization, and Ridge regression. Drug-held-out splits grouped rows by drug; leave-one-dataset-out folds held out each source dataset in turn. Outer joins were retained for structured missingness analyses.

## Results

Drug-held-out performance was split-sensitive: fusion improved two of three seeds and worsened slightly on one. In leave-one-dataset-out validation, expression was consistently stronger than fusion, with the largest fusion degradation on CTD2. The signed fusion-minus-expression RMSE deltas and all frozen metrics are available in the machine-readable result tables. Row-level modality summaries showed weak-to-moderate correlations, while outer-joined tables showed dataset-dependent modality availability.

## Discussion

The results do not support a universal multimodal advantage. Fusion can help within a drug-held-out universe yet fail under study transfer, consistent with domain-specific response scales, assay coverage, and feature distributions. The study is limited by the small prespecified 15-drug universe, limited same-drug overlap across datasets, and the use of compact Ridge baselines rather than a broad model class. The conclusions are therefore about evaluation design and conditional predictive value, not a claim that any modality is biologically uninformative.

## Data and code availability

Code, manifests, derived result summaries, figures, and reproducibility notes are provided in the private project repository. Raw DepMap files must be obtained from the provider under the applicable terms; see `docs/public_data_access_note.md`.
