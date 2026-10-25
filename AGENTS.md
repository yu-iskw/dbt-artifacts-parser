# Project instructions for AI agents

This file is the single source of project expectations for Codex, Cursor, and other AI agents. Claude Code uses [CLAUDE.md](CLAUDE.md), which references this file.

## Project overview

dbt-artifacts-parser is a Python package that parses dbt artifacts (catalog, manifest, run-results, sources) as Python objects. Pydantic models are generated from the official dbt artifact JSON schemas (from dbt-labs/dbt-core). We do not manually edit generated parser models; we use dbt artifacts from stable dbt versions only; we support only artifacts whose JSON schemas are publicly available.

See [README.md](README.md) for usage and [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution and implementation policy.

## When documentation and code disagree

When a repository's documentation and its existing code disagree, follow the conventions used in the existing code, and in your final reply point out each inconsistency you found between the documentation and the code.

"Documentation" includes this file, `CLAUDE.md`, editor rules, READMEs, `docs/`, ADRs, RFCs, and code comments. Treat what they say about the code as claims to check against the code, not as facts.

- **Documented target state wins only when it is explicit.** Follow the documentation instead of the code only when the documentation says the code is legacy or a migration is in progress. For example: a "migration in progress", "legacy", or "deprecated" marker, `@deprecated` on the code you would copy, or an ADR/RFC with status *Accepted* that is not superseded and is newer than the code it replaces. Ignore ADRs/RFCs that are *Proposed*, *Rejected*, *Deprecated*, or *Superseded*. Follow the superseding one.
- **When you can't tell which is current,** compare recency (`git log -1 --format=%cs -- <doc>` vs the code paths). Prefer the newer source, and say that you did. If the choice changes behavior and is still unclear, ask before proceeding.
- **Scope.** Apply the convention you choose to the code you are writing or changing. Don't rewrite working code, and don't edit documentation just to make the two agree, unless the task asks for it.
- **Process and safety rules still apply.** Commands to run, quality gates, review/merge rules, and security constraints in this file are not descriptions of the code. Follow them.
- **Report.** In your final reply (and in the PR description, if you open one), list each inconsistency: the document and section, what the code actually does, which one you followed, and why.

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

Artifact types: `catalog`, `manifest`, `run-results`, `sources`. Omit arguments to process all types and versions. Default download ref is `1.latest` (dbt Core v1; `main` no longer hosts `schemas/dbt`). For releases, pass an explicit stable tag (e.g. `--ref v1.11.12`). If the user specifies a ref, pass `--ref REF` only to the download script.

A project skill **dbt-parser-refresh** encodes this workflow in detail. Skills live in `.claude/skills/` (Cursor and Claude Code). Codex users: this repo provides `.agents/skills` as a symlink to `.claude/skills`, so the same skill is available there.

## Package version and PyPI release

To bump the library semver (`__version__`), prepare a release, and align GitHub Releases with PyPI, follow the **package-version-bump** skill in [.claude/skills/package-version-bump/SKILL.md](.claude/skills/package-version-bump/SKILL.md).
