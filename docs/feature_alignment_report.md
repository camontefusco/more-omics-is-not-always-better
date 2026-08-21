# Feature-alignment report

Feature names were compared after removing the seven shared metadata columns (`depmap_id`, display name, and lineage fields).

| Modality | Feature columns |
|---|---:|
| Expression | 19,215 |
| Copy number | 18,613 |
| Damaging mutations | 19,505 |

Pairwise and three-way intersections:

- Expression ∩ copy number: 18,399
- Expression ∩ mutation: 17,699
- Copy number ∩ mutation: 17,556
- All three modalities: 17,490

The initial multimodal feature universe can therefore use the 17,490 shared feature names, subject to a subsequent identifier audit for gene symbols, duplicated aliases, and non-gene columns. Feature selection must still be fitted inside each training split to avoid leakage.
