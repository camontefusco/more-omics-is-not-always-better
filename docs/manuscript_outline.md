# Manuscript outline — evidence-bounded draft

## Working title

When More Omics Is Not Always Better: Drug- and Dataset-Conditional Value of Multimodal Cancer Pharmacogenomics

## Central claim to test

Additional molecular modalities should be evaluated by incremental predictive value, calibration, redundancy, and failure under missingness—not assumed beneficial because they increase input dimensionality.

## Results currently support

1. A locked, reproducible DepMap-based workflow spanning GDSC1, GDSC2, and CTD² response tables and three molecular modalities.
2. Exploratory GDSC1 fusion baselines improved RMSE over expression alone for the five selected compounds.
3. Masked uncertainty calibration is materially better than the initial unmasked calibration procedure.
4. Calibration varies by drug and dataset: pooled mean coverage was 91.1%, but only 8/15 drug-level evaluations met nominal 90% coverage.

## Claims currently blocked

- A universal 90% uncertainty guarantee.
- Mechanism-stratified conclusions for the full response universe; only 5/316 GDSC1 compounds currently have audited MoA mappings.
- Confirmatory superiority of multimodal fusion across all drugs or datasets.

## Required final analyses

- Expand and source the MoA mapping for the prespecified analysis universe.
- Repeat modality comparisons across seeds and response datasets.
- Add drug-held-out and cross-study performance summaries.
- Add conflict/redundancy analyses and calibration-stratified figures.
