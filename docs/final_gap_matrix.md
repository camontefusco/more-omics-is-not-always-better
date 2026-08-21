# Final gap matrix

| Work package | Current state | Evidence required | Completion criterion |
|---|---|---|---|
| MoA mapping | 15/15 compounds in the current cross-dataset evaluation universe mapped; full GDSC1 universe remains 5/316 | Audited source, confidence, and caveat for each prespecified compound | Mapping audit passes for the declared analysis universe |
| Validation | Drug-held-out and leave-one-dataset-out validation complete for the declared 15-drug universe | Locked result manifest contains split types, seeds, feature budget, and caveats | Formal tables and manifests are versioned |
| Failure analysis | Structured missingness and modality mean-correlation audit complete; model disagreement analysis remains | Missing-modality patterns, modality correlations, disagreement cases | Conflict/redundancy and performance-stratified figures are versioned |
| Release package | Reproducibility materials and result artifacts are being frozen | Clean environment rerun, rendered figures, public-data note | Checklist in `docs/reproducibility_release_checklist.md` passes |

## Recommended execution order

1. Freeze the prespecified drug universe and complete MoA mapping.
2. Run drug-held-out and cross-study validation using the same universe.
3. Add conflict/redundancy and structured missingness analyses.
4. Freeze results, render figures, rerun from a clean environment, and package the release.

The project should not be marked complete until the clean rerun, figure QA, manuscript package, and public-data access note are complete. The cross-study result is not same-drug replication because the declared datasets have limited drug overlap.
