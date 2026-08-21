# First missingness and uncertainty note

Exploratory test on the first GDSC1 compound using 2,000 expression features, 25% random feature masking, and a residual-based 90% interval.

- Test rows: 97
- Interval radius: 0.00032
- Observed interval coverage: 0.0

This is a useful failure signal, not a scientific result. The initial interval calibration used unmasked training residuals and was overconfident under missingness. The final uncertainty analysis must calibrate intervals under the same missingness regime—or use a method explicitly robust to missing modalities—and report coverage by missingness pattern.
