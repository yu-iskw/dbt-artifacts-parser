"""Compatibility handling for manifest.json producer differences."""

from copy import deepcopy
from typing import Any, Dict

_RESOURCE_COLLECTIONS = (
    "nodes",
    "sources",
    "exposures",
    "metrics",
    "semantic_models",
    "saved_queries",
    "unit_tests",
    "functions",
)

_SEED_V2_EXTRA_FIELDS = {
    "contract",
    "functions",
    "metrics",
    "refs",
    "sources",
}

_UNIT_TEST_V2_EXTRA_FIELDS = {
    "_event_status",
    "_pre_injected_sql",
    "alias",
    "build_path",
    "columns",
    "compiled",
    "compiled_code",
    "compiled_path",
    "contract",
    "database",
    "doc_blocks",
    "extra_ctes",
    "extra_ctes_injected",
    "functions",
    "language",
    "meta",
    "metrics",
    "patch_path",
    "raw_code",
    "refs",
    "relation_name",
    "sources",
    "tags",
    "tested_node_unique_id",
    "this_input_node_unique_id",
    "unrendered_config",
}


def _normalize_resource_item(item: Dict[str, Any]) -> None:
    item.pop("classifiers", None)
    item.pop("static_analysis_off_reason", None)
    depends_on = item.get("depends_on")
    if isinstance(depends_on, dict):
        depends_on.pop("nodes_with_ref_location", None)

    if item.get("resource_type") == "seed":
        for field_name in _SEED_V2_EXTRA_FIELDS:
            item.pop(field_name, None)
        if isinstance(depends_on, dict):
            depends_on.pop("nodes", None)


def normalize_manifest_v12(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize known dbt v2 producer differences for manifest/v12.

    dbt v2 currently emits several Fusion-only fields while retaining the
    public manifest/v12 schema URL. This adapter removes only fields known to
    be outside that schema and canonicalizes the unit-test checksum shape.
    Unknown fields remain untouched so strict Pydantic validation still
    catches unrecognized drift.
    """
    normalized = deepcopy(manifest)

    for collection_name in _RESOURCE_COLLECTIONS:
        collection = normalized.get(collection_name)
        if not isinstance(collection, dict):
            continue
        for item in collection.values():
            if isinstance(item, dict):
                _normalize_resource_item(item)

    disabled = normalized.get("disabled")
    if isinstance(disabled, dict):
        for disabled_items in disabled.values():
            if not isinstance(disabled_items, list):
                continue
            for item in disabled_items:
                if isinstance(item, dict):
                    _normalize_resource_item(item)

    unit_tests = normalized.get("unit_tests")
    if isinstance(unit_tests, dict):
        for unit_test in unit_tests.values():
            if not isinstance(unit_test, dict):
                continue
            for field_name in _UNIT_TEST_V2_EXTRA_FIELDS:
                unit_test.pop(field_name, None)
            checksum = unit_test.get("checksum")
            if isinstance(checksum, dict):
                checksum_value = checksum.get("checksum")
                unit_test["checksum"] = (
                    checksum_value if isinstance(checksum_value, str) else None
                )

    return normalized
