# Formal drug-held-out benchmark note

The combined 15-drug outer-joined table was evaluated with drug-grouped held-out splits at seeds 20260821, 20260822, and 20260823. Each fold selected 2,000 features per modality from the complete raw feature universe using training-drug rows only and fit expression, copy-number, mutation, and fusion Ridge models.

| Seed | Expression RMSE | Fusion RMSE | Fusion delta |
|---:|---:|---:|---:|
| 20260821 | 0.1696 | 0.1672 | −0.0024 |
| 20260822 | 0.2538 | 0.2527 | −0.0011 |
| 20260823 | 0.2329 | 0.2326 | −0.0003 |
| **Mean** | **0.2188** | **0.2175** | **−0.0013** |

Fusion improved seed-level RMSE slightly on all three splits. The reported mean is the arithmetic mean of split-level RMSE values, not a pooled observation-level RMSE. This supports a small incremental effect rather than a universal fusion advantage.

The benchmark implementation is `scripts/run_full_universe_benchmark.py`; split manifests are written under `data/processed/full_universe_manifests/`.

The corrected modality-level availability strata were independently recomputed from each persisted split manifest and the combined outer table. The resulting complete/missing/total test-row counts are:

| Seed | Complete | Missing | Total |
|---:|---:|---:|---:|
| 20260821 | 0 | 2,559 | 2,559 |
| 20260822 | 0 | 2,729 | 2,729 |
| 20260823 | 0 | 2,608 | 2,608 |

These counts replace the earlier any-feature diagnostic; they classify a row as complete only when all selected features for each modality are available. Under this strict definition, no drug-heldout test row is complete across the full 2,000-feature blocks, so these strata should not be interpreted as evidence that the model had no usable information: the models use median imputation and retain the rows.
