# CLAUDE.md - AI Assistant Guide for dbt-artifacts-parser

## Project Overview

**dbt-artifacts-parser** is a Python library that parses dbt (data build tool) artifacts into Python objects using Pydantic models. It enables developers to work with `catalog.json`, `manifest.json`, `run-results.json`, and `sources.json` as strongly-typed Python objects.

- **Current Version**: 0.12.0
- **License**: Apache License 2.0
- **Primary Dependencies**: Pydantic v2 (>=2.0,<3.0)
- **Python Support**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Package Manager**: uv (with uv.lock)
- **Build System**: hatchling

### Key Characteristics

- **Auto-Generated Models**: Pydantic models are generated from dbt JSON schemas using `datamodel-code-generator`
- **Version Coverage**: Supports dbt 0.19 through 1.11
- **Pydantic v2 Only**: Version 0.12+ only supports Pydantic v2 (Pydantic v1 support ended with dbt 1.8)

## Codebase Structure

```
dbt-artifacts-parser/
├── dbt_artifacts_parser/          # Main package
│   ├── __init__.py                # Version: 0.12.0
│   ├── parser.py                  # Main parser functions
│   ├── utils.py                   # Utility functions
│   ├── parsers/                   # Generated parser models
│   │   ├── base.py               # BaseParserModel (extends pydantic.BaseModel)
│   │   ├── version_map.py        # ArtifactTypes enum mapping
│   │   ├── utils.py              # Parser utilities
│   │   ├── catalog/              # Catalog parsers (v1)
│   │   ├── manifest/             # Manifest parsers (v1-v12)
│   │   ├── run_results/          # Run results parsers (v1-v6)
│   │   └── sources/              # Sources parsers (v1-v3)
│   └── resources/                 # JSON schemas from dbt-core
│       ├── catalog/
│       ├── manifest/
│       ├── run-results/
│       └── sources/
├── tests/                         # Test suite
│   ├── test_parser.py            # Parser tests
│   ├── test_utils.py             # Utility tests
│   └── resources/                # Test fixtures (real dbt artifacts)
├── dev/                          # Development scripts
│   ├── setup.sh                  # Environment setup
│   ├── generate_parser_classes.sh # Code generation
│   ├── test_python.sh            # Run tests
│   ├── build.sh                  # Build package
│   ├── clean.sh                  # Clean artifacts
│   └── publish.sh                # Publish to PyPI
├── .github/workflows/            # CI/CD workflows
│   ├── test.yml                  # Run tests on PRs and main
│   ├── lint.yml                  # Linting checks
│   ├── publish.yml               # Publish to PyPI
│   ├── test-publish.yml          # Publish to TestPyPI
│   └── contributors-list.yml     # Update contributors
├── pyproject.toml                # Project configuration
├── Makefile                      # Development commands
├── .pre-commit-config.yaml       # Pre-commit hooks
├── .pylintrc                     # Pylint configuration
└── README.md                     # User-facing documentation
```

## Critical Implementation Policies

### DO NOT MODIFY GENERATED CODE

**EXTREMELY IMPORTANT**: The Pydantic models in `dbt_artifacts_parser/parsers/` are auto-generated and must NEVER be manually edited. This is a fundamental rule:

1. **Never manually modify** files in:
   - `dbt_artifacts_parser/parsers/catalog/`
   - `dbt_artifacts_parser/parsers/manifest/`
   - `dbt_artifacts_parser/parsers/run_results/`
   - `dbt_artifacts_parser/parsers/sources/`

2. **Exception**: You may edit `base.py`, `version_map.py`, and `utils.py` in `dbt_artifacts_parser/parsers/`

3. **Why**: Manual changes would be lost on the next code generation. If changes are needed, they must be made to the upstream dbt JSON schemas.

4. **Pylint Configuration**: Note that `.pre-commit-config.yaml` excludes `dbt_artifacts_parser/parsers/` from pylint checks for this reason.

### JSON Schema Source Policy

1. **Only use stable dbt releases** - no alpha/beta versions
2. **Only support publicly available schemas** - dbt Cloud-exclusive artifacts (like `semantic_manifest.json`) are not supported
3. **Schemas are sourced from**: https://github.com/dbt-labs/dbt-core/tree/main/schemas/dbt
4. **Schemas are stored in**: `dbt_artifacts_parser/resources/`

## Development Setup

### Prerequisites

- Python 3.9+
- uv package manager (or pip)
- pre-commit (installed via setup)

### Setup Commands

```bash
# Full setup (installs dependencies + pre-commit hooks)
make setup

# Or individually:
make setup-python      # Install Python dependencies
make setup-pre-commit  # Install pre-commit hooks
```

The setup script (`dev/setup.sh`) accepts a `--deps` parameter:
- `--deps "development"` - Install all dev dependencies (default for make setup)

## Development Workflows

### Making Code Changes

