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
- [x] Freeze software environment and record exact dependency versions.
- [x] Render and visually inspect the release validation figures; source data are committed alongside them.
- [x] Prepare a public-data access note that respects provider terms and does not redistribute restricted raw files.
- [x] Assemble the evidence-bounded manuscript draft.

## Current release decision

The repository is suitable for internal continuation and audit, with the evidence-bounded manuscript and release artifacts assembled. A final public release still requires an external licensing review and, if desired, expansion beyond the declared 15-compound universe.


## Zenodo release gate

- [x] Curate the final manuscript-supporting files and release metadata; see `docs/release_manifest_v1.0.0-jpbi-revision.txt`.
- [x] Exclude raw provider data, credentials, caches, and exploratory artifacts not required for reproduction.
- [ ] Create GitHub tag `v1.0.0-jpbi-revision`.
- [ ] Create a GitHub release from that tag.
- [ ] Enable this repository in Zenodo and archive the GitHub release.
- [ ] Record the version DOI and concept DOI in the manuscript, response letter, README, and `docs/public_data_access_note.md`.
- [ ] Verify that a clean clone plus permitted raw-data downloads can regenerate the frozen tables and figures.
