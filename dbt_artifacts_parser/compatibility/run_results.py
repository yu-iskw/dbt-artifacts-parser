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
"""Compatibility rules for run_results.json v6.

Rule: run_results_v6_static_analysis_off_reason
    Artifact: run-results
    Schema: v6
    Producer: dbt Fusion / dbt 2.x
    Observed: results[*].static_analysis_off_reason (Fusion-only; skipped when null)
    Normalization: drop the key
    Removal: when run-results/v6 schema includes the field
"""

from __future__ import annotations

RESULT_PRODUCER_KEYS = frozenset({"static_analysis_off_reason"})


def normalize_run_results_v6(payload: dict) -> None:
    """Apply run-results v6 producer compatibility in place."""
    results = payload.get("results")
    if not isinstance(results, list):
        return
    for result in results:
        if not isinstance(result, dict):
            continue
        for key in RESULT_PRODUCER_KEYS:
            result.pop(key, None)
