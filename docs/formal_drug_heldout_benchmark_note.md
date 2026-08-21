# Formal drug-held-out benchmark note

The combined 15-drug outer-joined table was evaluated with drug-grouped held-out splits at seeds 20260821, 20260822, and 20260823. Each fold selected 2,000 features per modality using training-drug rows only and fit expression, copy-number, mutation, and fusion Ridge models.

| Seed | Expression RMSE | Fusion RMSE | Fusion delta |
|---:|---:|---:|---:|
| 20260821 | 0.1481 | 0.1326 | −0.0155 |
| 20260822 | 0.2174 | 0.2148 | −0.0026 |
| 20260823 | 0.2535 | 0.2542 | +0.0007 |
| **Mean** | **0.2063** | **0.2005** | **−0.0058** |

Fusion improved pooled RMSE on two seeds and worsened slightly on one. This supports a modest, split-sensitive incremental effect rather than a universal fusion advantage.

The benchmark implementation is `scripts/run_drug_heldout_benchmark.py`; split manifests are written under `data/processed/drug_heldout_splits/`. The first seed has corrected modality-level availability strata; seeds 20260822–20260823 retain model metrics from the completed full-scale runs but require a later runtime pass to rewrite their corrected strata counts.
