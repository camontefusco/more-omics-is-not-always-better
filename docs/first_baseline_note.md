# First real-data baseline note

This is an exploratory pipeline check, not a confirmatory result. It uses the most frequent GDSC1 response drug in the downloaded subset (`AICA RIBONUCLEOTIDE (GDSC1:1001)`), 481 cell lines with all three modalities, a cell-line-held-out split, and 2,000 features selected within the training cell lines for each modality.

| Model | Features | MAE | RMSE |
|---|---:|---:|---:|
| Expression | 2,000 | 0.0784 | 0.1106 |
| Copy number | 2,000 | 0.1378 | 0.1881 |
| Damaging mutation | 2,000 | 0.1187 | 0.1523 |
| Simple fusion | 6,000 | 0.0732 | 0.1027 |

The fusion RMSE improvement versus expression alone is 0.0078 in this exploratory run. This does not establish pharmacological generality; the full analysis must repeat the comparison across pre-specified drugs, mechanisms of action, datasets, seeds, and missing-modality conditions.
