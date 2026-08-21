# First missingness and uncertainty note

Exploratory test on the first GDSC1 compound using 2,000 expression features, 25% random feature masking, and a residual-based 90% interval.

- Test rows: 97
- Initial interval radius: 0.00032
- Initial observed interval coverage: 0.0

This was a failure signal: the initial interval calibration used unmasked training residuals and was overconfident under missingness.

## Calibrated follow-up

The evaluator now uses separate cell-line-grouped fit, calibration, and test partitions. Calibration receives the same masking fraction as test, and the 90th-percentile absolute residual is computed from masked calibration predictions.

For the same exploratory setup: fit rows 307, calibration rows 77, test rows 97; 25% masking; interval radius 0.1654; observed coverage 93.8%. This repairs the calibration-regime bug for this test, but remains exploratory until repeated across drugs, masking patterns, and response datasets.
