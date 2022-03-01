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


@dataclass
class ArtifactType:
    dbt_schema_version: str
    model_class: Type[BaseParserModel]


class ArtifactTypes(Enum):
    """Dbt artifacts types"""
    # Catalog
    CATALOG_V1 = ArtifactType("https://schemas.getdbt.com/dbt/catalog/v1.json", CatalogV1)
    # Manifest
    MANIFEST_V1 = ArtifactType("https://schemas.getdbt.com/dbt/manifest/v1.json", ManifestV1)
    MANIFEST_V2 = ArtifactType("https://schemas.getdbt.com/dbt/manifest/v2.json", ManifestV2)
    MANIFEST_V3 = ArtifactType("https://schemas.getdbt.com/dbt/manifest/v3.json", ManifestV3)
    MANIFEST_V4 = ArtifactType("https://schemas.getdbt.com/dbt/manifest/v4.json", ManifestV4)
    # RunResults
    RUN_RESULTS_V1 = ArtifactType("https://schemas.getdbt.com/dbt/run-results/v1.json", RunResultsV1)
    RUN_RESULTS_V2 = ArtifactType("https://schemas.getdbt.com/dbt/run-results/v2.json", RunResultsV2)
    RUN_RESULTS_V3 = ArtifactType("https://schemas.getdbt.com/dbt/run-results/v3.json", RunResultsV3)
    RUN_RESULTS_V4 = ArtifactType("https://schemas.getdbt.com/dbt/run-results/v4.json", RunResultsV4)
    # Sources
    SOURCES_V1 = ArtifactType("https://schemas.getdbt.com/dbt/sources/v1.json", SourcesV1)
    SOURCES_V2 = ArtifactType("https://schemas.getdbt.com/dbt/sources/v2.json", SourcesV2)
    SOURCES_V3 = ArtifactType("https://schemas.getdbt.com/dbt/sources/v3.json", SourcesV3)
