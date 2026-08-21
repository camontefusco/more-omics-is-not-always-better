# Controlled ingestion protocol

Data ingestion may begin only when the manifest audit passes.

For every downloaded source, record:

- provider and exact URL;
- release/version identifier;
- retrieval timestamp;
- file name and SHA-256 checksum;
- declared response metric and assay context;
- license/access notes;
- mapping-table versions used;
- software environment and command.

Raw files belong under `data/raw/` and are excluded from Git. Derived, harmonized tables belong under `data/processed/` and must be accompanied by a JSON provenance record. No raw data or credentials may be committed.
