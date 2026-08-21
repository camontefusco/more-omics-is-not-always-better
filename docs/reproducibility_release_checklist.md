# Reproducibility release checklist

## Present

- [x] Private GitHub repository with pinned commit history.
- [x] Locked dataset manifest and release identifiers.
- [x] Raw-file provenance and SHA-256 checksums.
- [x] Identifier harmonization, validation, and grouped split scripts.
- [x] Train-only feature selection.
- [x] Baseline, modality, missingness, and aggregation scripts.
- [x] Automated test suite: 13 passing tests.
- [x] Cross-dataset exploratory notes and evidence-bounded manuscript/figure plans.

## Required before public release or submission

- [x] Version formal drug-held-out and leave-one-dataset-out result tables and manifests.
- [x] Complete MoA mapping for the declared 15-compound evaluation universe; retain the 5/316 full-GDSC1 limitation.
- [x] Add repeated-seed cross-dataset modality outputs to the formal results record.
- [x] Add drug-held-out and cross-study validation results.
- [x] Add structured missingness and modality redundancy summaries.
- [x] Add model disagreement/conflict cases to the final results and figure source data.
- [ ] Freeze software environment and record exact dependency versions.
- [ ] Render and visually inspect all main and supplementary figures.
- [ ] Prepare a public-data access note that respects provider terms and does not redistribute restricted raw files.

## Current release decision

The repository is suitable for internal continuation and audit. It is not yet a final public research release: clean-environment rerun, figure QA, manuscript assembly, public-data access documentation, and model-disagreement analysis remain open.
