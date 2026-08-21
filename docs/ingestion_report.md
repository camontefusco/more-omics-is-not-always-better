# Initial ingestion report

Generated 2026-08-21 from the six downloaded DepMap exports.

| Response resource | Long-form rows | Cell lines | Drugs |
|---|---:|---:|---:|
| CTD² | 346,553 | 810 | 544 |
| GDSC1 | 251,532 | 948 | 316 |
| GDSC2 | 230,149 | 947 | 286 |

Modality availability by `depmap_id`:

- Expression: 1,719
- Copy number: 1,118
- Damaging mutations: 1,968
- Union: 2,044
- Intersection: 1,105

The response tables are generated under `data/processed/` and excluded from Git because they are derived data. The compact JSON report is stored at `data/processed/ingestion_report.json`.
