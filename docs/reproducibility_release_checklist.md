# Reproducibility release checklist

## Present

- [x] Private GitHub repository with pinned commit history.
- [x] Locked dataset manifest and release identifiers.
- [x] Raw-file provenance and SHA-256 checksums.
- [x] Identifier harmonization, validation, and grouped split scripts.
- [x] Train-only feature selection.
- [x] Baseline, modality, missingness, and aggregation scripts.
- [x] Automated test suite: 12 passing tests.
- [x] Cross-dataset exploratory notes and evidence-bounded manuscript/figure plans.

## Required before public release or submission

- [ ] Replace exploratory JSON-only outputs with versioned result tables and figure source data.
- [ ] Complete authoritative MoA mapping for the prespecified analysis universe.
- [ ] Add repeated-seed cross-dataset modality outputs to the formal results manifest.
- [ ] Add drug-held-out and cross-study validation results.
- [ ] Add conflict/redundancy and missing-modality pattern analyses.
- [ ] Freeze software environment and record exact dependency versions.
- [ ] Render and visually inspect all main and supplementary figures.
- [ ] Prepare a public-data access note that respects provider terms and does not redistribute restricted raw files.

## Current release decision

The repository is suitable for internal continuation and audit. It is not yet suitable as a final public research release because MoA coverage, formal result tables, and the final figure/manuscript package are incomplete.
