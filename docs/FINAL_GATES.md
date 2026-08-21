# Final scientific gates before real-data modeling

1. Lock exact releases and response metrics in `configs/dataset_manifest.yaml`.
2. Complete and verify the compound mechanism mapping.
3. Download raw data with checksums and provenance records.
4. Harmonize identifiers and validate the analysis table.
5. Run unimodal, fusion, missingness, and uncertainty analyses under locked splits.
6. Perform cross-study validation with assay and response-metric context retained.
7. Reassess novelty against the final literature matrix before manuscript drafting.

Current state: gates 1, 3, 4, and 5 have been exercised on the locked real-data subset; gate 6 has exploratory replication across GDSC1, GDSC2, and CTD². Gate 2 is incomplete because only 5 of 316 GDSC1 response compounds are mapped, and gate 7 remains open. Results are therefore exploratory and should not be presented as a complete mechanism-stratified study.
