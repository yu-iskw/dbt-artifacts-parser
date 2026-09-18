"""Validate artifacts emitted by the dbt v2 compatibility canary."""

import json
import sys
from pathlib import Path

from dbt_artifacts_parser import parser


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def main(artifact_dir: Path) -> None:
    raw_manifest = load_json(artifact_dir / "manifest.json")
    manifest = parser.parse_manifest(raw_manifest)

    operation_ids = [
        unique_id
        for unique_id in raw_manifest["nodes"]
        if unique_id.startswith("operation.")
    ]
    assert operation_ids, "expected the on-run-start hook to produce an operation node"
    for unique_id in operation_ids:
        raw_node = raw_manifest["nodes"][unique_id]
        assert unique_id in manifest.nodes
        missing_legacy_fields = [
            field_name
            for field_name in ("config", "tags")
            if field_name not in raw_node
        ]
        if missing_legacy_fields:
            print(
                "dbt v2 operation node omits legacy fields: "
                + ", ".join(missing_legacy_fields)
            )

    unit_test_id = "unit_test.dbt_v2_canary.unit_target.unit_target_returns_one"
    assert unit_test_id in raw_manifest["unit_tests"]
    raw_overrides = raw_manifest["unit_tests"][unit_test_id].get("overrides")
    assert raw_overrides
    assert raw_overrides.get("vars", {}).get("compatibility_mode") == "'v2'"
    parsed_unit_test = manifest.unit_tests[unit_test_id]
    assert parsed_unit_test.overrides is not None
    assert parsed_unit_test.overrides.vars["compatibility_mode"] == "'v2'"

    macro_id = "macro.dbt_v2_canary.compat_macro"
    assert macro_id in raw_manifest["macros"]
    assert raw_manifest["macros"][macro_id].get("arguments")
    assert manifest.macros[macro_id].arguments

    raw_run_results = load_json(artifact_dir / "run_results.json")
    run_results = parser.parse_run_results(raw_run_results)
    assert run_results.results
    assert any(
        result.static_analysis_off_reason is not None
        for result in run_results.results
    ), "expected a dbt v2 static_analysis_off_reason result field"

    raw_sources = load_json(artifact_dir / "sources.json")
    raw_statuses = {result["status"] for result in raw_sources["results"]}
    assert raw_statuses <= {"Pass", "Warn", "Error", "runtime error"}
    sources = parser.parse_sources(raw_sources)
    normalized_statuses = {result.status.value for result in sources.results}
    assert normalized_statuses <= {"pass", "warn", "error", "runtime error"}

    catalog = parser.parse_catalog(load_json(artifact_dir / "catalog.json"))
    assert catalog.metadata.dbt_schema_version.endswith("/catalog/v1.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_dbt_v2_canary.py <artifact-dir>")
    main(Path(sys.argv[1]))
