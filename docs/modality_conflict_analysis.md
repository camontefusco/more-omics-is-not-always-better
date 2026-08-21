# Modality conflict and redundancy analysis

The frozen full-universe validation results show conditional rather than universal fusion benefit. Across five drug-held-out seeds, fusion improves RMSE in three and is slightly worse in two; it is slightly worse on all three leave-one-dataset-out folds. The signed fusion-minus-expression RMSE deltas are persisted in `data/processed/modality_conflict_summary.json`.

The row-mean redundancy audit reports weak-to-moderate cross-modality correlations (approximately 0.12–0.17 for expression/copy-number and −0.09 to −0.20 for copy-number/mutation, depending on dataset/table). This does not imply feature-level independence; it is a compact audit of row-level modality summaries. Missingness is structured in outer-joined tables, with the all-modality complete fraction varying by source dataset.

Interpretation is deliberately limited: these results identify split- and dataset-conditional disagreement, not a causal mechanism for fusion degradation. The final manuscript should show the signed deltas and retain CTD2 as an explicit failure case.
