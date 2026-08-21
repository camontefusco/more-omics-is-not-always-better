# Artifact classification

## Frozen and versioned

- `data/processed/leave_one_dataset_out_results.json`
- `data/processed/drug_heldout_results_20260821.json`, `20260822.json`, and `20260823.json`
- `data/processed/drug_heldout_splits/`
- `data/processed/cross_dataset_modality_seeds.json`
- `data/processed/cross_dataset_missingness_summary.json`
- `data/processed/structured_missingness_outer.json`
- `data/processed/structured_missingness_redundancy.json`
- `outputs/figures/lood_rmse.png`, `lood_rmse.pdf`, and `lood_rmse_source.json`

## Reproducible but not committed as release artifacts

The large outer-joined feature tables and selected-modality tables under `data/processed/*outer_tables/` and `data/processed/*top5_tables/` are derived intermediates. They can be regenerated from the locked raw-file manifest and scripts; they are not duplicated into the Git repository.

## Retained locally for audit

The remaining untracked JSON files are exploratory smoke, first-drug, or dataset-specific calibration outputs. They are retained locally and are not used for the final claims unless promoted by a later manifest update. No raw DepMap files are redistributed by this repository.
