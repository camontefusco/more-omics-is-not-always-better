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
