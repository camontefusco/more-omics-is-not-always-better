# Drug-held-out validation note

The 15 prepared outer-joined drug tables were concatenated into `data/processed/combined_15drug_outer_table.csv`, retaining `drug_id_raw` and `dataset_id`. A true grouped drug-held-out split was then executed with `drug_id_raw` as the grouping variable.

Because the full 2,000-feature/three-seed run is computationally expensive on the 116 MB combined table, the completed smoke validation used 25 fixed selected features per modality and seed 20260821:

| Model | RMSE |
|---|---:|
| Expression | 0.3144 |
| Copy number | 0.3194 |
| Mutation | 0.3188 |
| Fusion | 0.3143 |

Fusion delta versus expression was −0.00007. This confirms the grouped drug-held-out implementation and schema, but is not a scientific performance result. The formal benchmark still requires fold-local feature selection, the full declared feature budget, repeated seeds, and a persisted drug split manifest.
