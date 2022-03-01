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
from typing import Type
from enum import Enum
from dataclasses import dataclass

from dbt_artifacts_parser.parsers.base import BaseParserModel

from dbt_artifacts_parser.parsers.catalog.catalog_v1 import CatalogV1

from dbt_artifacts_parser.parsers.manifest.manifest_v1 import ManifestV1
from dbt_artifacts_parser.parsers.manifest.manifest_v2 import ManifestV2
from dbt_artifacts_parser.parsers.manifest.manifest_v3 import ManifestV3
from dbt_artifacts_parser.parsers.manifest.manifest_v4 import ManifestV4

from dbt_artifacts_parser.parsers.run_results.run_results_v1 import RunResultsV1
from dbt_artifacts_parser.parsers.run_results.run_results_v2 import RunResultsV2
from dbt_artifacts_parser.parsers.run_results.run_results_v3 import RunResultsV3
from dbt_artifacts_parser.parsers.run_results.run_results_v4 import RunResultsV4

from dbt_artifacts_parser.parsers.sources.sources_v1 import SourcesV1
from dbt_artifacts_parser.parsers.sources.sources_v2 import SourcesV2
from dbt_artifacts_parser.parsers.sources.sources_v3 import SourcesV3


class DestinationTables(Enum):
    """Destination tables"""
    # V1
    CATALOG_V1 = "catalog_v1"
    MANIFEST_V1 = "manifest_v1"
    RUN_RESULTS_V1 = "run_results_v1"
    SOURCES_V1 = "sources_v1"
    # V2
    MANIFEST_V2 = "manifest_v2"
    RUN_RESULTS_V2 = "run_results_v2"
    SOURCES_V2 = "sources_v2"
    # V3
    MANIFEST_V3 = "manifest_v3"
    RUN_RESULTS_V3 = "run_results_v3"
    SOURCES_V3 = "sources_v3"
    # V4
    MANIFEST_V4 = "manifest_v4"
    RUN_RESULTS_V4 = "run_results_v4"


class ArtifactsTypes(Enum):
    """Dbt artifacts types"""
    # V1
    CATALOG_V1 = "CatalogV1"
    MANIFEST_V1 = "ManifestV1"
    RUN_RESULTS_V1 = "RunResultsV1"
    SOURCES_V1 = "SourcesV1"
    # V2
    MANIFEST_V2 = "ManifestV2"
    RUN_RESULTS_V2 = "RunResultsV2"
    SOURCES_V2 = "SourcesV2"
    # V3
    MANIFEST_V3 = "ManifestV3"
    RUN_RESULTS_V3 = "RunResultsV3"
    SOURCES_V3 = "SourcesV3"
    # V4
    MANIFEST_V4 = "ManifestV4"
    RUN_RESULTS_V4 = "RunResultsV4"


@dataclass
class ArtifactInfo:
    dbt_schema_version: str
    artifact_type: ArtifactsTypes
    destination_table: DestinationTables
    model_class: Type[BaseParserModel]


ARTIFACT_INFO = {
    # V1
    "CATALOG_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/catalog/v1.json",
                               ArtifactsTypes.CATALOG_V1, DestinationTables.CATALOG_V1, CatalogV1),
    "MANIFEST_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v1.json",
                                ArtifactsTypes.MANIFEST_V1, DestinationTables.MANIFEST_V1, ManifestV1),
    "RUN_RESULTS_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v1.json",
                                   ArtifactsTypes.RUN_RESULTS_V1, DestinationTables.RUN_RESULTS_V1, RunResultsV1),
    "SOURCES_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v1.json",
                               ArtifactsTypes.SOURCES_V1, DestinationTables.SOURCES_V1, SourcesV1),
    # V2
    "MANIFEST_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v2.json",
                                ArtifactsTypes.MANIFEST_V2, DestinationTables.MANIFEST_V2, ManifestV2),
    "RUN_RESULTS_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v2.json",
                                   ArtifactsTypes.RUN_RESULTS_V2, DestinationTables.RUN_RESULTS_V2, RunResultsV2),
    "SOURCES_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v2.json",
                               ArtifactsTypes.SOURCES_V2, DestinationTables.SOURCES_V2, SourcesV2),
    # V3
    "MANIFEST_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v3.json",
                                ArtifactsTypes.MANIFEST_V3, DestinationTables.MANIFEST_V3, ManifestV3),
    "RUN_RESULTS_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v3.json",
                                   ArtifactsTypes.RUN_RESULTS_V3, DestinationTables.RUN_RESULTS_V3, RunResultsV3),
    "SOURCES_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v3.json",
                               ArtifactsTypes.SOURCES_V3, DestinationTables.SOURCES_V3, SourcesV3),
    # V4
    "MANIFEST_V4": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v4.json",
                                ArtifactsTypes.MANIFEST_V4, DestinationTables.MANIFEST_V4, ManifestV4),
    "RUN_RESULTS_V4": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v4.json",
                                   ArtifactsTypes.RUN_RESULTS_V4, DestinationTables.RUN_RESULTS_V4, RunResultsV4),
}
