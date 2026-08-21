# Structured missingness and redundancy audit

The new audit was run across all 15 prepared drug tables. Each table showed 100% row availability for expression, copy number, and mutation and a 100% all-modality complete-case fraction.

This result is expected from the current table-construction rule: prepared tables are created by inner-joining the three selected modality matrices. Therefore, the audit verifies the prepared-table invariant but does not estimate natural missingness in the source datasets. The masked-feature uncertainty analyses remain the valid missingness experiments currently available.

The audit script is `scripts/audit_structured_missingness.py`; its local derived output is `data/processed/structured_missingness_redundancy.json`. A final study must add outer-joined tables and explicit missing-modality pattern labels before making claims about real-world modality availability.
