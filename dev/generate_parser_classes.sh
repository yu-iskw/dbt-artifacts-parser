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
target_python_version="3.10"
output_model_type="pydantic_v2.BaseModel"

# All artifact types for "generate all"
ARTIFACT_TYPES=(catalog manifest run-results sources)

# Version list per artifact type (bash arrays). Used indirectly via nameref in main (default_versions_array_name).
# shellcheck disable=SC2034
CATALOG_VERSIONS=(v1)
# shellcheck disable=SC2034
MANIFEST_VERSIONS=(v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 v11 v12)
# shellcheck disable=SC2034
RUN_RESULTS_VERSIONS=(v1 v2 v3 v4 v5 v6)
# shellcheck disable=SC2034
SOURCES_VERSIONS=(v1 v2 v3)

usage() {
	echo "Usage: $0 [artifact_type] [version ...]"
	echo "  Generate Pydantic parser classes from dbt artifact JSON schemas."
	echo "  With no arguments, generates all artifact types and versions."
	echo ""
	echo "  artifact_type  one of: catalog, manifest, run-results, sources"
	echo "  version        optional list of versions (e.g. v1 v7). If omitted, all versions for the type are generated."
	exit "$1"
}

# Sets resource_dir, parser_dir, file_stem, output_file_stem, class_prefix, default_versions_array_name for the given artifact type.
# Exits with usage if type is invalid.
get_artifact_metadata() {
	local type="$1"
	case "${type}" in
	catalog)
		resource_dir="catalog"
		parser_dir="catalog"
		file_stem="catalog"
		output_file_stem="catalog"
		class_prefix="Catalog"
		default_versions_array_name="CATALOG_VERSIONS"
		;;
	manifest)
		resource_dir="manifest"
		parser_dir="manifest"
		file_stem="manifest"
		output_file_stem="manifest"
		class_prefix="Manifest"
		default_versions_array_name="MANIFEST_VERSIONS"
		;;
	run-results)
		resource_dir="run-results"
		parser_dir="run_results"
		file_stem="run-results"
		output_file_stem="run_results"
		class_prefix="RunResults"
		default_versions_array_name="RUN_RESULTS_VERSIONS"
		;;
	sources)
		resource_dir="sources"
		parser_dir="sources"
		file_stem="sources"
		output_file_stem="sources"
		class_prefix="Sources"
		default_versions_array_name="SOURCES_VERSIONS"
		;;
	*)
		echo "Invalid artifact type: ${type}" >&2
		usage 1
		;;
	esac
}

# Generate parser for one (artifact_type, version) pair.
run_codegen() {
	local artifact_type="$1"
	local ver="$2"
	get_artifact_metadata "${artifact_type}"
	upper_ver=${ver^v}
	input="${MODULE_ROOT}/dbt_artifacts_parser/resources/${resource_dir}/${file_stem}_${ver}.json"
	destination="${MODULE_ROOT}/dbt_artifacts_parser/parsers/${parser_dir}/${output_file_stem}_${ver}.py"
	echo "Generate ${destination}"
	datamodel-codegen --input-file-type jsonschema \
		--target-python-version "${target_python_version}" \
		--output-model-type "${output_model_type}" \
		--disable-timestamp \
		--base-class "${base_class}" \
		--class-name "${class_prefix}${upper_ver}" \
		--input "${input}" \
		--output "${destination}"
}

# --- Main ---
if [[ $1 == "-h" || $1 == "--help" ]]; then
	usage 0
fi

if [[ $# -eq 0 ]]; then
	# Generate all artifact types and versions (backward-compatible behavior)
	for artifact_type in "${ARTIFACT_TYPES[@]}"; do
		get_artifact_metadata "${artifact_type}"
		declare -n vers="${default_versions_array_name}"
		for ver in "${vers[@]}"; do
			run_codegen "${artifact_type}" "${ver}"
		done
	done
else
	artifact_type="$1"
	shift
	get_artifact_metadata "${artifact_type}"
	if [[ $# -eq 0 ]]; then
		declare -n vers="${default_versions_array_name}"
		for ver in "${vers[@]}"; do
			run_codegen "${artifact_type}" "${ver}"
		done
	else
		versions=("$@")
		for ver in "${versions[@]}"; do
			run_codegen "${artifact_type}" "${ver}"
		done
	fi
fi
