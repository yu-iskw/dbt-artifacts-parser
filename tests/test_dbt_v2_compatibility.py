import copy
import json
import os

import pytest
from pydantic import ValidationError

from dbt_artifacts_parser import parser
from dbt_artifacts_parser.compatibility.manifest import normalize_manifest_v12
from dbt_artifacts_parser.parsers.run_results.run_results_v6 import RunResultsV6
from dbt_artifacts_parser.utils import get_project_root


def _resource_path(*parts: str) -> str:
    return os.path.join(get_project_root(), "tests", "resources", *parts)


def _load_json(*parts: str) -> dict:
    with open(_resource_path(*parts), "r", encoding="utf-8") as fp:
        return json.load(fp)


@pytest.mark.parametrize(
    ("wire_status", "canonical_status"),
    [
        ("Pass", "pass"),
        ("Warn", "warn"),
        ("Error", "error"),
    ],
)
def test_sources_v3_normalizes_dbt_v2_freshness_status(
    wire_status: str,
    canonical_status: str,
):
    sources = _load_json(
        "sources",
        "v3",
        "dbt_v2",
        "sources_2.0.4_compat.json",
    )
    sources["results"][0]["status"] = wire_status
    original = copy.deepcopy(sources)

    parsed = parser.parse_sources(sources)

    assert parsed.results[0].status.value == canonical_status
    assert sources == original


def test_parse_sources_v3_specific_normalizes_dbt_v2_freshness_status():
    sources = _load_json(
        "sources",
        "v3",
        "dbt_v2",
        "sources_2.0.4_compat.json",
    )

    parsed = parser.parse_sources_v3(sources)

    assert parsed.results[0].status.value == "pass"


def test_run_results_v6_preserves_dbt_v2_static_analysis_off_reason():
    run_results = _load_json(
        "run_results",
        "v6",
        "dbt_v2",
        "run_results_2.0.4_compat.json",
    )

    parsed = parser.parse_run_results(run_results)

    assert isinstance(parsed, RunResultsV6)
    assert parsed.results[0].static_analysis_off_reason == "configuredoff"


def test_parse_run_results_v6_specific_preserves_dbt_v2_field():
    run_results = _load_json(
        "run_results",
        "v6",
        "dbt_v2",
        "run_results_2.0.4_compat.json",
    )

    parsed = parser.parse_run_results_v6(run_results)

    assert parsed.results[0].static_analysis_off_reason == "configuredoff"


def test_run_results_v6_stays_strict_for_unknown_fields():
    run_results = _load_json(
        "run_results",
        "v6",
        "dbt_v2",
        "run_results_2.0.4_compat.json",
    )
    run_results["results"][0]["unknown_future_field"] = "unexpected"

    with pytest.raises(ValidationError):
        parser.parse_run_results(run_results)


def test_manifest_v12_normalizer_is_narrow():
    manifest = {
        "nodes": {
            "model.compat.example": {
                "classifiers": [],
                "static_analysis_off_reason": "configuredoff",
                "depends_on": {
                    "nodes": [],
                    "nodes_with_ref_location": [],
                },
                "unknown_future_field": "must-survive-normalization",
            }
        },
        "unit_tests": {
            "unit_test.compat.example": {
                "checksum": {"name": "none", "checksum": ""},
                "database": "db",
                "tested_node_unique_id": "model.compat.example",
                "unknown_future_field": "must-survive-normalization",
            }
        },
    }
    original = copy.deepcopy(manifest)

    normalized = normalize_manifest_v12(manifest)

    assert manifest == original
    node = normalized["nodes"]["model.compat.example"]
    assert "classifiers" not in node
    assert "static_analysis_off_reason" not in node
    assert "nodes_with_ref_location" not in node["depends_on"]
    assert node["unknown_future_field"] == "must-survive-normalization"

    unit_test = normalized["unit_tests"]["unit_test.compat.example"]
    assert unit_test["checksum"] == ""
    assert "database" not in unit_test
    assert "tested_node_unique_id" not in unit_test
    assert unit_test["unknown_future_field"] == "must-survive-normalization"
