#!/usr/bin/env python3
"""Detect structural drift in published dbt Core artifact schemas."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

DBT_CORE_REPOSITORY = "dbt-labs/dbt-core"
ARTIFACT_CATEGORIES = ("catalog", "manifest", "run-results", "sources")
IGNORED_SCHEMA_KEYS = frozenset({"default", "description"})
STABLE_V1_TAG = re.compile(r"^v1\.(\d+)\.(\d+)$")
SCHEMA_VERSION = re.compile(r"(?:^|[_-])v(\d+)\.json$")
GITHUB_API_VERSION = "2022-11-28"
REQUEST_TIMEOUT_SECONDS = 30
MAX_DIFF_PATHS = 20


def github_headers() -> dict[str, str]:
    """Return headers for authenticated or anonymous GitHub API requests."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "dbt-artifacts-schema-drift-check",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str) -> Any:
    """Fetch and decode a JSON document."""
    request = Request(url, headers=github_headers())
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:  # noqa: S310
        return json.load(response)


def latest_stable_v1_tag(repository: str) -> str:
    """Resolve the highest stable dbt Core v1 semantic version."""
    candidates: list[tuple[tuple[int, int], str]] = []
    for page in range(1, 11):
        releases = fetch_json(
            f"https://api.github.com/repos/{repository}/releases"
            f"?per_page=100&page={page}"
        )
        for release in releases:
            if release.get("draft") or release.get("prerelease"):
                continue
            tag = release.get("tag_name", "")
            match = STABLE_V1_TAG.fullmatch(tag)
            if match:
                candidates.append(((int(match.group(1)), int(match.group(2))), tag))
        if len(releases) < 100:
            break
    if not candidates:
        raise RuntimeError("No stable dbt Core v1 release found")
    return max(candidates)[1]


def contents(repository: str, path: str, ref: str) -> list[dict[str, Any]]:
    """List a GitHub repository directory at a ref."""
    encoded_path = "/".join(quote(part, safe="") for part in path.split("/"))
    encoded_ref = quote(ref, safe="")
    result = fetch_json(
        f"https://api.github.com/repos/{repository}/contents/"
        f"{encoded_path}?ref={encoded_ref}"
    )
    if not isinstance(result, list):
        raise RuntimeError(f"Expected directory listing for {path} at {ref}")
    return result


def schema_version(filename: str) -> int | None:
    """Extract a schema version from supported local and upstream filenames."""
    match = SCHEMA_VERSION.search(filename)
    return int(match.group(1)) if match else None


