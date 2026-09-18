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
"""Compatibility rules for manifest.json v12.

Rule: manifest_v12_nodes_with_ref_location
    Artifact: manifest
    Schema: v12
    Producer: dbt Fusion / dbt 2.x
    Observed: depends_on.nodes_with_ref_location on nodes/exposures/unit tests
    Normalization: drop the key; keep depends_on.nodes/macros
    Removal: when manifest/v12 schema includes the field

Rule: manifest_v12_resource_classifiers
    Artifact: manifest
    Schema: v12
    Producer: dbt Fusion / dbt 2.x
    Observed: resource-level classifiers
    Normalization: drop the key at resource top-level only (not inside meta/config)
    Removal: when the published schema includes classifiers

Rule: manifest_v12_generated_sql_file
    Artifact: manifest
    Schema: v12
    Producer: dbt Fusion / dbt 2.x
    Observed: test nodes include generated_sql_file
    Normalization: drop the key
    Removal: when the published test node schema includes the field

Rule: manifest_v12_seed_depends_on_nodes
    Artifact: manifest
    Schema: v12
    Producer: dbt Fusion / dbt 2.x
    Observed: seed/macro depends_on includes nodes (schema only allows macros)
    Normalization: drop depends_on.nodes for seed and macro resources only
    Removal: when those DependsOn schemas allow nodes

Rule: manifest_v12_unit_test_producer_fields
    Artifact: manifest
    Schema: v12
    Producer: dbt Fusion / dbt 2.x
    Observed: unit tests include extra node-shaped fields and FileHash checksum
    Normalization: drop known extras; coerce checksum object to its hash string
    Removal: when UnitTests schema matches Fusion output
"""

from __future__ import annotations

from typing import Iterator, Optional, Tuple

RESOURCE_COLLECTIONS = (
    "nodes",
    "sources",
    "macros",
    "docs",
    "exposures",
    "metrics",
    "groups",
    "unit_tests",
    "semantic_models",
    "saved_queries",
    "functions",
)

# Dropped at resource object top-level only — never walked into meta/config.
RESOURCE_PRODUCER_KEYS = frozenset(
    {
        "classifiers",
        "generated_sql_file",
    }
)

# Fusion unit-test nodes carry model-like extras the UnitTests schema forbids.
UNIT_TEST_PRODUCER_KEYS = RESOURCE_PRODUCER_KEYS | frozenset(
    {
        "tested_node_unique_id",
        "database",
        "alias",
        "columns",
        "refs",
        "sources",
        "functions",
        "unrendered_config",
        "metrics",
        "language",
        "contract",
        "tags",
        "meta",
    }
)

# Schema DependsOn for these types is macros-only.
MACRO_ONLY_DEPENDS_ON_TYPES = frozenset({"seed", "macro"})

UNIT_TEST_RESOURCE_TYPES = frozenset({"unit_test", "unit test"})


def _resource_type(resource: dict) -> Optional[str]:
    value = resource.get("resource_type")
    if isinstance(value, str):
        return value
    return None


def iter_resource_dicts(payload: dict) -> Iterator[Tuple[str, dict]]:
    """Yield (collection, resource dict) including disabled lists."""
    for collection in RESOURCE_COLLECTIONS:
        items = payload.get(collection)
        if isinstance(items, dict):
            for resource in items.values():
                if isinstance(resource, dict):
                    yield collection, resource
    disabled = payload.get("disabled")
    if isinstance(disabled, dict):
        for entries in disabled.values():
            if not isinstance(entries, list):
                continue
            for resource in entries:
                if isinstance(resource, dict):
                    yield "disabled", resource


def _is_unit_test(collection: str, resource: dict) -> bool:
    if collection == "unit_tests":
        return True
    return _resource_type(resource) in UNIT_TEST_RESOURCE_TYPES


def _normalize_checksum(resource: dict) -> None:
    checksum = resource.get("checksum")
    if isinstance(checksum, dict) and "checksum" in checksum:
        hash_value = checksum["checksum"]
        if isinstance(hash_value, str):
            resource["checksum"] = hash_value
        else:
            resource["checksum"] = str(hash_value)


def _normalize_depends_on(resource: dict) -> None:
    depends_on = resource.get("depends_on")
    if not isinstance(depends_on, dict):
        return
    depends_on.pop("nodes_with_ref_location", None)
    if _resource_type(resource) in MACRO_ONLY_DEPENDS_ON_TYPES:
        depends_on.pop("nodes", None)


def normalize_manifest_v12(payload: dict) -> None:
    """Apply manifest v12 producer compatibility in place."""
    for collection, resource in iter_resource_dicts(payload):
        if _is_unit_test(collection, resource):
            keys = UNIT_TEST_PRODUCER_KEYS
        else:
            keys = RESOURCE_PRODUCER_KEYS
        for key in keys:
            resource.pop(key, None)
        if _is_unit_test(collection, resource):
            _normalize_checksum(resource)
        _normalize_depends_on(resource)
