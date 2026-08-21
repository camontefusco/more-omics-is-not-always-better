# Leave-one-dataset-out validation

The combined 15-drug outer table was evaluated by holding out each source dataset in turn. For every fold, the held-out dataset was excluded from feature selection; Ridge models selected the top 2,000 training-variance features per modality from the complete raw modality universe and used a 6,000-feature concatenated fusion model. Results are persisted in `data/processed/full_universe_lood_results.json`.

| Held-out dataset | Expression RMSE | Copy-number RMSE | Mutation RMSE | Fusion RMSE |
|---|---:|---:|---:|---:|
| CTD2 | 0.3231 | 0.3287 | 0.3325 | 0.3238 |
| GDSC1 | 0.2322 | 0.2353 | 0.2342 | 0.2339 |
| GDSC2 | 0.2347 | 0.2326 | 0.2406 | 0.2387 |

Fusion is slightly worse than expression in all three full-universe LOOD folds. This is evidence that cross-study transfer is dataset-sensitive and does not support a universal multimodal advantage. These are cross-study validations, not same-drug replications: the declared 15-drug universe has limited overlap across source datasets.

The implementation is `scripts/run_leave_one_dataset_out.py`. Missingness strata are reported as complete versus missing rows using availability across all selected features in each modality; model fitting still uses median imputation within each training fold.
