---
name: dbt-parser-refresh
description: Refreshes dbt artifact schemas from schemas.getdbt.com and regenerates Pydantic parser classes. Use when the user asks to update parsers, sync with upstream, download dbt schemas, or regenerate parser models.
---

# dbt Parser Refresh

## Trigger scenarios

Activate this skill when the user says or implies:

- Refresh parsers, update parsers, sync parsers
- Update from schemas.getdbt.com, sync with upstream schemas
- Download dbt schemas, pull schemas from schemas.getdbt.com
- Regenerate parser classes, regenerate parser models, run codegen

## Scripts and paths

- Run all commands from the **repository root**.
- **Download:** `bash dev/download_dbt_schemas.sh [artifact_type] [version ...]`
- **Generate:** `bash dev/generate_parser_classes.sh [artifact_type] [version ...]`
- **Artifact types:** `catalog`, `manifest`, `run-results`, `sources`
- **Versions:** e.g. `v1`, `v7`. Omit args to process all types and versions.

## Order rule

When doing both download and generate, **always run download first**, then generate.

## Three modes

### 1. Download + generate (default)

When the user wants to refresh or update parsers (e.g. "refresh parsers", "update schemas"):

1. Run `bash dev/download_dbt_schemas.sh` with any user-specified artifact_type or versions.
2. Then run `bash dev/generate_parser_classes.sh` with the same artifact_type and versions.

If the user did not specify scope, use no arguments for both (download all, then generate all).

### 2. Download only

When the user only wants to fetch schemas (e.g. "download dbt schemas", "pull schemas from schemas.getdbt.com"):

- Run only `bash dev/download_dbt_schemas.sh` with optional artifact_type/version.

### 3. Generate only

When schemas are already present and the user only wants to regenerate code (e.g. "regenerate parsers", "run codegen"):

- Run only `bash dev/generate_parser_classes.sh` with optional artifact_type/version.

## Passing through user intent

- **Scope:** If they specify an artifact or version (e.g. "just manifest v7"), use the same artifact_type and version(s) for both scripts when running both.

## Example

Full refresh (all types and versions):

```bash
bash dev/download_dbt_schemas.sh
bash dev/generate_parser_classes.sh
```

Refresh only manifest v7:

```bash
bash dev/download_dbt_schemas.sh manifest v7
bash dev/generate_parser_classes.sh manifest v7
```
