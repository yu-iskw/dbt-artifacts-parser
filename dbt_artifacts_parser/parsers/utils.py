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

from typing import Optional, Type

from dbt_artifacts_parser.parsers.base import BaseParserModel
from dbt_artifacts_parser.parsers.version_map import ARTIFACT_INFO, ArtifactsTypes


def get_dbt_schema_version(artifact_json: dict) -> str:
    """Get the dbt schema version from the dbt artifact JSON

    Args:
        artifact_json (dict): dbt artifacts JSON

    Returns:
        (str): dbt schema version from 'metadata.dbt_schema_version'
    """
    if "metadata" not in artifact_json:
        raise ValueError("'metadata' doesn't exist.")
    if "dbt_schema_version" not in artifact_json["metadata"]:
        raise ValueError("'metadata.dbt_schema_version' doesnt' exist.")
    return artifact_json["metadata"]["dbt_schema_version"]


def get_artifact_type_by_id(dbt_schema_version: str) -> Optional["ArtifactsTypes"]:
    """Get one of the enumeration values by the schema ID

    Args:
        dbt_schema_version (str): The schema ID

    Returns:
        one of ArtifactsTypeV1 values
    """
    for _, artifact_info in ARTIFACT_INFO.items():
        if dbt_schema_version == artifact_info.dbt_schema_version:
            return artifact_info.artifact_type
    return None


def get_model_class(artifact_type: ArtifactsTypes) -> Type[BaseParserModel]:
    """Get the model class

    Args:
        artifact_type (ArtifactsTypes): artifact type

    Returns:
        the model class
    """
    # v1
    for _, artifact_info in ARTIFACT_INFO.items():
        if artifact_type == artifact_info.artifact_type:
            return artifact_info.model_class
    raise ValueError(f"No such an artifact {artifact_type}")
