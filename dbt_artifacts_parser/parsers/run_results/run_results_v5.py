# generated by datamodel-codegen:
#   filename:  run-results_v5.json

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Extra

from dbt_artifacts_parser.parsers.base import BaseParserModel


class BaseArtifactMetadata(BaseParserModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: str
    dbt_version: Optional[str] = '1.7.0b1'
    generated_at: Optional[str] = None
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = None


class StatusEnum(Enum):
    success = 'success'
    error = 'error'
    skipped = 'skipped'


class StatusEnum1(Enum):
    pass_ = 'pass'
    error = 'error'
    fail = 'fail'
    warn = 'warn'
    skipped = 'skipped'


class StatusEnum2(Enum):
    pass_ = 'pass'
    warn = 'warn'
    error = 'error'
    runtime_error = 'runtime error'


class TimingInfo(BaseParserModel):
    class Config:
        extra = Extra.forbid

    name: str
    started_at: Optional[Optional[str]] = None
    completed_at: Optional[Optional[str]] = None


class RunResultOutput(BaseParserModel):
    class Config:
        extra = Extra.forbid

    status: Union[StatusEnum, StatusEnum1, StatusEnum2]
    timing: List[TimingInfo]
    thread_id: str
    execution_time: float
    adapter_response: Dict[str, Any]
    message: Optional[str]
    failures: Optional[int]
    unique_id: str
    compiled: Optional[bool]
    compiled_code: Optional[str]
    relation_name: Optional[str]


class RunResultsArtifact(BaseParserModel):
    class Config:
        extra = Extra.forbid

    metadata: BaseArtifactMetadata
    results: List[RunResultOutput]
    elapsed_time: float
    args: Optional[Dict[str, Any]] = None


class RunResultsV5(BaseParserModel):
    __root__: RunResultsArtifact
