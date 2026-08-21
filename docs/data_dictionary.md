# Data dictionary — draft

| Field | Meaning | Required | Provenance |
|---|---|---:|---|
| `cell_line_id_raw` | Source cell-line identifier | yes | source file |
| `cellosaurus_id` | Harmonized cell-line identifier | yes | Cellosaurus mapping |
| `drug_id_raw` | Source compound identifier | yes | source file |
| `pubchem_cid` | Harmonized compound identifier | preferred | PubChem mapping |
| `response_value` | Drug-response measurement | yes | source file |
| `response_metric` | AUC, AAC, IC50, LN_IC50, or other metric | yes | source metadata |
| `assay_context` | Assay/readout/incubation context | yes when available | source metadata |
| `moa_label` | Mechanism-of-action category | required for stratified analysis | curated mapping with citation |
| `transcriptomics_available` | Whether transcriptomic modality is present | yes | derived |
| `mutation_available` | Whether mutation modality is present | yes | derived |
| `copy_number_available` | Whether copy-number modality is present | yes | derived |
| `dataset_id` | Source dataset | yes | manifest |
| `release_id` | Dataset release/version | yes | manifest |
| `download_date` | Retrieval date | yes | pipeline |
