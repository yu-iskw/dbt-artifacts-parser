# Shared artifact type and version lists for dev scripts.
# shellcheck shell=bash
#
# ALL_* versions: every schema vendored in dbt_artifacts_parser/resources/ (codegen + tests).
# DOWNLOAD_* versions: schemas available on dbt-core main (see schemas/dbt/); historical
# versions are kept in-repo only and are not re-fetched on a default refresh.

ARTIFACT_TYPES=(catalog manifest run-results sources)

CATALOG_VERSIONS=(v1)
CATALOG_DOWNLOAD_VERSIONS=(v1)

MANIFEST_VERSIONS=(v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 v11 v12)
MANIFEST_DOWNLOAD_VERSIONS=(v5 v6 v7 v8 v9 v10 v11 v12)

RUN_RESULTS_VERSIONS=(v1 v2 v3 v4 v5 v6)
RUN_RESULTS_DOWNLOAD_VERSIONS=(v4 v5 v6)

SOURCES_VERSIONS=(v1 v2 v3)
SOURCES_DOWNLOAD_VERSIONS=(v3)
