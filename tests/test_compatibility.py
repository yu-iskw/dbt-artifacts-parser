#
#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
"""Producer-compatibility tests for dbt 2.x JSON artifacts.

These fixtures encode known Fusion/dbt 2.x wire differences against the
published artifact schemas. They are not a substitute for regenerating
models when dbt publishes a new schema version.
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from dbt_artifacts_parser.compatibility.manifest import normalize_manifest_v12
from dbt_artifacts_parser.compatibility.normalize import normalize_artifact
from dbt_artifacts_parser.compatibility.sources import normalize_sources_v3
from dbt_artifacts_parser.parser import (
    parse_manifest,
    parse_manifest_v12,
    parse_run_results,
    parse_run_results_v6,
    parse_sources,
    parse_sources_v3,
)
from dbt_artifacts_parser.parsers.manifest.manifest_v12 import ManifestV12
from dbt_artifacts_parser.parsers.sources.sources_v3 import Status1
from dbt_artifacts_parser.utils import get_project_root

MANIFEST_V12_URL = "https://schemas.getdbt.com/dbt/manifest/v12.json"
SOURCES_V3_URL = "https://schemas.getdbt.com/dbt/sources/v3.json"
RUN_RESULTS_V6_URL = "https://schemas.getdbt.com/dbt/run-results/v6.json"


def _compat_path(*parts: str) -> str:
    return os.path.join(get_project_root(), "tests", "resources", *parts)


def _load_json(*parts: str) -> dict:
    with open(_compat_path(*parts), encoding="utf-8") as handle:
        return json.load(handle)


def _checksum(value: str = "abc") -> dict:
    return {"name": "sha256", "checksum": value}


def _minimal_manifest(**overrides: object) -> dict:
    payload = {
        "metadata": {
            "dbt_schema_version": MANIFEST_V12_URL,
            "dbt_version": "2.0.0",
        },
        "nodes": {},
        "sources": {},
        "macros": {},
        "docs": {},
        "exposures": {},
        "metrics": {},
        "groups": {},
        "selectors": {},
        "disabled": {},
        "parent_map": {},
        "child_map": {},
        "group_map": {},
        "saved_queries": {},
        "semantic_models": {},
        "unit_tests": {},
        "functions": {},
    }
    payload.update(overrides)
    return payload


def _model_node() -> dict:
    return {
        "database": "analytics",
        "schema": "dbt",
        "name": "customers",
        "resource_type": "model",
        "package_name": "jaffle_shop",
        "path": "models/customers.sql",
        "original_file_path": "models/customers.sql",
        "unique_id": "model.jaffle_shop.customers",
        "fqn": ["jaffle_shop", "customers"],
        "alias": "customers",
        "checksum": _checksum("model"),
        "config": {"tags": ["core"], "custom_team_key": "analytics"},
        "tags": ["core"],
        "classifiers": ["pii"],
        "depends_on": {
            "macros": [],
            "nodes": ["model.jaffle_shop.stg_customers"],
            "nodes_with_ref_location": [
                ["model.jaffle_shop.stg_customers", {"file": "models/customers.sql"}]
            ],
        },
    }


def _operation_node() -> dict:
    return {
        "database": "analytics",
        "schema": "dbt",
        "name": "on_run_end",
        "resource_type": "operation",
        "package_name": "jaffle_shop",
        "path": "hooks/on_run_end.sql",
        "original_file_path": "hooks/on_run_end.sql",
        "unique_id": "operation.jaffle_shop.on_run_end",
        "fqn": ["jaffle_shop", "hooks", "on_run_end"],
        "alias": "on_run_end",
        "checksum": _checksum("op"),
        "config": {"tags": ["hook"], "custom_hook": "keep-me"},
        "tags": ["hourly"],
        "classifiers": ["internal"],
        "depends_on": {
            "macros": ["macro.jaffle_shop.log"],
            "nodes": [],
            "nodes_with_ref_location": [],
        },
    }


def _seed_node() -> dict:
    return {
        "database": "analytics",
        "schema": "raw",
        "name": "raw_customers",
        "resource_type": "seed",
        "package_name": "jaffle_shop",
        "path": "seeds/raw_customers.csv",
        "original_file_path": "seeds/raw_customers.csv",
        "unique_id": "seed.jaffle_shop.raw_customers",
        "fqn": ["jaffle_shop", "raw_customers"],
        "alias": "raw_customers",
        "checksum": _checksum("seed"),
        "classifiers": ["raw"],
        "depends_on": {
            "macros": [],
            "nodes": [],
            "nodes_with_ref_location": [],
        },
    }


def _macro() -> dict:
    return {
        "name": "log",
        "resource_type": "macro",
        "package_name": "jaffle_shop",
        "path": "macros/log.sql",
        "original_file_path": "macros/log.sql",
        "unique_id": "macro.jaffle_shop.log",
        "macro_sql": "{% macro log() %}{% endmacro %}",
        "arguments": [{"name": "msg", "type": "string", "description": ""}],
        "depends_on": {"macros": [], "nodes": [], "nodes_with_ref_location": []},
    }


def _unit_test() -> dict:
    return {
        "model": "customers",
        "given": [{"input": "ref('stg_customers')", "rows": [{"id": 1}]}],
        "expect": {"rows": [{"id": 1}]},
        "name": "test_customers_ids",
        "resource_type": "unit_test",
        "package_name": "jaffle_shop",
        "path": "unit_tests/test_customers_ids.yml",
        "original_file_path": "unit_tests/test_customers_ids.yml",
        "unique_id": "unit_test.jaffle_shop.customers.test_customers_ids",
        "fqn": ["jaffle_shop", "customers", "test_customers_ids"],
        "overrides": {
            "macros": {"is_incremental": "false"},
            "vars": {"timezone": "UTC"},
        },
        "checksum": {"name": "none", "checksum": "deadbeef"},
        "classifiers": ["unit"],
        "tested_node_unique_id": "model.jaffle_shop.customers",
        "database": "analytics",
        "tags": ["unit"],
        "meta": {"owner": "analytics"},
        "alias": "test_customers_ids",
        "columns": {},
        "refs": [["customers"]],
        "sources": [],
        "functions": [],
        "unrendered_config": {},
        "metrics": [],
        "language": "sql",
        "contract": {"enforced": False},
        "depends_on": {
            "macros": [],
            "nodes": ["model.jaffle_shop.customers"],
            "nodes_with_ref_location": [],
        },
    }


def _fusion_manifest() -> dict:
    model = _model_node()
    operation = _operation_node()
    seed = _seed_node()
    return _minimal_manifest(
        nodes={
            model["unique_id"]: model,
            operation["unique_id"]: operation,
        },
        macros={_macro()["unique_id"]: _macro()},
        unit_tests={_unit_test()["unique_id"]: _unit_test()},
        disabled={seed["unique_id"]: [seed]},
        parent_map={
            model["unique_id"]: ["model.jaffle_shop.stg_customers"],
            operation["unique_id"]: [],
        },
        child_map={
            "model.jaffle_shop.stg_customers": [model["unique_id"]],
        },
    )


class TestNormalizeDoesNotMutateInput:
    def test_sources_status_alias_leaves_caller_dict_unchanged(self):
        original = _load_json("compat", "fusion", "sources_v3.json")
        snapshot = copy.deepcopy(original)
        normalized = normalize_artifact(original)
        assert original == snapshot
        assert normalized is not original
        assert normalized["results"][0]["status"] == "pass"
        assert original["results"][0]["status"] == "Pass"

    def test_schema_without_rules_returns_same_object(self):
        catalog = {
            "metadata": {
                "dbt_schema_version": "https://schemas.getdbt.com/dbt/catalog/v1.json"
            }
        }
        assert normalize_artifact(catalog) is catalog


class TestSourcesV3Compatibility:
    def test_core_fixture_parses_without_aliases(self):
        sources = _load_json("sources", "v3", "jaffle_shop", "sources.json")
        parsed = parse_sources(sources)
        assert parsed.metadata.dbt_schema_version == SOURCES_V3_URL
        assert parsed.results[0].status == Status1.pass_
        assert parsed.results[0].criteria.warn_after.period.value == "hour"

    def test_fusion_capitalized_status_and_criteria_extras(self):
        sources = _load_json("compat", "fusion", "sources_v3.json")
        parsed = parse_sources(sources)
        statuses = [result.status.value for result in parsed.results]
        assert statuses == ["pass", "warn", "error"]
        criteria = parsed.results[0].criteria
        assert criteria.warn_after.count == 12
        dumped = criteria.model_dump()
        assert "loaded_at_field" not in dumped
        assert "loaded_at_query" not in dumped

    def test_pinned_parser_applies_the_same_rules(self):
        sources = _load_json("compat", "fusion", "sources_v3.json")
        parsed = parse_sources_v3(sources)
        assert parsed.results[0].status == Status1.pass_

    def test_does_not_rewrite_unrelated_pass_strings(self):
        payload = {
            "metadata": {"dbt_schema_version": SOURCES_V3_URL},
            "results": [
                {
                    "unique_id": "source.jaffle_shop.raw.customers",
                    "error": "Pass",
                    "status": "runtime error",
                }
            ],
            "elapsed_time": 0.0,
        }
        normalize_sources_v3(payload)
        assert payload["results"][0]["error"] == "Pass"
        assert payload["results"][0]["status"] == "runtime error"

    def test_unknown_extra_still_fails(self):
        sources = _load_json("compat", "fusion", "sources_v3.json")
        sources["future_only_field"] = "nope"
        with pytest.raises(ValidationError):
            parse_sources(sources)

    def test_fallback_to_latest_is_not_the_v2_mechanism(self):
        sources = _load_json("compat", "fusion", "sources_v3.json")
        parsed = parse_sources(sources, fallback_to_latest=True)
        assert parsed.metadata.dbt_schema_version == SOURCES_V3_URL
        newer = {
            "metadata": {
                "dbt_schema_version": "https://schemas.getdbt.com/dbt/sources/v99.json"
            },
            "results": [],
            "elapsed_time": 0.0,
        }
        with pytest.raises(ValueError, match="Not a sources.json"):
            parse_sources(newer)


class TestRunResultsV6Compatibility:
    def test_drops_static_analysis_off_reason_and_keeps_result_fields(self):
        run_results = _load_json("compat", "fusion", "run_results_v6.json")
        parsed = parse_run_results(run_results)
        assert parsed.metadata.dbt_schema_version == RUN_RESULTS_V6_URL
        result = parsed.results[0]
        assert result.status.value == "success"
        assert result.message == "Succeeded"
        assert result.unique_id == "model.jaffle_shop.customers"
        assert result.compiled_code == "select 1 as id"
        dumped = result.model_dump()
        assert "static_analysis_off_reason" not in dumped

    def test_pinned_parser_accepts_fusion_run_results(self):
        run_results = _load_json("compat", "fusion", "run_results_v6.json")
        parsed = parse_run_results_v6(run_results)
        assert parsed.results[0].unique_id == "model.jaffle_shop.customers"


class TestManifestV12Compatibility:
    def test_existing_core_1_12_fixture_still_parses(self):
        path = _compat_path("manifest", "v12", "jaffle_shop", "manifest_1.12.json")
        with open(path, encoding="utf-8") as handle:
            manifest = json.load(handle)
        parsed = parse_manifest(manifest)
        assert parsed.metadata.dbt_schema_version == MANIFEST_V12_URL
        node = parsed.nodes["model.jaffle_shop.stg_customers"]
        assert node.config is not None
        unit_test = next(iter(parsed.unit_tests.values()))
        assert unit_test.given
        assert unit_test.expect is not None
        macro = next(iter(parsed.macros.values()))
        assert macro.macro_sql is not None

    def test_fusion_manifest_keeps_semantic_fields(self):
        parsed = parse_manifest(_fusion_manifest())
        model = parsed.nodes["model.jaffle_shop.customers"]
        assert model.depends_on.nodes == ["model.jaffle_shop.stg_customers"]
        assert model.tags == ["core"]
        assert model.config.model_extra["custom_team_key"] == "analytics"
        dumped_depends = model.depends_on.model_dump()
        assert "nodes_with_ref_location" not in dumped_depends

        operation = parsed.nodes["operation.jaffle_shop.on_run_end"]
        assert operation.tags == ["hourly"]
        assert operation.config.model_extra["custom_hook"] == "keep-me"
        assert operation.depends_on.macros == ["macro.jaffle_shop.log"]

        unit_test = parsed.unit_tests[
            "unit_test.jaffle_shop.customers.test_customers_ids"
        ]
        assert unit_test.overrides.macros == {"is_incremental": "false"}
        assert unit_test.overrides.vars == {"timezone": "UTC"}
        assert unit_test.checksum == "deadbeef"
        assert unit_test.depends_on.nodes == ["model.jaffle_shop.customers"]

        seed = parsed.disabled["seed.jaffle_shop.raw_customers"][0]
        seed_depends = seed.depends_on.model_dump(exclude_none=True)
        assert seed_depends.get("macros") == []
        assert "nodes" not in seed_depends

        macro = parsed.macros["macro.jaffle_shop.log"]
        assert macro.arguments[0].name == "msg"
        macro_depends = macro.depends_on.model_dump(exclude_none=True)
        assert "nodes" not in macro_depends

    def test_pinned_parser_accepts_fusion_manifest(self):
        parsed = parse_manifest_v12(_fusion_manifest())
        assert isinstance(parsed, ManifestV12)

    def test_unknown_model_extra_still_fails(self):
        manifest = _fusion_manifest()
        manifest["nodes"]["model.jaffle_shop.customers"]["totally_unknown_field"] = 1
        with pytest.raises(ValidationError):
            parse_manifest(manifest)

    def test_fallback_to_latest_is_not_used_for_same_schema_producer_drift(self):
        parsed = parse_manifest(_fusion_manifest(), fallback_to_latest=False)
        assert parsed.metadata.dbt_schema_version == MANIFEST_V12_URL
        newer = {
            "metadata": {
                "dbt_schema_version": "https://schemas.getdbt.com/dbt/manifest/v99.json"
            }
        }
        with pytest.raises(ValueError, match="Not a manifest.json"):
            parse_manifest(newer)

    def test_does_not_strip_classifiers_inside_meta(self):
        resource = {
            "resource_type": "model",
            "meta": {"classifiers": ["keep-me"]},
            "classifiers": ["drop-me"],
            "depends_on": {
                "macros": [],
                "nodes": ["a"],
                "nodes_with_ref_location": ["x"],
            },
        }
        payload = {"nodes": {"model.x": resource}}
        normalize_manifest_v12(payload)
        assert "classifiers" not in payload["nodes"]["model.x"]
        assert payload["nodes"]["model.x"]["meta"]["classifiers"] == ["keep-me"]
        assert payload["nodes"]["model.x"]["depends_on"]["nodes"] == ["a"]
        depends_on = payload["nodes"]["model.x"]["depends_on"]
        assert "nodes_with_ref_location" not in depends_on


class TestGeneratedModelsStayCanonical:
    def test_generated_parser_modules_do_not_import_compatibility(self):
        parsers_root = Path(get_project_root()) / "dbt_artifacts_parser" / "parsers"
        generated = [
            path for path in parsers_root.glob("*/*.py") if path.name != "__init__.py"
        ]
        assert generated
        for path in generated:
            text = path.read_text(encoding="utf-8")
            assert text.startswith("# generated by datamodel-codegen:")
            assert "dbt_artifacts_parser.compatibility" not in text

    def test_sources_v3_enum_remains_lowercase(self):
        text = (
            Path(get_project_root())
            / "dbt_artifacts_parser"
            / "parsers"
            / "sources"
            / "sources_v3.py"
        ).read_text(encoding="utf-8")
        assert 'pass_ = "pass"' in text
        assert 'warn = "warn"' in text
        assert '"Pass"' not in text
