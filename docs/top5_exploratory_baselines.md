# Top-five exploratory GDSC1 baselines

Five most frequently observed drugs in the complete three-modality GDSC1 subset were evaluated with the same cell-line-held-out split and 2,000 training-selected features per modality.

| Drug | Cell lines | Expression RMSE | Fusion RMSE | Fusion ΔRMSE |
|---|---:|---:|---:|---:|
| AICA RIBONUCLEOTIDE (GDSC1:1001) | 481 | 0.1106 | 0.1027 | -0.0078 |
| DACOMITINIB (GDSC1:363) | 480 | 0.1886 | 0.1706 | -0.0180 |
| ACY-1215 (GDSC1:264) | 480 | 0.1363 | 0.1283 | -0.0079 |
| GSK1059615 (GDSC1:374) | 480 | 0.1947 | 0.1870 | -0.0077 |
| TENOVIN-6 (GDSC1:342) | 480 | 0.1245 | 0.1125 | -0.0120 |

Fusion improved RMSE versus expression in all five exploratory runs. These are not mechanism-stratified or confirmatory results; the next analysis must add authoritative MoA labels, broader drug coverage, and cross-dataset replication.

## Three-seed robustness extension

The same five prepared GDSC1 tables were rerun with grouped splits at seeds 20260821, 20260822, and 20260823. Mean fusion RMSE deltas versus expression were −0.0050 for AICA ribonucleotide, −0.0217 for dacomitinib, −0.0035 for ACY-1215, −0.0069 for GSK1059615, and −0.0128 for Tenovin-6. The per-seed delta range for ACY-1215 was −0.0079 to +0.0001, showing that the incremental value can be negligible on an individual split.

This remains exploratory: the feature set is fixed from the initial train-only selection, the analysis is limited to five drugs, and cross-dataset modality performance has not yet been completed.
