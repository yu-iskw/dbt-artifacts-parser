"""Compatibility handling for sources.json producer differences."""

from copy import deepcopy
from typing import Any, Dict

_DBT_V2_FRESHNESS_STATUS_MAP = {
    "Pass": "pass",
    "Warn": "warn",
    "Error": "error",
}


def normalize_sources_v3(sources: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize known dbt v2 sources/v3 wire differences.

    dbt v2/Fusion can serialize FreshnessStatus using Rust enum variant names
    (Pass, Warn, Error) while the published sources/v3 schema uses lowercase
    values. Normalize only that exact field and leave the caller's input object
    unchanged.

    Args:
        sources: Parsed sources.json payload.

    Returns:
        The original payload when no compatibility change is needed, otherwise
        a copied payload with canonical freshness statuses.
    """
    results = sources.get("results")
    if not isinstance(results, list):
        return sources

    normalized = None
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            continue

        status = result.get("status")
        canonical_status = (
            _DBT_V2_FRESHNESS_STATUS_MAP.get(status)
            if isinstance(status, str)
            else None
        )
        if canonical_status is None:
            continue

        if normalized is None:
            normalized = deepcopy(sources)

        normalized_results = normalized.get("results")
        if not isinstance(normalized_results, list):
            return sources

        normalized_result = normalized_results[index]
        if isinstance(normalized_result, dict):
            normalized_result["status"] = canonical_status

    return normalized if normalized is not None else sources
