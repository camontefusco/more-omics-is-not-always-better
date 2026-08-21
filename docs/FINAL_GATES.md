# Final scientific gates before real-data modeling

1. Lock exact releases and response metrics in `configs/dataset_manifest.yaml`.
2. Complete and verify the compound mechanism mapping.
3. Download raw data with checksums and provenance records.
4. Harmonize identifiers and validate the analysis table.
5. Run unimodal, fusion, missingness, and uncertainty analyses under locked splits.
6. Perform cross-study validation with assay and response-metric context retained.
7. Reassess novelty against the final literature matrix before manuscript drafting.

Current state: gates 1–6 are complete for the declared 15-compound evaluation universe, including formal drug-heldout and leave-one-dataset-out validation. Gate 2 remains limited only outside that universe: 5 of 316 full GDSC1 response compounds are mapped. Gate 7 should be rerun as an external pre-submission literature/licensing review. Results must remain explicitly bounded to the prespecified evaluation subset.
