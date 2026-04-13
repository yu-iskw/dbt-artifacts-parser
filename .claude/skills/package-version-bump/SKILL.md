---
name: package-version-bump
description: Bumps the dbt-artifacts-parser package semver, prepares a PyPI release, and aligns GitHub Releases with __version__. Use when the user asks to bump the library version, prepare a release, tag a version, or ship to PyPI—not for upgrading project dependencies or lockfile pins.
---

# Package Version Bump

## Trigger scenarios

Activate this skill when the user says or implies:

- Bump version, release version, next patch/minor/major
- Prepare a release, ship to PyPI, publish the package
- Set version to a specific semver (e.g. `0.14.0`)
- Tag or GitHub Release in the context of **this library’s** version

## Not this skill

- **Dependency / lockfile bumps** (e.g. Renovate, “upgrade deps”): use `make upgrade-deps` (`uv lock --upgrade && uv sync`) and edits to [pyproject.toml](../../../pyproject.toml) constraints—not `__version__` in the package.

## Single source of truth

- The published package version is **`__version__`** in [dbt_artifacts_parser/__init__.py](../../../dbt_artifacts_parser/__init__.py).
- [pyproject.toml](../../../pyproject.toml) sets `dynamic = ["version"]` and `[tool.hatch.version] path = "dbt_artifacts_parser/__init__.py"` so the **Hatch CLI** can bump that file.

Run all commands from the **repository root**.

## Bump the version

Choose one path.

### Preferred: Hatch CLI via uvx

The `hatch` CLI is not a project dev dependency; use ephemeral install:

```bash
uvx hatch version patch
# or: uvx hatch version minor
# or: uvx hatch version major
```

To set an explicit version:

```bash
uvx hatch version 0.14.0
```

### Fallback: manual edit

Edit only the `__version__ = "..."` assignment in [dbt_artifacts_parser/__init__.py](../../../dbt_artifacts_parser/__init__.py).

## Verify

- Confirm the string: `uv run python -c 'import dbt_artifacts_parser; print(dbt_artifacts_parser.__version__)'`
- Optionally: `uv build` and/or `make test` before releasing.

## Ship (PyPI)

Publishing is automated when a **GitHub Release** is created (workflow [publish.yml](../../../.github/workflows/publish.yml) on `release: created` → [dev/publish.sh](../../../dev/publish.sh)).

1. Commit the version change on the branch you release from (typically `main`).
2. **Create a GitHub Release** (this triggers CI publish). Prefer a tag aligned with semver, e.g. `v0.14.0` for `0.14.0`.

Local publish (maintainers): `make publish` or `make test-publish` — same scripts as CI; still requires `__version__` updated first.

## Do not

- Do **not** rely on a git tag or Release title alone: the wheel/sdist **must** reflect the updated `__version__` or users and PyPI metadata will disagree with the tag.

## Optional

- Add `hatch` to `[project.optional-dependencies].dev` if you prefer `uv run hatch version …` without `uvx`.
