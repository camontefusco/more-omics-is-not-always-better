# CTD² missingness replication note

CTD² selected expression, copy-number, and damaging-mutation features using the locked cell-line-held-out training IDs. Five high-frequency compounds were evaluated with grouped fit/calibration/test partitions, 2,000 expression features, 25% random feature masking, and a nominal 90% residual interval.

| Drug | Test rows | Interval radius | Coverage |
|---|---:|---:|---:|
| Leptomycin B | 111 | 0.2975 | 91.9% |
| Vincristine | 110 | 0.2986 | 88.2% |
| SR-II-138A | 111 | 0.2219 | 88.3% |
| AZD-8055 | 110 | 0.2346 | 82.7% |
| Ouabain | 110 | 0.3092 | 91.8% |

Three of five compounds fell below nominal coverage in this single-seed exploratory run. Together with GDSC1 and GDSC2, this supports reporting drug-specific calibration rather than assuming a universal interval guarantee.
