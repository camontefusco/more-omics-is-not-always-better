# Data specification — pre-analysis draft

## Candidate response resources

- GDSC1/GDSC2: primary pharmacogenomic screens with transcriptomic, mutation, and copy-number annotations.
- CCLE/DepMap: molecularly characterized cell lines and drug-response/dependency resources.
- CTRPv2 and gCSI: independent screens suitable for external validation and reproducibility checks.
- IMPROVE Benchmark or iDRR: standardized cross-study resources to be evaluated as benchmark inputs, not assumed to be interchangeable with the original screens.

## Proposed analysis unit

Cell-line × drug observations, harmonized by stable cell-line and compound identifiers. Response metric must be locked before modeling; AUC/activity-area and log potency metrics should not be mixed without an explicit conversion or sensitivity analysis.

## Required pre-modeling decisions

1. Exact release/version and download date for every resource.
2. Cell-line and drug identity harmonization rules.
3. Feature preprocessing and gene-universe intersection across datasets.
4. Leakage-controlled split design: cell-line-held-out, drug-held-out, pair-held-out, and cross-study tests.
5. Mechanism-of-action source and minimum stratum size.
6. Missingness mechanism: random masking, modality-availability patterns, and sensitivity to non-random missingness.
7. Primary metrics: rank correlation, error, calibration, and clinically interpretable decision utility.

## Current evidence constraint

Cross-study reproducibility is affected by response metric and experimental factors, so a model comparison that ignores assay and response-definition differences would confound modality value with measurement inconsistency.
