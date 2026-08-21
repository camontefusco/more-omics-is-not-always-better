# Release audit — 2026-08-21

## Confirmed from provider or primary distribution pages

- DepMap currently identifies **DepMap Public 26Q1** as the current release for the portal's public release datasets.
- The gCSI distribution is identified as **gCSI GRdata v1.3**, with 788 cell lines and 44 compounds in the cited resource description; its response assay is CellTiter-Glo.

## Still unresolved before manifest lock

- Exact GDSC1 and GDSC2 bulk-download release identifiers and the response fields to use.
- Exact CTRPv2 release identifier and response field.
- Whether CCLE/DepMap response data will be used as a primary screen or only as molecular-feature infrastructure.
- A single primary response metric or a pre-specified source-native metric strategy.

## Additional response-metric evidence

- The DepMap custom-download catalog exposes GDSC1/GDSC2 AUC, log2-AUC, and viability fields, and exposes CTD^2 AUC and log2-AUC fields. These should be treated as distinct candidate fields until one is locked.
- A secondary methods source identifies CTRPv2 as version 2.0 (released October 2015) and GDSC1 as Release 8.1, but these identifiers still require confirmation against the original provider distribution metadata before entering the locked manifest.

## Decision

Do not mark the manifest locked or download the full data bundle yet. The release names above are recorded as evidence, but the remaining unresolved fields would make cross-study comparisons ambiguous.
