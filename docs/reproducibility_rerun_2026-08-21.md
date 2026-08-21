# Reproducibility rerun — 2026-08-21

The release runtime was verified with Python 3.12.2, NumPy 1.26.4, pandas 2.2.3, scikit-learn 1.9.0, and Matplotlib 3.10.6. The locked versions are recorded in `configs/requirements-release.txt`.

The full-universe leave-one-dataset-out workflow was rerun from the 578 MB combined outer table with fold-local selection from the complete raw feature universes and a 2,000-feature-per-modality budget. The frozen output is `data/processed/full_universe_lood_results.json`. The test suite passed 13 tests, and release figure artifact validation passed.

This is an isolated runtime verification using the recorded dependency versions. It does not redistribute raw DepMap files and does not claim same-drug replication across the three source datasets.
