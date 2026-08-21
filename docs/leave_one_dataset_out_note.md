# Leave-one-dataset-out validation

The combined 15-drug outer table was evaluated by holding out each source dataset in turn. For every fold, the held-out dataset was excluded from feature selection; Ridge models used the top 2,000 training-variance features per modality and a 6,000-feature concatenated fusion model. Results are persisted in `data/processed/leave_one_dataset_out_results.json`.

| Held-out dataset | Expression RMSE | Copy-number RMSE | Mutation RMSE | Fusion RMSE |
|---|---:|---:|---:|---:|
| CTD2 | 0.3276 | 0.3575 | 0.4048 | 0.5649 |
| GDSC1 | 0.2585 | 0.4121 | 0.5062 | 0.3101 |
| GDSC2 | 0.2291 | 0.4935 | 0.6469 | 0.2870 |

Fusion improves on expression for GDSC1 and GDSC2 but degrades substantially on CTD2. This is evidence that cross-study transfer is dataset-sensitive and does not support a universal multimodal advantage. These are cross-study validations, not same-drug replications: the declared 15-drug universe has limited overlap across source datasets.

The implementation is `scripts/run_leave_one_dataset_out.py`. Missingness strata are reported as complete versus missing rows using availability across all selected features in each modality; model fitting still uses median imputation within each training fold.
