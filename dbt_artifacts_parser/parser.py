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
from typing import Union

from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version

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

from dbt_artifacts_parser.parsers.version_map import ArtifactTypes


#
# catalog
#
def parse_catalog(catalog: dict) -> Union[CatalogV1]:
    """Parse catalog.json

    Args:
        catalog: dict of catalog.json

    Returns:
        Union[CatalogV1]
    """
    dbt_schema_version = get_dbt_schema_version(artifact_json=catalog)
    if dbt_schema_version == ArtifactTypes.CATALOG_V1.value.dbt_schema_version:
        return CatalogV1(**catalog)
    raise ValueError("Not a soft of catalog.json")


def parse_catalog_v1(catalog: dict) -> CatalogV1:
    """Parse catalog.json v1"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=catalog)
    if dbt_schema_version == ArtifactTypes.CATALOG_V1.value.dbt_schema_version:
        return CatalogV1(**catalog)
    raise ValueError("Not a catalog.json v1")


#
# manifest
#
def parse_manifest(
        manifest: dict
) -> Union[ManifestV1, ManifestV2, ManifestV3, ManifestV4]:
    """Parse manifest.json

    Args:
        manifest: A dict of manifest.json

    Returns:
       Union[ManifestV1, ManifestV2, ManifestV3, ManifestV4]
    """
    dbt_schema_version = get_dbt_schema_version(artifact_json=manifest)
    if dbt_schema_version == ArtifactTypes.MANIFEST_V1.value.dbt_schema_version:
        return ManifestV1(**manifest)
    elif dbt_schema_version == ArtifactTypes.MANIFEST_V2.value.dbt_schema_version:
        return ManifestV2(**manifest)
    elif dbt_schema_version == ArtifactTypes.MANIFEST_V3.value.dbt_schema_version:
        return ManifestV3(**manifest)
    elif dbt_schema_version == ArtifactTypes.MANIFEST_V4.value.dbt_schema_version:
        return ManifestV4(**manifest)
    raise ValueError("Not a soft of manifest.json")


def parse_manifest_v1(manifest: dict) -> ManifestV1:
    """Parse manifest.json ver.1"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=manifest)
    if dbt_schema_version == ArtifactTypes.MANIFEST_V1.value.dbt_schema_version:
        return ManifestV1(**manifest)
    raise ValueError("Not a manifest.json v1")


def parse_manifest_v2(manifest: dict) -> ManifestV2:
    """Parse manifest.json ver.2"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=manifest)
    if dbt_schema_version == ArtifactTypes.MANIFEST_V2.value.dbt_schema_version:
        return ManifestV2(**manifest)
    raise ValueError("Not a manifest.json v2")


def parse_manifest_v3(manifest: dict) -> ManifestV3:
    """Parse manifest.json ver.3"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=manifest)
    if dbt_schema_version == ArtifactTypes.MANIFEST_V3.value.dbt_schema_version:
        return ManifestV3(**manifest)
    raise ValueError("Not a manifest.json v3")


def parse_manifest_v4(manifest: dict) -> ManifestV4:
    """Parse manifest.json ver.4"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=manifest)
    if dbt_schema_version == ArtifactTypes.MANIFEST_V4.value.dbt_schema_version:
        return ManifestV4(**manifest)
    raise ValueError("Not a manifest.json v4")


#
# run-results
#
def parse_run_results(
    run_results: dict
) -> Union[RunResultsV1, RunResultsV2, RunResultsV3, RunResultsV4]:
    """Parse run-results.json

    Args:
        run_results: A dict of run-results.json

    Returns:
        Union[RunResultsV1, RunResultsV2, RunResultsV3, RunResultsV4]:
    """
    dbt_schema_version = get_dbt_schema_version(artifact_json=run_results)
    if dbt_schema_version == ArtifactTypes.RUN_RESULTS_V1.value.dbt_schema_version:
        return RunResultsV1(**run_results)
    elif dbt_schema_version == ArtifactTypes.RUN_RESULTS_V2.value.dbt_schema_version:
        return RunResultsV2(**run_results)
    elif dbt_schema_version == ArtifactTypes.RUN_RESULTS_V3.value.dbt_schema_version:
        return RunResultsV3(**run_results)
    elif dbt_schema_version == ArtifactTypes.RUN_RESULTS_V4.value.dbt_schema_version:
        return RunResultsV4(**run_results)
    raise ValueError("Not a soft of manifest.json")


def parse_run_results_v1(run_results: dict) -> RunResultsV1:
    """Parse run-results.json v1"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=run_results)
    if dbt_schema_version == ArtifactTypes.RUN_RESULTS_V1.value.dbt_schema_version:
        return RunResultsV1(**run_results)
    raise ValueError("Not a run-results.json v1")


def parse_run_results_v2(run_results: dict) -> RunResultsV2:
    """Parse run-results.json v2"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=run_results)
    if dbt_schema_version == ArtifactTypes.RUN_RESULTS_V2.value.dbt_schema_version:
        return RunResultsV2(**run_results)
    raise ValueError("Not a run-results.json v2")


def parse_run_results_v3(run_results: dict) -> RunResultsV3:
    """Parse run-results.json v3"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=run_results)
    if dbt_schema_version == ArtifactTypes.RUN_RESULTS_V3.value.dbt_schema_version:
        return RunResultsV3(**run_results)
    raise ValueError("Not a run-results.json v3")


def parse_run_results_v4(run_results: dict) -> RunResultsV4:
    """Parse run-results.json v4"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=run_results)
    if dbt_schema_version == ArtifactTypes.RUN_RESULTS_V4.value.dbt_schema_version:
        return RunResultsV4(**run_results)
    raise ValueError("Not a run-results.json v4")


#
# sources
#
def parse_sources(sources: dict) -> Union[SourcesV1, SourcesV2, SourcesV3]:
    """Parse sources.json

    Args:
        sources: A dict of sources.json

    Returns:
        Union[SourcesV1, SourcesV2, SourcesV3]
    """
    dbt_schema_version = get_dbt_schema_version(artifact_json=sources)
    if dbt_schema_version == ArtifactTypes.SOURCES_V1.value.dbt_schema_version:
        return SourcesV1(**sources)
    elif dbt_schema_version == ArtifactTypes.SOURCES_V2.value.dbt_schema_version:
        return SourcesV2(**sources)
    elif dbt_schema_version == ArtifactTypes.SOURCES_V3.value.dbt_schema_version:
        return SourcesV3(**sources)
    raise ValueError("Not a soft of manifest.json")


def parse_sources_v1(sources: dict) -> SourcesV1:
    """Parse sources.json v1"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=sources)
    if dbt_schema_version == ArtifactTypes.SOURCES_V1.value.dbt_schema_version:
        return SourcesV1(**sources)
    raise ValueError("Not a sources.json v1")


def parse_sources_v2(sources: dict) -> SourcesV2:
    """Parse sources.json v2"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=sources)
    if dbt_schema_version == ArtifactTypes.SOURCES_V2.value.dbt_schema_version:
        return SourcesV2(**sources)
    raise ValueError("Not a sources.json v2")


def parse_sources_v3(sources: dict) -> SourcesV3:
    """Parse sources.json v3"""
    dbt_schema_version = get_dbt_schema_version(artifact_json=sources)
    if dbt_schema_version == ArtifactTypes.SOURCES_V3.value.dbt_schema_version:
        return SourcesV3(**sources)
    raise ValueError("Not a sources.json v3")
