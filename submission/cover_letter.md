# Cover letter — Information Fusion

Dear Editors,

We submit “When More Omics Is Not Always Better: Drug- and Dataset-Conditional Value of Multimodal Cancer Pharmacogenomics” as a Research article. The study evaluates multimodal information fusion for cancer drug-response prediction using a locked 15-compound universe spanning GDSC1, GDSC2, and CTD².

The manuscript fits Information Fusion because it studies feature-level fusion in an imperfect and incomplete biomedical environment, with explicit attention to missingness, redundancy, algorithmic comparison, and cross-source transfer. The central finding is that fusion is conditional: it produced a small improvement in all three full-universe drug-heldout splits but was slightly worse in all three leave-one-dataset-out folds.

State of the art: the study is positioned against CCLE/GDSC pharmacogenomic resources, multimodal drug-response methods including MOLI, and machine-learning benchmarks of multi-omics integration [Barretina et al., 2012; Iorio et al., 2016; Tsherniak et al., 2017; Azuaje, 2017; Sharifi-Noghabi et al., 2019; Cai et al., 2022]. The contribution is evaluation design and evidence-bounded comparison, not a claim of a new deep-learning architecture.

Public datasets: common resources include CCLE/DepMap and GDSC. We used DepMap response and molecular releases for GDSC1, GDSC2, and CTD², with release identifiers and checksums recorded in the repository. Raw files are not redistributed.

Validation: standard response-prediction measures include RMSE and MAE; we report both. We applied drug-grouped heldout splits across three seeds, fold-local feature selection, and leave-one-dataset-out validation. We also report structured missingness strata and modality redundancy summaries.

Main claim and significance: adding modalities should be judged by incremental value and transferability rather than dimensionality alone. The finding that fusion fails under cross-study transfer is directly relevant to information-fusion systems operating across heterogeneous sources.

Evidence: all formal splits, feature-selection rules, derived result tables, figures, tests, and an identical reproducibility rerun are versioned in the repository. Raw provider files are not redistributed. The manuscript explicitly limits claims to the prespecified 15-compound universe and identifies the lack of broad same-drug cross-study replication as a limitation.

This manuscript has not been published previously and is not under consideration elsewhere. All authors will approve the submitted version and authorship list before submission.

Sincerely,

**Carlos Victor Montefusco-Pereira**
