# Initial modality-overlap report

The complete-case cohort is defined by `depmap_id` availability in expression, copy number, and damaging-mutation tables. Response observations are then restricted to those cell lines for each screen.

| Response screen | Response cell lines | Expression overlap | Copy-number overlap | Mutation overlap | Complete three-modality overlap |
|---|---:|---:|---:|---:|---:|
| CTD² | 810 | 794 | 569 | 796 | 567 |
| GDSC1 | 948 | 700 | 502 | 938 | 499 |
| GDSC2 | 947 | 701 | 500 | 937 | 497 |

Copy-number availability is the limiting modality. The primary complete-case analyses should therefore report these cohort sizes explicitly, while missing-modality analyses should retain the larger partially observed cohorts rather than silently dropping them.

No feature-level join has been performed yet; this report is based only on identifier overlap.

The first deterministic GDSC1 split manifest uses seed `20260821`: 201,225/50,307 pair rows, 758/190 held-out cell-line groups, and 252/64 held-out drug groups for train/test respectively. The same split generator will be applied to CTD² and GDSC2.
