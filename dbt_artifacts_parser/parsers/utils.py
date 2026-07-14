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

import copy
import re
import warnings
from typing import Any, Optional, Sequence, Type, TypeVar, Union

from pydantic import ValidationError

from dbt_artifacts_parser.parsers.base import BaseParserModel
from dbt_artifacts_parser.parsers.version_map import ArtifactTypes

T = TypeVar("T", bound=BaseParserModel)

_ARTIFACT_SLUGS = ("catalog", "manifest", "run-results", "sources")
_MAX_EXTRA_STRIP_RETRIES = 50


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


def extract_artifact_version(schema_version: str, artifact_slug: str) -> Optional[int]:
    """Extract the integer schema version from a dbt schema URL.

    Args:
        schema_version: Value of metadata.dbt_schema_version
        artifact_slug: Artifact family slug (e.g. 'manifest', 'run-results')

    Returns:
        Version number, or None if the URL does not match the artifact family.
    """
    pattern = rf"/{re.escape(artifact_slug)}/v(\d+)\.json$"
    match = re.search(pattern, schema_version)
    if match is None:
        return None
    return int(match.group(1))


def _max_versions_from_artifact_types() -> dict[str, int]:
    """Derive max supported version per slug from ArtifactTypes."""
    maxima: dict[str, int] = {slug: 0 for slug in _ARTIFACT_SLUGS}
    for artifact_type in ArtifactTypes:
        schema_version = artifact_type.value.dbt_schema_version
        for slug in _ARTIFACT_SLUGS:
            version = extract_artifact_version(schema_version, slug)
            if version is not None and version > maxima[slug]:
                maxima[slug] = version
    return maxima


ARTIFACT_MAX_VERSIONS = _max_versions_from_artifact_types()


def warn_fallback_to_latest(requested: str, parsed_as: str) -> None:
    """Warn that an unsupported newer schema was parsed as the latest known version."""
    warnings.warn(
        (
            f"Unsupported artifact schema version {requested!r}; "
            f"falling back to latest supported schema {parsed_as!r}. "
            "This is best-effort; unknown fields may be dropped and "
            "incompatible changes may still fail validation."
        ),
        UserWarning,
        stacklevel=4,
    )


def _delete_at_loc(payload: Any, loc: Sequence[Union[str, int]]) -> bool:
    """Delete the value at a Pydantic error loc.

    Returns True if something was removed.
    """
    if not loc:
        return False
    current = payload
    for part in loc[:-1]:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif (
            isinstance(current, list)
            and isinstance(part, int)
            and 0 <= part < len(current)
        ):
            current = current[part]
        else:
            return False
    last = loc[-1]
    if isinstance(current, dict) and last in current:
        del current[last]
        return True
    if isinstance(current, list) and isinstance(last, int) and 0 <= last < len(current):
        del current[last]
        return True
    return False


def validate_preserving_allowed_extras(model_class: Type[T], artifact_json: dict) -> T:
    """Validate without overriding nested extra config.

    Strips only ``extra_forbidden`` fields and retries so nested ``extra="allow"``
    models (e.g. dbt config) keep schema-allowed custom keys.
    """
    payload = copy.deepcopy(artifact_json)
    for _ in range(_MAX_EXTRA_STRIP_RETRIES):
        try:
            return model_class.model_validate(payload)
        except ValidationError as exc:
            errors = exc.errors()
            forbidden_locs = [
                err["loc"] for err in errors if err.get("type") == "extra_forbidden"
            ]
            if not forbidden_locs or len(forbidden_locs) != len(errors):
                raise
            removed_any = False
            # Delete deepest paths first so parent locs stay valid when stripping lists.
            for loc in sorted(forbidden_locs, key=len, reverse=True):
                if _delete_at_loc(payload, loc):
                    removed_any = True
            if not removed_any:
                raise
    raise RuntimeError(
        f"Exceeded {_MAX_EXTRA_STRIP_RETRIES} retries while stripping "
        f"extra_forbidden fields for {model_class.__name__}"
    )


def try_parse_fallback_to_latest(
    artifact_json: dict,
    schema_version: str,
    artifact_slug: str,
    model_class: Type[T],
) -> Optional[T]:
    """Parse as the latest known model when schema_version is a newer forward version.

    Returns None when fallback does not apply (wrong family or not newer).
    """
    version = extract_artifact_version(schema_version, artifact_slug)
    max_version = ARTIFACT_MAX_VERSIONS[artifact_slug]
    if version is None or version <= max_version:
        return None
    warn_fallback_to_latest(schema_version, f"v{max_version}")
    return validate_preserving_allowed_extras(model_class, artifact_json)


def get_artifact_type_by_id(schema_version: str) -> ArtifactTypes:
    """Get artifact information by schema version

    Args:
        schema_version: dbt schema version

    Returns:
        ArtifactsTypes
    """
    for artifact_type in ArtifactTypes:
        if schema_version == artifact_type.value.dbt_schema_version:
            return artifact_type
    raise ValueError(f"no such schema version: {schema_version}")


def get_model_class(artifact_type: ArtifactTypes) -> Type[BaseParserModel]:
    """Get the model class

    Args:
        artifact_type (ArtifactTypes): artifact type

    Returns:
        the model class
    """
    for artifact_type_ in ArtifactTypes:
        if artifact_type == artifact_type_:
            return artifact_type_.value.model_class
    raise ValueError(f"No such an artifact {artifact_type}")
