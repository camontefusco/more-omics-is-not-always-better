# Work packages

## Bulk 1 — Study scaffold and novelty gate

- Establish repository structure and reproducibility rules.
- Search and verify the literature on multimodal cancer drug-response prediction, modality contribution, missing modalities, uncertainty, mechanism-of-action stratification, and cross-dataset reproducibility.
- Build a source-grounded literature matrix.
- Rewrite the novelty statement conservatively before modeling.

## Bulk 2 — Data and pharmacology specification

- Lock dataset versions and access routes for GDSC, CCLE/DepMap, CTRP, and gCSI where appropriate.
- Define drug mechanism-of-action strata and inclusion criteria.
- Specify cell-line and drug identity harmonization.
- Write the analysis plan before downloading large datasets.

## Bulk 3 — Baselines and unimodal models

- Implement leakage-controlled splits and preprocessing.
- Train transcriptomic, mutation, copy-number, and clinical/drug-only baselines.
- Establish calibration and uncertainty metrics.

## Bulk 4 — Fusion, ablation, and missing-modality experiments

- Compare early/late/simple established fusion strategies.
- Quantify incremental value and conflict/redundancy.
- Simulate missing modalities and evaluate graceful degradation.

## Bulk 5 — External validation and interpretation

- Repeat locked analyses across independent screens.
- Stratify results by mechanism of action and pharmacological class.
- Assess robustness, calibration, distribution shift, and clinically meaningful operating points.

## Bulk 6 — Manuscript and reproducibility package

- Freeze results and provenance.
- Produce figures, tables, supplement, codebook, and manuscript.
- Run final reference, data, and computational audits.
