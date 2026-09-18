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
"""Dispatch producer-compatibility rules by artifact schema URL."""

from __future__ import annotations

import copy
from typing import Callable, Optional

from dbt_artifacts_parser.compatibility.manifest import normalize_manifest_v12
from dbt_artifacts_parser.compatibility.run_results import normalize_run_results_v6
from dbt_artifacts_parser.compatibility.sources import normalize_sources_v3
from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version
from dbt_artifacts_parser.parsers.version_map import ArtifactTypes

Normalizer = Callable[[dict], None]

_NORMALIZERS: dict[str, Normalizer] = {
    ArtifactTypes.MANIFEST_V12.value.dbt_schema_version: normalize_manifest_v12,
    ArtifactTypes.SOURCES_V3.value.dbt_schema_version: normalize_sources_v3,
    ArtifactTypes.RUN_RESULTS_V6.value.dbt_schema_version: normalize_run_results_v6,
}


def get_normalizer(schema_version: str) -> Optional[Normalizer]:
    """Return the in-place normalizer for a schema URL, if any."""
    return _NORMALIZERS.get(schema_version)


def normalize_artifact(artifact: dict) -> dict:
    """Return a dict safe to validate against the canonical generated model.

    The input is not mutated. Artifacts without a matching rule are returned
    unchanged (same object) so large Core artifacts are not copied.
    """
    schema_version = get_dbt_schema_version(artifact_json=artifact)
    normalizer = get_normalizer(schema_version)
    if normalizer is None:
        return artifact
    payload = copy.deepcopy(artifact)
    normalizer(payload)
    return payload
