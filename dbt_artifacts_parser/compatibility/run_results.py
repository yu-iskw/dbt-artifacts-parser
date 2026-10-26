"""Compatibility overlays for run_results.json producer differences."""

from typing import List, Optional

from dbt_artifacts_parser.parsers.run_results.run_results_v6 import (
    Result,
    RunResultsV6,
)


class RunResultV6Compat(Result):
    """run-results/v6 result plus fields emitted by dbt v2/Fusion."""

    static_analysis_off_reason: Optional[str] = None


class RunResultsV6Compat(RunResultsV6):
    """run-results/v6 artifact with dbt v2-compatible result rows."""

    results: List[RunResultV6Compat]
