# Project instructions for AI agents

This file is the single source of project expectations for Codex, Cursor, and other AI agents. Claude Code uses [CLAUDE.md](CLAUDE.md), which references this file.

## Project overview

dbt-artifacts-parser is a Python package that parses dbt artifacts (catalog, manifest, run-results, sources) as Python objects. Pydantic models are generated from the official dbt artifact JSON schemas (from dbt-labs/dbt-core). We do not manually edit generated parser models; we use dbt artifacts from stable dbt versions only; we support only artifacts whose JSON schemas are publicly available.

See [README.md](README.md) for usage and [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution and implementation policy.

## Setup and commands

Run from the **repository root**.

- **Setup:** `make setup` — installs dependencies and pre-commit hooks.
- **Test:** `make test`
- **Lint:** `make lint` (runs pre-commit on all files)
- **Build:** `make build` — clean, lint, test, then build the package.

## Code and contribution

- Follow the implementation policy in [CONTRIBUTING.md](CONTRIBUTING.md): no manual changes to generated Pydantic models; use the download and generate scripts for any parser updates.
- Parser codegen: download schemas with [dev/download_dbt_schemas.sh](dev/download_dbt_schemas.sh), then generate classes with [dev/generate_parser_classes.sh](dev/generate_parser_classes.sh).

## Parser refresh workflow

When updating or adding parsers (syncing with dbt-core, regenerating Pydantic models):

1. **Download first:** `bash dev/download_dbt_schemas.sh [--ref REF] [artifact_type] [version ...]`
2. **Then generate:** `bash dev/generate_parser_classes.sh [artifact_type] [version ...]`

Artifact types: `catalog`, `manifest`, `run-results`, `sources`. Omit arguments to process all types and versions. If the user specifies a ref (e.g. branch), pass `--ref REF` only to the download script.

A project skill **dbt-parser-refresh** encodes this workflow in detail. Skills live in `.claude/skills/` (Cursor and Claude Code). Codex users: this repo provides `.agents/skills` as a symlink to `.claude/skills`, so the same skill is available there.
