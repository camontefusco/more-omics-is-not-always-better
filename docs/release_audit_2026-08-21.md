# Release audit — 2026-08-21

## Confirmed from provider or primary distribution pages

- DepMap currently identifies **DepMap Public 26Q1** as the current release for the portal's public release datasets.
- The gCSI distribution is identified as **gCSI GRdata v1.3**, with 788 cell lines and 44 compounds in the cited resource description; its response assay is CellTiter-Glo.

## Initial-set lock decision

- The initial set uses `Harmonized GDSC 25Q2`, `Harmonized CTD^2 25Q2`, and `DepMap Public 26Q1`.
- AUC is the primary response metric for GDSC1, GDSC2, and CTD^2; DepMap is used for molecular features in the initial set.
- gCSI is deferred to external validation because its native GR-value metric is not directly interchangeable with AUC.

## Additional response-metric evidence

- The DepMap custom-download catalog exposes GDSC1/GDSC2 AUC, log2-AUC, and viability fields, and exposes CTD^2 AUC and log2-AUC fields. These should be treated as distinct candidate fields until one is locked.
- A secondary methods source identifies CTRPv2 as version 2.0 (released October 2015) and GDSC1 as Release 8.1, but these identifiers still require confirmation against the original provider distribution metadata before entering the locked manifest.

## Decision

The initial manifest set is now locked for controlled ingestion. gCSI remains a deferred external-validation resource and is not part of the initial ingestion run.

## Access constraint

On 2026-08-21, the DepMap download-catalog endpoint returned an interactive Turnstile verification page to automated access. The portal is therefore not suitable for unattended metadata retrieval in this environment; a human/browser-assisted download or provider-supplied direct file URL is required for file-level checksums and exact release metadata.
