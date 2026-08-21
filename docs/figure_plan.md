# Figure plan

## Main figures

1. Study design: locked datasets, modality intersection, grouped splits, and evaluation branches.
2. Incremental modality value: per-drug RMSE deltas for expression, copy number, mutation, and fusion.
3. Missingness calibration: coverage versus nominal target, stratified by dataset and drug.
4. Failure modes: modality conflict/redundancy and performance degradation under missingness.

## Supplementary figures

- Release and identifier harmonization flow.
- Cell-line and drug overlap across datasets.
- Sensitivity to masking fraction and random seed.
- MoA mapping coverage and confidence audit.

All figures must carry dataset, split, seed, feature-selection, and masking metadata in the accompanying machine-readable tables.
