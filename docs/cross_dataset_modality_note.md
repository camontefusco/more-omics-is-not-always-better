# Cross-dataset modality robustness note

The expression, copy-number, damaging-mutation, and simple fusion Ridge baselines were evaluated on five prepared drugs in each of GDSC2 and CTD² using three cell-line-held-out seeds. Values below are mean fusion RMSE minus expression RMSE; negative values favor fusion.

| Dataset | Drug-level mean delta range | Drugs with negative mean delta |
|---|---:|---:|
| GDSC2 | −0.0072 to +0.0010 | 4/5 |
| CTD² | −0.0200 to +0.0017 | 3/5 |

The direction of incremental value is therefore not universal. Some drugs show consistent modest improvement, while others are near zero or change sign across seeds. These results support reporting per-drug deltas and uncertainty rather than a blanket claim that multimodal fusion is better.

The complete machine-readable results are retained locally in `data/processed/cross_dataset_modality_seeds.json`.
