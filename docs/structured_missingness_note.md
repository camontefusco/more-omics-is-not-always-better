# Structured missingness and redundancy audit

The new audit was run across all 15 prepared drug tables. Each table showed 100% row availability for expression, copy number, and mutation and a 100% all-modality complete-case fraction.

This result is expected from the current table-construction rule: prepared tables are created by inner-joining the three selected modality matrices. Therefore, the audit verifies the prepared-table invariant but does not estimate natural missingness in the source datasets. The masked-feature uncertainty analyses remain the valid missingness experiments currently available.

The audit script is `scripts/audit_structured_missingness.py`; its local derived output is `data/processed/structured_missingness_redundancy.json`. A final study must add outer-joined tables and explicit missing-modality pattern labels before making claims about real-world modality availability.

## Outer-join follow-up

The builder now supports `--join outer`. Across the 15 outer-joined evaluation tables, mean row availability was 82.7% for expression, 59.4% for copy number, and 99.5% for damaging mutation. The mean all-three-modality complete-case fraction was 59.1%.

These values are a useful first structured-missingness signal, but they are averaged across selected drugs and remain dependent on the downloaded feature intersection and selected-cell-line universe. The outer-join audit is retained locally as `data/processed/structured_missingness_outer.json`.
