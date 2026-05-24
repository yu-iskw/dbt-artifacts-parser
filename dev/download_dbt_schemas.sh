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
BASE_URL="https://raw.githubusercontent.com/dbt-labs/dbt-core"
REF="main"
RESOURCES_DIR="${MODULE_ROOT}/dbt_artifacts_parser/resources"

# shellcheck disable=SC1091
source "${SCRIPT_DIR}/_artifact_versions.sh"

usage() {
	echo "Usage: $0 [--ref REF] [artifact_type] [version ...]"
	echo "  Download dbt artifact JSON schemas from dbt-labs/dbt-core into this project's resources."
	echo "  With no arguments (after --ref), downloads upstream-available schemas for all artifact types."
	echo "  Historical versions vendored in-repo are skipped (not on dbt-core main)."
	echo ""
	echo "  --ref REF       Git ref: branch, tag, or commit (default: main)"
	echo "  artifact_type   one of: catalog, manifest, run-results, sources"
	echo "  version         optional list of versions (e.g. v1 v7). If omitted, upstream versions for the type are downloaded."
	exit "$1"
}

# Sets resource_dir, file_stem, default_versions_array_name for the given artifact type.
# Exits with usage if type is invalid.
get_artifact_metadata() {
	local type="$1"
	case "${type}" in
	catalog)
		resource_dir="catalog"
		file_stem="catalog"
		default_versions_array_name="CATALOG_DOWNLOAD_VERSIONS"
		;;
	manifest)
		resource_dir="manifest"
		file_stem="manifest"
		default_versions_array_name="MANIFEST_DOWNLOAD_VERSIONS"
		;;
	run-results)
		resource_dir="run-results"
		file_stem="run-results"
		default_versions_array_name="RUN_RESULTS_DOWNLOAD_VERSIONS"
		;;
	sources)
		resource_dir="sources"
		file_stem="sources"
		default_versions_array_name="SOURCES_DOWNLOAD_VERSIONS"
		;;
	*)
		echo "Invalid artifact type: ${type}" >&2
		usage 1
		;;
	esac
}

download_one() {
	local artifact_type="$1"
	local ver="$2"
	get_artifact_metadata "${artifact_type}"
	url="${BASE_URL}/${REF}/schemas/dbt/${resource_dir}/${ver}.json"
	dest="${RESOURCES_DIR}/${resource_dir}/${file_stem}_${ver}.json"
	mkdir -p "${RESOURCES_DIR}/${resource_dir}"
	curl -f -S -L -o "${dest}" "${url}"
	echo "Downloaded ${dest}"
}

# --- Argument parsing ---
while [[ $# -gt 0 ]]; do
	case "$1" in
	--ref)
		if [[ -z "${2:-}" ]]; then
			echo "Missing value for --ref" >&2
			usage 1
		fi
		REF="$2"
		shift 2
		;;
	-h|--help)
		usage 0
		;;
	*)
		break
		;;
	esac
done

# --- Main ---
if [[ $# -eq 0 ]]; then
	for artifact_type in "${ARTIFACT_TYPES[@]}"; do
		get_artifact_metadata "${artifact_type}"
		declare -n vers="${default_versions_array_name}"
		for ver in "${vers[@]}"; do
			download_one "${artifact_type}" "${ver}"
		done
	done
else
	artifact_type="$1"
	shift
	get_artifact_metadata "${artifact_type}"
	if [[ $# -eq 0 ]]; then
		declare -n vers="${default_versions_array_name}"
		for ver in "${vers[@]}"; do
			download_one "${artifact_type}" "${ver}"
		done
	else
		versions=("$@")
		for ver in "${versions[@]}"; do
			download_one "${artifact_type}" "${ver}"
		done
	fi
fi
