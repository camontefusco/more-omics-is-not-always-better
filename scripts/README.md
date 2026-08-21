# Analysis scripts

Scripts should be small, composable, and runnable from the repository root. Each script must write a provenance record containing the manifest version, input checksums, software environment, random seed, and output paths.

Planned interfaces:

- `audit_dataset_manifest.py`: validate manifest completeness and release fields.
- `harmonize_identifiers.py`: map cell lines, compounds, and genes while preserving raw identifiers.
- `build_analysis_table.py`: create a versioned cell-line × drug analysis table.
- `run_baselines.py`: fit locked unimodal and simple fusion baselines.
- `evaluate_fusion.py`: calculate paired incremental value, calibration, missingness, and conflict metrics.
