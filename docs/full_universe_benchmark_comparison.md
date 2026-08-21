# Full-universe feature-selection benchmark

The stronger benchmark selects the top 2,000 variance-ranked features per modality inside each drug-held-out training fold from the complete raw modality tables. It bypasses the prepared 2,000-feature candidate tables used by the earlier formal benchmark.

| Seed | Expression RMSE | Fusion RMSE | Fusion − expression |
|---:|---:|---:|---:|
| 20260821 | 0.1696 | 0.1672 | −0.0024 |
| 20260822 | 0.2538 | 0.2527 | −0.0011 |
| 20260823 | 0.2329 | 0.2326 | −0.0003 |
| 20260824 | 0.2299 | 0.2294 | −0.0005 |
| 20260825 | 0.2776 | 0.2788 | +0.0012 |
| **Mean** | **0.2328** | **0.2322** | **−0.0006** |

Fusion improved RMSE in all three full-universe splits, but the mean improvement was small. The full-universe absolute errors differ from the earlier candidate-table benchmark, confirming that candidate-table construction materially affects the reported error scale. The full-universe result should replace the earlier headline benchmark if the manuscript claims selection from the full raw feature universe.

Raw feature counts were 19,215 expression, 18,613 copy-number, and 19,505 mutation features. Each fold saved its train/test drug manifest and exact selected-feature lists under `data/processed/full_universe_manifests/`.

This benchmark remains limited to variance-based selection and the fixed Ridge model. It does not establish that the selected feature set is optimal or that the small fusion gain will transfer across datasets.

## Full-universe LOOD comparison

| Held-out dataset | Expression RMSE | Fusion RMSE | Fusion − expression |
|---|---:|---:|---:|
| CTD2 | 0.3231 | 0.3238 | +0.0007 |
| GDSC1 | 0.2322 | 0.2339 | +0.0017 |
| GDSC2 | 0.2347 | 0.2387 | +0.0040 |

Fusion was slightly worse than expression in all three full-universe LOOD folds. The effect is smaller than in the earlier candidate-table results but has the same direction. Thus, the consistent interpretation is a small within-universe fusion benefit and a small cross-study transfer penalty under this benchmark.