For non-generated code (parser.py, utils.py, base.py, version_map.py, tests):
1. Make your changes
2. Run linting: `make lint` or `make run-pre-commit`
3. Run tests: `make test`
4. Commit changes

### Adding Support for New dbt Artifact Versions

When dbt releases a new version with updated artifacts:

1. **Download the new JSON schema** from https://github.com/dbt-labs/dbt-core/tree/main/schemas/dbt
2. **Save it** to `dbt_artifacts_parser/resources/{artifact_type}/{artifact_type}_{version}.json`
   - Example: `dbt_artifacts_parser/resources/manifest/manifest_v13.json`
3. **Update** `dev/generate_parser_classes.sh` to include the new version
4. **Run code generation**: `bash dev/generate_parser_classes.sh`
5. **Update** `dbt_artifacts_parser/parsers/version_map.py` to add the new artifact type
6. **Update** `dbt_artifacts_parser/parser.py` to add parsing functions
7. **Add test fixtures** to `tests/resources/{artifact_type}/{version}/`
8. **Update tests** in `tests/test_parser.py`
9. **Run tests**: `make test`
10. **Update README.md** with new version support

### Code Generation Process

The `dev/generate_parser_classes.sh` script uses `datamodel-code-generator` to create Pydantic models:

```bash
bash dev/generate_parser_classes.sh
```

This generates:
- Catalog parsers: `CatalogV1`
- Manifest parsers: `ManifestV1` through `ManifestV12`
- Run results parsers: `RunResultsV1` through `RunResultsV6`
- Sources parsers: `SourcesV1` through `SourcesV3`

Configuration:
- **Target Python**: 3.9
- **Output Model Type**: pydantic_v2.BaseModel
- **Base Class**: `dbt_artifacts_parser.parsers.base.BaseParserModel`
- **Timestamps disabled**: `--disable-timestamp` (for reproducible builds)

## Testing

### Running Tests

```bash
# Run all tests
make test

# Or directly:
bash dev/test_python.sh

# Or with pytest:
pytest -v -s --cache-clear tests/
```

### Test Structure

