# Full-universe feature-selection benchmark

The stronger benchmark selects the top 2,000 variance-ranked features per modality inside each drug-held-out training fold from the complete raw modality tables. It bypasses the prepared 2,000-feature candidate tables used by the earlier formal benchmark.

| Seed | Expression RMSE | Fusion RMSE | Fusion − expression |
|---:|---:|---:|---:|
| 20260821 | 0.1696 | 0.1672 | −0.0024 |
| 20260822 | 0.2538 | 0.2527 | −0.0011 |
| 20260823 | 0.2329 | 0.2326 | −0.0003 |
| **Mean** | **0.2188** | **0.2175** | **−0.0013** |

Fusion improved RMSE in all three full-universe splits, but the mean improvement was small. The full-universe absolute errors differ from the earlier candidate-table benchmark, confirming that candidate-table construction materially affects the reported error scale. The full-universe result should replace the earlier headline benchmark if the manuscript claims selection from the full raw feature universe.

Raw feature counts were 19,215 expression, 18,613 copy-number, and 19,505 mutation features. Each fold saved its train/test drug manifest and exact selected-feature lists under `data/processed/full_universe_manifests/`.

This benchmark remains limited to variance-based selection and the fixed Ridge model. It does not establish that the selected feature set is optimal or that the small fusion gain will transfer across datasets.
