# Pre-analysis plan — draft for lock

## Primary estimand

For each drug and mechanism-of-action stratum, estimate the incremental predictive value of adding mutation and copy-number features to a transcriptomic baseline, with uncertainty intervals and external validation. The estimand is the paired performance difference under the same split, preprocessing, and model family.

## Primary comparisons

1. Transcriptomics alone.
2. Mutation alone.
3. Copy number alone.
4. Transcriptomics + mutation.
5. Transcriptomics + copy number.
6. Transcriptomics + mutation + copy number.

Drug descriptors may be included only in a clearly separated secondary analysis because drug-feature leakage and drug-held-out generalization change the scientific question.

## Validation hierarchy

- Pair-held-out: baseline discrimination within the observed drug/cell-line domain.
- Cell-line-held-out: generalization to unseen biological samples.
- Drug-held-out: generalization to unseen compounds.
- Cross-study: train on one screen and test on another, with assay and response metric recorded.

## Primary outcomes

- Spearman correlation for ranking response.
- MAE or RMSE for absolute error.
- Calibration error and interval coverage for uncertainty-aware predictions.
- Paired incremental performance by drug and mechanism-of-action stratum.

## Trustworthy fusion analyses

- Missing-modality stress tests under random and structured missingness.
- Conflict analysis when modalities imply discordant predictions.
- Redundancy analysis using conditional performance and feature perturbation.
- Stability of conclusions across seeds, splits, response metrics, and datasets.

## Exclusions from the primary claim

The study will not claim that one modality is universally biologically superior, that cell-line results directly establish patient benefit, or that a complex architecture is clinically deployable. It will report where modality value is conditional, uncertain, or non-reproducible.
