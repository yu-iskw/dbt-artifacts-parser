#!/bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -e

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
MODULE_ROOT="$(dirname "${SCRIPT_DIR}")"

# Base class
base_class="dbt_artifacts_parser.parsers.base.BaseParserModel"
target_python_version="3.9"
output_model_type="pydantic_v2.BaseModel"

#
# catalog
#
catalog_versions=("v1")
for ver in "${catalog_versions[@]}"
do
  # Convert `v1` to `V1`
  upper_ver=${ver^v}
  destination="${MODULE_ROOT}/dbt_artifacts_parser/parsers/catalog/catalog_${ver}.py"
  echo "Generate ${destination}"
  datamodel-codegen  --input-file-type jsonschema \
    --target-python-version "${target_python_version}" \
    --output-model-type "${output_model_type}" \
    --disable-timestamp \
    --base-class "${base_class}" \
    --class-name "Catalog${upper_ver}" \
    --input "${MODULE_ROOT}/dbt_artifacts_parser/resources/catalog/catalog_${ver}.json" \
    --output "${destination}"
done

#
# manifest
#
manifest_versions=("v1" "v2" "v3" "v4" "v5" "v6" "v7" "v8" "v9" "v10" "v11" "v12")
for ver in "${manifest_versions[@]}"
do
  # Convert `v1` to `V1`
  upper_ver=${ver^v}
  destination="${MODULE_ROOT}/dbt_artifacts_parser/parsers/manifest/manifest_${ver}.py"
  echo "Generate ${destination}"
  datamodel-codegen  --input-file-type jsonschema \
    --target-python-version "${target_python_version}" \
    --output-model-type "${output_model_type}" \
    --disable-timestamp \
    --base-class "${base_class}" \
    --class-name "Manifest${upper_ver}" \
    --input "${MODULE_ROOT}/dbt_artifacts_parser/resources/manifest/manifest_${ver}.json" \
    --output "${destination}"
done

#
# run-results
#
run_results_versions=("v1" "v2" "v3" "v4" "v5" "v6")
for ver in "${run_results_versions[@]}"
do
  # Convert `v1` to `V1`
  upper_ver=${ver^v}
  destination="${MODULE_ROOT}/dbt_artifacts_parser/parsers/run_results/run_results_${ver}.py"
  echo "Generate ${destination}"
  datamodel-codegen  --input-file-type jsonschema \
    --target-python-version "${target_python_version}" \
    --output-model-type "${output_model_type}" \
    --disable-timestamp \
    --base-class "${base_class}" \
    --class-name "RunResults${upper_ver}" \
    --input "${MODULE_ROOT}/dbt_artifacts_parser/resources/run-results/run-results_${ver}.json" \
    --output "${destination}"
done

#
# sources
#
sources_versions=("v1" "v2" "v3")
for ver in "${sources_versions[@]}"
do
  # Convert `v1` to `V1`
  upper_ver=${ver^v}
  destination="${MODULE_ROOT}/dbt_artifacts_parser/parsers/sources/sources_${ver}.py"
  echo "Generate ${destination}"
  datamodel-codegen  --input-file-type jsonschema \
    --target-python-version "${target_python_version}" \
    --output-model-type "${output_model_type}" \
    --disable-timestamp \
    --base-class "${base_class}" \
    --class-name "Sources${upper_ver}" \
    --input "${MODULE_ROOT}/dbt_artifacts_parser/resources/sources/sources_${ver}.json" \
    --output "${destination}"
done
