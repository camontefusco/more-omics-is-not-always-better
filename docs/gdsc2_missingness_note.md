# GDSC2 missingness replication note

GDSC2 selected expression, copy-number, and damaging-mutation features using the locked cell-line-held-out training IDs. Five high-frequency GDSC2 compounds were then evaluated with grouped fit/calibration/test partitions, 2,000 expression features, 25% random feature masking, and a nominal 90% residual interval.

| Drug | Test rows | Interval radius | Coverage |
|---|---:|---:|---:|
| Navitoclax | 100 | 0.2282 | 89.0% |
| MK-2206 | 100 | 0.1885 | 100.0% |
| Staurosporine | 100 | 0.2605 | 96.0% |
| Pictilisib | 100 | 0.1872 | 95.0% |
| MG-132 | 100 | 0.1990 | 93.0% |

This is a single-seed exploratory replication. Results broadly resemble the GDSC1 finding that coverage is drug-specific, while the GDSC2 sample gives four of five compounds at or above nominal coverage. Larger repeated-seed and cross-dataset analyses remain required.
