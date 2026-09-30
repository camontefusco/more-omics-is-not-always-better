# Multimodal Cancer Drug-Response Prediction Benchmark

This repository contains the reproducibility materials for a leakage-controlled benchmark of expression-only and early-fusion cancer drug-response models. The current release is limited to a declared 15-compound universe drawn from GDSC1, GDSC2, and CTD².

## Reproducibility release

The repository is intended to be archived as a versioned GitHub release and through Zenodo. Use the exact release tag named in the manuscript and response letter. The release contains code, split and feature manifests, derived result summaries, figures, manuscript materials, tests, and the pinned environment specification.

Raw provider files are not redistributed. Obtain the following source releases under their applicable terms and follow `data/raw/README.md` and `configs/dataset_manifest.yaml`:

- Harmonized GDSC 25Q2.
- Harmonized CTD² 25Q2.
- DepMap Public 26Q1.

## Regeneration outline

1. Create the environment from `configs/requirements-release.txt`.
2. Obtain the permitted provider files and place them under `data/raw/`.
3. Review `configs/dataset_manifest.yaml` and the public-data access note.
4. Run the ingestion and validation scripts in `scripts/README.md`.
5. Run `scripts/run_full_universe_benchmark.py` for grouped drug-held-out results.
6. Run `scripts/run_full_universe_lood.py` for leave-one-dataset-out results.
7. Run the missingness, conflict, and figure-generation scripts.
8. Compare regenerated machine-readable results with the frozen release artifacts.

## Scope

The model uses cell-line molecular features and does not include drug chemical structure, target, mechanism, dose, or fingerprint features. Drug-held-out results are therefore a limited transfer stress test within the declared response universe, not arbitrary unseen-drug prediction. The results are not clinical or causal validation.

## Citation

See `CITATION.cff`. The preferred citation will be the immutable Zenodo release associated with the final GitHub tag, together with the manuscript citation. The version DOI is pending until the GitHub release is archived by Zenodo.

## Project links

- GitHub: https://github.com/camontefusco/more-omics-is-not-always-better
- Local project: `/Users/cmontefusco/Coding_projects/more-omics-is-not-always-better`
