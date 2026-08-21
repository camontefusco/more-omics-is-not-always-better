# Formal drug-held-out benchmark note

The combined 15-drug outer-joined table was evaluated with drug-grouped held-out splits at seeds 20260821, 20260822, and 20260823. Each fold selected 2,000 features per modality using training-drug rows only and fit expression, copy-number, mutation, and fusion Ridge models.

| Seed | Expression RMSE | Fusion RMSE | Fusion delta |
|---:|---:|---:|---:|
| 20260821 | 0.1481 | 0.1326 | −0.0155 |
| 20260822 | 0.2174 | 0.2148 | −0.0026 |
| 20260823 | 0.2535 | 0.2542 | +0.0007 |
| **Mean** | **0.2063** | **0.2005** | **−0.0058** |

Fusion improved pooled RMSE on two seeds and worsened slightly on one. This supports a modest, split-sensitive incremental effect rather than a universal fusion advantage.

The benchmark implementation is `scripts/run_drug_heldout_benchmark.py`; split manifests are written under `data/processed/drug_heldout_splits/`.

The corrected modality-level availability strata were independently recomputed from each persisted split manifest and the combined outer table. The resulting complete/missing/total test-row counts are:

| Seed | Complete | Missing | Total |
|---:|---:|---:|---:|
| 20260821 | 1,513 | 1,046 | 2,559 |
| 20260822 | 1,458 | 1,271 | 2,729 |
| 20260823 | 1,530 | 1,078 | 2,608 |

These counts replace the earlier first-feature-only diagnostic; they classify a row as complete only when all selected features for each modality are available.
