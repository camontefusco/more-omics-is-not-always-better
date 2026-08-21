# Release audit — 2026-08-21

## Confirmed from provider or primary distribution pages

- DepMap currently identifies **DepMap Public 26Q1** as the current release for the portal's public release datasets.
- The gCSI distribution is identified as **gCSI GRdata v1.3**, with 788 cell lines and 44 compounds in the cited resource description; its response assay is CellTiter-Glo.

## Still unresolved before manifest lock

- Exact GDSC1 and GDSC2 bulk-download release identifiers and the response fields to use.
- Exact CTRPv2 release identifier and response field.
- Whether CCLE/DepMap response data will be used as a primary screen or only as molecular-feature infrastructure.
- A single primary response metric or a pre-specified source-native metric strategy.

## Decision

Do not mark the manifest locked or download the full data bundle yet. The release names above are recorded as evidence, but the remaining unresolved fields would make cross-study comparisons ambiguous.
