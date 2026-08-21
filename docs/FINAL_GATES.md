# Final scientific gates before real-data modeling

1. Lock exact releases and response metrics in `configs/dataset_manifest.yaml`.
2. Complete and verify the compound mechanism mapping.
3. Download raw data with checksums and provenance records.
4. Harmonize identifiers and validate the analysis table.
5. Run unimodal, fusion, missingness, and uncertainty analyses under locked splits.
6. Perform cross-study validation with assay and response-metric context retained.
7. Reassess novelty against the final literature matrix before manuscript drafting.

The current repository contains executable infrastructure and smoke tests only. No scientific result should be interpreted until these gates pass on real data.
