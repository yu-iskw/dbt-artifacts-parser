# generated by datamodel-codegen:
#   filename:  sources_v2.json
#   timestamp: 2022-03-01T06:21:38+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Extra

from dbt_artifacts_parser.parsers.base import BaseParserModel


class FreshnessMetadata(BaseParserModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/sources/v2.json'
    dbt_version: Optional[str] = '0.21.0rc1'
    generated_at: Optional[datetime] = '2021-09-24T13:29:14.312598Z'
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = {}


class Status(Enum):
    runtime_error = 'runtime error'


class SourceFreshnessRuntimeError(BaseParserModel):
    class Config:
        extra = Extra.forbid

    unique_id: str
    error: Optional[Optional[Union[str, int]]] = None
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
    class Config:
        extra = Extra.forbid

    count: int
    period: Period


class TimingInfo(BaseParserModel):
    class Config:
        extra = Extra.forbid

    name: str
    started_at: Optional[Optional[datetime]] = None
    completed_at: Optional[Optional[datetime]] = None


class FreshnessThreshold(BaseParserModel):
    class Config:
        extra = Extra.forbid

    warn_after: Optional[Optional[Time]] = None
    error_after: Optional[Optional[Time]] = None
    filter: Optional[Optional[str]] = None


class SourceFreshnessOutput(BaseParserModel):
    class Config:
        extra = Extra.forbid

    unique_id: str
    max_loaded_at: datetime
    snapshotted_at: datetime
    max_loaded_at_time_ago_in_s: float
    status: Status1
    criteria: FreshnessThreshold
    adapter_response: Dict[str, Any]
    timing: List[TimingInfo]
    thread_id: str
    execution_time: float


class SourcesV2(BaseParserModel):
    class Config:
        extra = Extra.forbid

    metadata: FreshnessMetadata
    results: List[Union[SourceFreshnessRuntimeError, SourceFreshnessOutput]]
    elapsed_time: float
