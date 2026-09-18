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
"""Compatibility rules for sources.json v3.

Rule: sources_v3_freshness_status_case
    Artifact: sources
    Schema: v3
    Producer: dbt Fusion / dbt 2.x (serde emits PascalCase; no rename_all)
    Observed: results[*].status is Pass/Warn/Error instead of pass/warn/error
    Normalization: map those exact aliases onto the published enum
    Removal: when Fusion writes lowercase sources.json (or sources/v4 exists)

Rule: sources_v3_criteria_fusion_keys
    Artifact: sources
    Schema: v3
    Producer: dbt Fusion / dbt 2.x freshness writer
    Observed: criteria may include loaded_at_field / loaded_at_query
              (freshness/v0 shape written into sources/v3)
    Normalization: drop those keys; warn_after/error_after/filter are kept
    Removal: when sources/v3 schema adds the keys, or Fusion stops emitting them
"""

from __future__ import annotations

# Exact Fusion serde names. Do not fold arbitrary strings.
FRESHNESS_STATUS_ALIASES = {
    "Pass": "pass",
    "Warn": "warn",
    "Error": "error",
}

CRITERIA_PRODUCER_KEYS = frozenset({"loaded_at_field", "loaded_at_query"})


def normalize_sources_v3(payload: dict) -> None:
    """Apply sources v3 producer compatibility in place."""
    results = payload.get("results")
    if not isinstance(results, list):
        return
    for result in results:
        if not isinstance(result, dict):
            continue
        status = result.get("status")
        if isinstance(status, str) and status in FRESHNESS_STATUS_ALIASES:
            result["status"] = FRESHNESS_STATUS_ALIASES[status]
        criteria = result.get("criteria")
        if isinstance(criteria, dict):
            for key in CRITERIA_PRODUCER_KEYS:
                criteria.pop(key, None)
