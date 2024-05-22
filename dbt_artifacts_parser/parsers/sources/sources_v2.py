# generated by datamodel-codegen:
#   filename:  sources_v2.json

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AwareDatetime, ConfigDict

from dbt_artifacts_parser.parsers.base import BaseParserModel


class FreshnessMetadata(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/sources/v2.json'
    dbt_version: Optional[str] = '0.21.0rc1'
    generated_at: Optional[AwareDatetime] = '2021-09-24T13:29:14.312598Z'
    invocation_id: Optional[str] = None
    env: Optional[Dict[str, str]] = {}


class Status(Enum):
    runtime_error = 'runtime error'


class SourceFreshnessRuntimeError(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    unique_id: str
    error: Optional[Union[str, int]] = None
    status: Status


class Status1(Enum):
    pass_ = 'pass'
    warn = 'warn'
    error = 'error'
    runtime_error = 'runtime error'


class Period(Enum):
    minute = 'minute'
    hour = 'hour'
    day = 'day'


class Time(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    count: int
    period: Period


class TimingInfo(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: str
    started_at: Optional[AwareDatetime] = None
    completed_at: Optional[AwareDatetime] = None


class FreshnessThreshold(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    warn_after: Optional[Time] = None
    error_after: Optional[Time] = None
    filter: Optional[str] = None


class SourceFreshnessOutput(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    unique_id: str
    max_loaded_at: AwareDatetime
    snapshotted_at: AwareDatetime
    max_loaded_at_time_ago_in_s: float
    status: Status1
    criteria: FreshnessThreshold
    adapter_response: Dict[str, Any]
    timing: List[TimingInfo]
    thread_id: str
    execution_time: float


class SourcesV2(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    metadata: FreshnessMetadata
    results: List[Union[SourceFreshnessRuntimeError, SourceFreshnessOutput]]
    elapsed_time: float
