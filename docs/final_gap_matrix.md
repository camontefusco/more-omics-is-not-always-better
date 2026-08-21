# Final gap matrix

| Work package | Current state | Evidence required | Completion criterion |
|---|---|---|---|
| MoA mapping | 5/316 GDSC1 compounds mapped | Audited source, confidence, and caveat for each prespecified compound | Mapping audit passes for the declared analysis universe |
| Validation | Exploratory grouped splits across 3 datasets | Drug-held-out, cross-study, and repeated-seed performance tables | Locked result manifest contains all required split types and seeds |
| Failure analysis | Random masking evaluated; conflict/redundancy not complete | Missing-modality patterns, modality correlations, disagreement cases | Main claims include stratified failure analyses |
| Release package | Internal reproducibility materials present | Clean environment rerun, formal result tables, rendered figures, public-data note | Checklist in `docs/reproducibility_release_checklist.md` passes |

## Recommended execution order

1. Freeze the prespecified drug universe and complete MoA mapping.
2. Run drug-held-out and cross-study validation using the same universe.
3. Add conflict/redundancy and structured missingness analyses.
4. Freeze results, render figures, rerun from a clean environment, and package the release.

The project should not be marked complete when only the first two exploratory baselines are available; the completion decision depends on all four rows above.