def canonicalize(value: Any) -> Any:
    """Remove non-structural fields and normalize object key ordering."""
    if isinstance(value, Mapping):
        return {
            key: canonicalize(item)
            for key, item in sorted(value.items())
            if key not in IGNORED_SCHEMA_KEYS
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [canonicalize(item) for item in value]
    return value


def differing_paths(left: Any, right: Any, path: str = "$") -> list[str]:
    """Return a bounded list of paths whose canonical values differ."""
    differences: list[str] = []

    def visit(left_value: Any, right_value: Any, current_path: str) -> None:
        if len(differences) >= MAX_DIFF_PATHS:
            return
        if isinstance(left_value, Mapping):
            if not isinstance(right_value, Mapping):
                differences.append(current_path)
                return
            keys = sorted(set(left_value) | set(right_value))
            for key in keys:
                child_path = f"{current_path}.{key}"
                if key not in left_value or key not in right_value:
                    differences.append(child_path)
                else:
                    visit(left_value[key], right_value[key], child_path)
                if len(differences) >= MAX_DIFF_PATHS:
                    return
            return
        if isinstance(left_value, list):
            if not isinstance(right_value, list):
                differences.append(current_path)
                return
            if len(left_value) != len(right_value):
                differences.append(f"{current_path}.length")
            for index, (left_item, right_item) in enumerate(
                zip(left_value, right_value, strict=False)
            ):
                visit(left_item, right_item, f"{current_path}[{index}]")
                if len(differences) >= MAX_DIFF_PATHS:
                    return
            return
        if left_value != right_value:
            differences.append(current_path)

    visit(left, right, path)
    return differences


def latest_local_schema(schema_directory: Path) -> tuple[int, Path] | None:
    """Find the highest versioned JSON schema in a local category directory."""
    candidates = [
        (version, path)
        for path in schema_directory.glob("*.json")
        if (version := schema_version(path.name)) is not None
    ]
    return max(candidates, default=None, key=lambda item: item[0])


def latest_upstream_schema(
    repository: str, category: str, ref: str
) -> tuple[int, dict[str, Any]]:
    """Find the highest schema version published upstream for a category."""
    entries = contents(repository, f"schemas/dbt/{category}", ref)
    candidates = [
        (version, entry)
        for entry in entries
        if entry.get("type") == "file"
        and (version := schema_version(entry.get("name", ""))) is not None
    ]
    if not candidates:
        raise RuntimeError(f"No upstream schemas found for {category} at {ref}")
    return max(candidates, key=lambda item: item[0])


def write_step_summary(lines: list[str]) -> None:
    """Append results to the GitHub Actions step summary when available."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with Path(summary_path).open("a", encoding="utf-8") as summary:
            summary.write("\n".join(lines) + "\n")


def check_drift(schema_root: Path, repository: str, ref: str) -> list[str]:
    """Compare the latest local schemas with a stable upstream dbt Core ref."""
    issues: list[str] = []
    root_entries = contents(repository, "schemas/dbt", ref)
    upstream_categories = {
        entry["name"] for entry in root_entries if entry.get("type") == "dir"
    }
    expected_categories = set(ARTIFACT_CATEGORIES)
    for category in sorted(upstream_categories - expected_categories):
        issues.append(f"New upstream artifact category: {category}")
    for category in sorted(expected_categories - upstream_categories):
        issues.append(f"Upstream artifact category disappeared: {category}")

    for category in ARTIFACT_CATEGORIES:
        if category not in upstream_categories:
            continue
        upstream_version, upstream_entry = latest_upstream_schema(
            repository, category, ref
        )
        local = latest_local_schema(schema_root / category)
        if local is None:
            issues.append(f"No local schema found for {category}")
            continue
        local_version, local_path = local
        if upstream_version != local_version:
            issues.append(
                f"{category}: local v{local_version}, upstream v{upstream_version}"
            )
            continue

        with local_path.open(encoding="utf-8") as local_file:
            local_schema = canonicalize(json.load(local_file))
        upstream_schema = canonicalize(fetch_json(upstream_entry["download_url"]))
        if local_schema != upstream_schema:
            paths = ", ".join(differing_paths(local_schema, upstream_schema))
            issues.append(
                f"{category} v{local_version}: structural drift at {paths}"
            )
    return issues


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema-root",
        required=True,
        type=Path,
        help="Directory containing one subdirectory per artifact category",
    )
    parser.add_argument(
        "--repository",
        default=DBT_CORE_REPOSITORY,
        help="Upstream repository in owner/name form",
    )
    parser.add_argument(
        "--ref",
        help="Stable dbt Core tag; defaults to the highest stable v1 release",
    )
    return parser.parse_args()


def main() -> int:
    """Run the drift check and render console and Actions summaries."""
    args = parse_args()
    ref = args.ref or latest_stable_v1_tag(args.repository)
    issues = check_drift(args.schema_root, args.repository, ref)
    if issues:
        lines = [f"## dbt schema drift detected ({ref})", ""]
        lines.extend(f"- {issue}" for issue in issues)
        print("\n".join(lines), file=sys.stderr)
        write_step_summary(lines)
        return 1

    lines = [
        f"## No dbt schema drift ({ref})",
        "",
        "The latest local catalog, manifest, run-results, and sources schemas "
        "match the latest stable dbt Core v1 release.",
    ]
    print("\n".join(lines))
    write_step_summary(lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