- **Test Framework**: pytest
- **Test Fixtures**: Real dbt artifacts from jaffle_shop (dbt's example project)
- **Parametrized Tests**: Tests run across all supported versions

Key test files:
- `tests/test_parser.py` - Tests all parser functions
- `tests/test_utils.py` - Tests utility functions

Test pattern:
```python
@pytest.mark.parametrize("version", ["v1", "v2", ...])
class TestManifestParser:
    def test_parse_manifest(self, version):
        # Test generic parse_manifest() function

    def test_parse_manifest_specific(self, version):
        # Test version-specific parse_manifest_v1() etc.
```

## Quality Assurance

### Pre-commit Hooks

Configured in `.pre-commit-config.yaml`:
- **end-of-file-fixer** - Ensures files end with newline
- **trailing-whitespace** - Removes trailing whitespace
- **check-json/toml/yaml** - Validates config files
- **detect-private-key** - Prevents committing secrets
- **actionlint** - Validates GitHub Actions workflows
- **pylint** - Python linting (excludes generated parsers)
- **shellcheck** - Shell script linting
- **ruff** - Fast Python linter and formatter

Run manually:
```bash
make lint
# or
make run-pre-commit
# or
pre-commit run --all-files
```

Update hooks:
```bash
make update-pre-commit
```

### Linting Tools

- **Ruff**: Primary linter and formatter (configured in `pyproject.toml`)
  - Enabled rules: E (pycodestyle errors), F (pyflakes), I (isort imports)
- **Pylint**: Secondary linter (configured in `.pylintrc`)
- **MyPy**: Type checking (optional, in dev dependencies)

## Build and Release Process

### Build Package

```bash
make build
# This runs: clean → lint → test → build
```

Or directly:
```bash
bash dev/build.sh
```

### Publishing

**TestPyPI** (for testing):
```bash
make test-publish
```

**Production PyPI**:
```bash
make publish
```

Note: Publishing requires proper credentials in `.pypirc`

### Version Management

Version is defined in `dbt_artifacts_parser/__init__.py`:
```python
__version__ = "0.12.0"
```

Hatchling reads this via configuration in `pyproject.toml`:
```toml
[tool.hatch.version]
path = "dbt_artifacts_parser/__init__.py"
```

## CI/CD Workflows

### GitHub Actions

**test.yml** (`.github/workflows/test.yml`):
- Triggers: PRs and pushes to main
- Matrix: Python 3.10, 3.11, 3.12, 3.13
- Steps: Install deps → Run tests → Test build → Test installation

**lint.yml** (`.github/workflows/lint.yml`):
- Runs pre-commit hooks on all files

**publish.yml** (`.github/workflows/publish.yml`):
- Publishes to PyPI on release tags

**test-publish.yml** (`.github/workflows/test-publish.yml`):
- Publishes to TestPyPI for testing

**contributors-list.yml** (`.github/workflows/contributors-list.yml`):
- Auto-updates contributor list in README

## Architecture Details

### Parser Functions

The main parser module (`dbt_artifacts_parser/parser.py`) provides two types of functions:

1. **Version-agnostic parsers**: Auto-detect version and return appropriate type
   - `parse_catalog(catalog: dict)`
   - `parse_manifest(manifest: dict)`
   - `parse_run_results(run_results: dict)`
   - `parse_sources(sources: dict)`

2. **Version-specific parsers**: Validate exact version and return specific type
   - `parse_catalog_v1(catalog: dict) -> CatalogV1`
   - `parse_manifest_v1(manifest: dict) -> ManifestV1`
   - ... through v12 for manifests
   - `parse_run_results_v1(run_results: dict) -> RunResultsV1`
   - ... through v6 for run results
   - `parse_sources_v1(sources: dict) -> SourcesV1`
   - ... through v3 for sources

### Version Detection

`get_dbt_schema_version()` (in `dbt_artifacts_parser/parsers/utils.py`) extracts the `metadata.dbt_schema_version` field from artifacts:
- Format: `https://schemas.getdbt.com/dbt/{artifact_type}/{version}.json`
- Example: `https://schemas.getdbt.com/dbt/manifest/v12.json`

### Type Mapping

`ArtifactTypes` enum (in `dbt_artifacts_parser/parsers/version_map.py`) maps schema URLs to Pydantic model classes:
```python
MANIFEST_V12 = ArtifactType(
    "https://schemas.getdbt.com/dbt/manifest/v12.json",
    ManifestV12
)
```

## Common Tasks for AI Assistants

### Adding a new artifact version

1. Check if JSON schema is available at dbt-core repository
2. Download and save to `dbt_artifacts_parser/resources/`
3. Update `dev/generate_parser_classes.sh`
4. Run code generation
5. Update `version_map.py`, `parser.py`, and tests
6. Verify with tests

### Fixing a bug in parser logic

1. Check if the issue is in generated code (DO NOT MODIFY) or custom code
2. If in generated code, the fix must be in the upstream JSON schema
3. If in custom code (parser.py, utils.py, base.py), make changes
4. Add/update tests
5. Run full test suite
6. Lint and commit

### Updating dependencies

1. Modify `pyproject.toml` dependencies
2. Run `make setup-python` to regenerate lock file
3. Test thoroughly (especially Pydantic-related changes)
4. Update CI if needed (test matrix, constraints)

### Debugging test failures

1. Check which artifact version is failing
2. Look at test fixtures in `tests/resources/{artifact_type}/{version}/`
3. Verify the fixture matches the schema version
4. Run single test: `pytest tests/test_parser.py::TestManifestParser::test_parse_manifest[v12-...]`
5. Check for schema changes in dbt-core

## Important Notes for AI Assistants

1. **NEVER edit generated parser files** - This cannot be stressed enough
2. **Use existing test fixtures** - They're real dbt artifacts from jaffle_shop
3. **Follow Apache 2.0 license headers** - All files need the header comment
4. **Maintain backward compatibility** - Don't break existing parser functions
5. **Test across Python versions** - CI tests 3.10-3.13, but code targets 3.9+
6. **Update README** - Keep version compatibility table current
7. **Follow Pydantic v2 patterns** - No Pydantic v1 compatibility needed
8. **Respect the implementation policies** - See CONTRIBUTING.md

## Key Files to Reference

- **Understanding the parser API**: `dbt_artifacts_parser/parser.py`
- **Adding new versions**: `dev/generate_parser_classes.sh` and `dbt_artifacts_parser/parsers/version_map.py`
- **Understanding tests**: `tests/test_parser.py`
- **Configuration**: `pyproject.toml`, `.pre-commit-config.yaml`, `.pylintrc`
- **Contributing guidelines**: `CONTRIBUTING.md`
- **User documentation**: `README.md`

## Quick Reference Commands

```bash
# Setup
make setup                 # Full setup (deps + pre-commit)
make setup-python         # Install dependencies only
make setup-pre-commit     # Setup pre-commit hooks only

# Development
make lint                 # Run all linters
make test                 # Run test suite
make build                # Full build (clean + lint + test + build)
make clean                # Clean build artifacts

# Pre-commit
make run-pre-commit       # Run pre-commit on all files
make update-pre-commit    # Update pre-commit hook versions

# Publishing (maintainers only)
make test-publish         # Publish to TestPyPI
make publish              # Publish to PyPI
```

## Contact and Resources

- **Repository**: https://github.com/yu-iskw/dbt-artifacts-parser
- **PyPI**: https://pypi.org/project/dbt-artifacts-parser
- **Issues**: https://github.com/yu-iskw/dbt-artifacts-parser/issues
- **dbt Documentation**: https://docs.getdbt.com/reference/artifacts/dbt-artifacts
- **dbt Schemas**: https://github.com/dbt-labs/dbt-core/tree/main/schemas/dbt

---

**Last Updated**: 2026-02-06
**For**: Version 0.12.0
