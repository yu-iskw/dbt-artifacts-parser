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
#
import json
import os

import pytest

from dbt_artifacts_parser.parsers.catalog.catalog_v1 import CatalogV1
from dbt_artifacts_parser.parsers.manifest.manifest_v1 import ManifestV1
from dbt_artifacts_parser.parsers.manifest.manifest_v2 import ManifestV2
from dbt_artifacts_parser.parsers.manifest.manifest_v3 import ManifestV3
from dbt_artifacts_parser.parsers.manifest.manifest_v4 import ManifestV4
from dbt_artifacts_parser.parsers.manifest.manifest_v5 import ManifestV5
from dbt_artifacts_parser.parsers.manifest.manifest_v6 import ManifestV6
from dbt_artifacts_parser.parsers.manifest.manifest_v7 import ManifestV7
from dbt_artifacts_parser.parsers.manifest.manifest_v8 import ManifestV8
from dbt_artifacts_parser.parsers.manifest.manifest_v9 import ManifestV9
from dbt_artifacts_parser.parsers.manifest.manifest_v10 import ManifestV10
from dbt_artifacts_parser.parsers.run_results.run_results_v1 import RunResultsV1
from dbt_artifacts_parser.parsers.run_results.run_results_v2 import RunResultsV2
from dbt_artifacts_parser.parsers.run_results.run_results_v3 import RunResultsV3
from dbt_artifacts_parser.parsers.run_results.run_results_v4 import RunResultsV4
from dbt_artifacts_parser.parsers.sources.sources_v1 import SourcesV1
from dbt_artifacts_parser.parsers.sources.sources_v2 import SourcesV2
from dbt_artifacts_parser.parsers.sources.sources_v3 import SourcesV3
from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version, get_model_class
from dbt_artifacts_parser.parsers.version_map import ArtifactTypes
from dbt_artifacts_parser.utils import get_project_root


class TestDbtUtils:
    @pytest.mark.parametrize(
        "version,artifacts",
        [
            (
                "v1",
                {
                    "catalog.json": "https://schemas.getdbt.com/dbt/catalog/v1.json",
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v1.json",
                    "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v1.json",
                },
            ),
            (
                "v2",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v2.json",
                    "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v2.json",
                },
            ),
            (
                "v3",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v3.json",
                    "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v3.json",
                },
            ),
            (
                "v4",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v4.json",
                    "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v4.json",
                },
            ),
            (
                "v5",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v5.json",
                },
            ),
            (
                "v6",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v6.json",
                },
            ),
            (
                "v7",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v7.json",
                },
            ),
            (
                "v8",
                {
                    "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v8.json",
                },
            ),
        ],
    )
    def test_get_dbt_schema_version(self, version, artifacts):
        for file, expected_dbt_schema_version in artifacts.items():
            # Determine the subdirectory based on file type
            if file == "catalog.json":
                subdirectory = "catalog"
            elif file == "manifest.json":
                subdirectory = "manifest"
            elif file == "run_results.json":
                subdirectory = "run_results"
            else:
                subdirectory = version  # fallback, though shouldn't happen

            path = os.path.join(
                get_project_root(),
                "tests",
                "resources",
                subdirectory,
                version,
                "jaffle_shop",
                file,
            )
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                assert dbt_schema_version == expected_dbt_schema_version

    @pytest.mark.parametrize(
        "artifact_type,expected_class",
        [
            # v1
            (ArtifactTypes.CATALOG_V1, CatalogV1),
            (ArtifactTypes.MANIFEST_V1, ManifestV1),
            (ArtifactTypes.RUN_RESULTS_V1, RunResultsV1),
            (ArtifactTypes.SOURCES_V1, SourcesV1),
            # v2
            (ArtifactTypes.MANIFEST_V2, ManifestV2),
            (ArtifactTypes.RUN_RESULTS_V2, RunResultsV2),
            (ArtifactTypes.SOURCES_V2, SourcesV2),
            # v3
            (ArtifactTypes.MANIFEST_V3, ManifestV3),
            (ArtifactTypes.RUN_RESULTS_V3, RunResultsV3),
            (ArtifactTypes.SOURCES_V3, SourcesV3),
            # v4
            (ArtifactTypes.MANIFEST_V4, ManifestV4),
            (ArtifactTypes.RUN_RESULTS_V4, RunResultsV4),
            # v5
            (ArtifactTypes.MANIFEST_V5, ManifestV5),
            # v6
            (ArtifactTypes.MANIFEST_V6, ManifestV6),
            # v7
            (ArtifactTypes.MANIFEST_V7, ManifestV7),
            # v8
            (ArtifactTypes.MANIFEST_V8, ManifestV8),
            # v9
            (ArtifactTypes.MANIFEST_V9, ManifestV9),
            # v10
            (ArtifactTypes.MANIFEST_V10, ManifestV10),
        ],
    )
    def test_get_model_class(self, artifact_type, expected_class):
        cls = get_model_class(artifact_type=artifact_type)
        assert cls is expected_class
