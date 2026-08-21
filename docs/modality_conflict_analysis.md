# Modality conflict and redundancy analysis

The frozen validation results show conditional rather than universal fusion benefit. Fusion improves RMSE in the three drug-held-out seeds on two of three splits, but worsens on all three leave-one-dataset-out folds, including the strongest degradation on CTD2. The signed fusion-minus-expression RMSE deltas are persisted in `data/processed/modality_conflict_summary.json`.

The row-mean redundancy audit reports weak-to-moderate cross-modality correlations (approximately 0.12–0.17 for expression/copy-number and −0.09 to −0.20 for copy-number/mutation, depending on dataset/table). This does not imply feature-level independence; it is a compact audit of row-level modality summaries. Missingness is structured in outer-joined tables, with the all-modality complete fraction varying by source dataset.

Interpretation is deliberately limited: these results identify split- and dataset-conditional disagreement, not a causal mechanism for fusion degradation. The final manuscript should show the signed deltas and retain CTD2 as an explicit failure case.
