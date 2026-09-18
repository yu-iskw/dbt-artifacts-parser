"""Compatibility overlays for producer-level dbt artifact differences.

Generated parser models remain aligned with the published dbt JSON schemas.
This package contains narrowly scoped handling for observed producer output
that keeps the same dbt_schema_version while differing from that schema.
"""

from dbt_artifacts_parser.compatibility.run_results import (
    RunResultV6Compat,
    RunResultsV6Compat,
)
from dbt_artifacts_parser.compatibility.sources import normalize_sources_v3

__all__ = [
    "RunResultV6Compat",
    "RunResultsV6Compat",
    "normalize_sources_v3",
]
