from typing import Dict, List, Optional

from pydantic import ConfigDict
from dbt_artifacts_parser.parsers.base import BaseParserModel

class NodeRelation(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    alias: str
    schema_name: str
    database: str
    relation_name: str


class Measure(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: str
    filter: Optional[str]
    alias: Optional[str]


class TypeParams(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    measure: Measure
    numerator: Optional[str] = ""
    denominator: Optional[str] = ""
    expr: Optional[str] = ""
    window: Optional[str] = ""
    grain_to_date: Optional[str] = ""
    metrics: List[str]
    input_measures: List[str]


class Metric(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: str
    description: str
    type: str
    type_params: TypeParams
    filter: Optional[str] = ""
    metadata: Optional[Dict[str, str]] = {}


class TimeSpineTableConfiguration(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    location: str
    column_name: str
    grain: str


class ProjectConfiguration(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    time_spine_table_configurations: List[TimeSpineTableConfiguration]
    metadata: Optional[Dict[str, str]] = {}
    dsi_package_version: Dict[str, str]


class SavedQueryExportConfig(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    export_as: str
    schema_name: Optional[str] = ""
    alias: Optional[str] = ""


class SavedQueryExport(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: str
    config: SavedQueryExportConfig


class SavedQueryParams(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    metrics: List[str]
    group_by: List[str]
    where: Optional[List[str]] = []


class SavedQuery(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: str
    query_params: SavedQueryParams
    description: str
    metadata: Optional[Dict[str, str]] = {}
    label: Optional[str] = ""
    exports: List[SavedQueryExport]


class SemanticModel(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: str
    defaults: Optional[Dict[str, str]] = {}
    description: str
    node_relation: NodeRelation
    entities: List[str]
    measures: List[str]
    dimensions: List[str]
    metrics: List[Metric]
    project_configuration: ProjectConfiguration
    saved_queries: List[SavedQuery]


class SemanticManifestV1(BaseParserModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    semantic_models: List[SemanticModel]
