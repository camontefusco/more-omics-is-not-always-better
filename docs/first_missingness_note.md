# First missingness and uncertainty note

Exploratory test on the first GDSC1 compound using 2,000 expression features, 25% random feature masking, and a residual-based 90% interval.

- Test rows: 97
- Initial interval radius: 0.00032
- Initial observed interval coverage: 0.0

This was a failure signal: the initial interval calibration used unmasked training residuals and was overconfident under missingness.

## Calibrated follow-up

The evaluator now uses separate cell-line-grouped fit, calibration, and test partitions. Calibration receives the same masking fraction as test, and the 90th-percentile absolute residual is computed from masked calibration predictions.

For the same exploratory setup: fit rows 307, calibration rows 77, test rows 97; 25% masking; interval radius 0.1654; observed coverage 93.8%. This repairs the calibration-regime bug for this test, but remains exploratory until repeated across drugs, masking patterns, and response datasets.

### Masking sensitivity using all 2,000 expression features

| Mask fraction | Interval radius | Test coverage |
|---:|---:|---:|
| 10% | 0.1909 | 95.9% |
| 25% | 0.1831 | 94.8% |
| 50% | 0.1921 | 94.8% |

Coverage is stable near the nominal 90% level in this sensitivity check. The result is still exploratory and should not be generalized beyond this drug and split until the planned per-drug and cross-dataset analyses are complete.

### Five-drug GDSC1 extension

Using the same grouped fit/calibration/test design and 25% expression-feature masking:

| Drug | Test rows | Interval radius | Coverage |
|---|---:|---:|---:|
| AICA ribonucleotide | 97 | 0.1831 | 94.8% |
| Tenovin-6 | 96 | 0.2161 | 94.8% |
| GSK1059615 | 96 | 0.2792 | 87.5% |
| ACY-1215 | 96 | 0.2096 | 87.5% |
| Dacomitinib | 96 | 0.2604 | 85.4% |

Coverage varies materially by drug. This is evidence that calibration must be evaluated per drug and mechanism, with larger calibration sets and repeated seeds, before any final uncertainty claim.

### Three-seed repeat

The same five drugs were rerun at 25% masking with seeds 20260821, 20260822, and 20260823. Mean coverage was 91.1% for AICA ribonucleotide, 94.1% for Tenovin-6, 89.6% for GSK1059615, 92.4% for ACY-1215, and 90.3% for dacomitinib. The full per-seed results are retained in the local derived output `data/processed/gdsc1_top5_missingness_seeds.json`.

Coverage ranges across seeds were 85.6–94.8%, 91.7–95.8%, 87.5–91.7%, 87.5–97.9%, and 85.4–93.8%, respectively. This confirms that uncertainty performance is both drug- and split-sensitive; larger repeated-split evaluation is required before treating nominal coverage as established.
