#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the License); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Smoke-test parsers against JSON fixtures under tests/resources.

Uses repository-relative paths (not get_project_root from site-packages) so this
works after ``pip install`` of the wheel while fixtures come from checkout.
Repository root is resolved from this file's location only (no environment
variables).
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import traceback
from pathlib import Path

from dbt_artifacts_parser import parser

logger = logging.getLogger(__name__)

_KINDS = ("catalog", "manifest", "run_results")
_VERSION_DIR = re.compile(r"^v\d+$")

GENERIC_PARSER = {
    "catalog": parser.parse_catalog,
    "manifest": parser.parse_manifest,
    "run_results": parser.parse_run_results,
}


def expected_schema_url(kind: str, version: str) -> str:
    if kind == "run_results":
        return f"https://schemas.getdbt.com/dbt/run-results/{version}.json"
    return f"https://schemas.getdbt.com/dbt/{kind}/{version}.json"


def specific_parser_name(kind: str, version: str) -> str:
    if kind == "catalog":
        return f"parse_catalog_{version}"
    if kind == "manifest":
        return f"parse_manifest_{version}"
    if kind == "run_results":
        return f"parse_run_results_{version}"
    raise ValueError(f"unknown kind: {kind}")


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def iter_fixture_files(resources: Path) -> list[tuple[str, str, Path]]:
    """Return sorted list of (kind, version, path) for each JSON fixture."""
    found: list[tuple[str, str, Path]] = []
    for kind in _KINDS:
        kind_dir = resources / kind
        if not kind_dir.is_dir():
            continue
        for path in sorted(kind_dir.rglob("*.json")):
            try:
                rel = path.relative_to(kind_dir)
            except ValueError:
                continue
            if not rel.parts:
                continue
            version_dir = rel.parts[0]
            if not _VERSION_DIR.match(version_dir):
                logger.warning("skip (unexpected layout): %s", path)
                continue
            found.append((kind, version_dir, path))
    return found


def verify_file(kind: str, version: str, path: Path) -> list[str]:
    """Return list of error messages (empty if ok)."""
    errors: list[str] = []
    try:
        with path.open(encoding="utf-8") as fp:
            data = json.load(fp)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: load failed: {exc}"]

    expected = expected_schema_url(kind, version)

    try:
        obj = GENERIC_PARSER[kind](data)
        if obj.metadata.dbt_schema_version != expected:
            errors.append(
                f"{path}: generic parse\n"
                f"  metadata.dbt_schema_version "
                f"{obj.metadata.dbt_schema_version!r} != {expected!r}"
            )
    # pylint: disable=broad-exception-caught
    except Exception:
        errors.append(f"{path}: generic parse failed:\n{traceback.format_exc()}")

    try:
        fn = getattr(parser, specific_parser_name(kind, version))
        obj = fn(data)
        if obj.metadata.dbt_schema_version != expected:
            errors.append(
                f"{path}: specific parse\n"
                f"  metadata.dbt_schema_version "
                f"{obj.metadata.dbt_schema_version!r} != {expected!r}"
            )
    # pylint: disable=broad-exception-caught
    except Exception:
        errors.append(f"{path}: specific parse failed:\n{traceback.format_exc()}")

    return errors


def main() -> int:
    arg_parser = argparse.ArgumentParser(
        description="Verify parsers against tests/resources JSON fixtures.",
    )
    arg_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging (repo root, fixtures, per-file progress).",
    )
    cli_args = arg_parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if cli_args.verbose else logging.WARNING,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    repo_root = resolve_repo_root()
    logger.debug("repo_root=%s", repo_root)
    resources = repo_root / "tests" / "resources"
    logger.debug("resources=%s", resources)
    if not resources.is_dir():
        print(
            f"tests/resources not found under {repo_root}; "
            "run from repository checkout.",
            file=sys.stderr,
        )
        return 1

    fixtures = iter_fixture_files(resources)
    logger.debug("fixture_count=%d", len(fixtures))
    if not fixtures:
        print("No JSON fixtures discovered.", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for kind, version, path in fixtures:
        logger.debug("verify kind=%s version=%s path=%s", kind, version, path)
        all_errors.extend(verify_file(kind, version, path))

    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        return 1

    logger.debug("all fixtures passed")
    print(f"OK: verified {len(fixtures)} JSON fixture(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
