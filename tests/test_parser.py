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
import os
import yaml

import pytest

from dbt_artifacts_parser import parser
from dbt_artifacts_parser.utils import get_project_root


@pytest.mark.parametrize("version", ["v1"])
class TestCatalogParser:
    def test_parse_catalog(self, version):
        path = os.path.join(
            get_project_root(),
            "tests",
            "resources",
            version,
            "jaffle_shop",
            "catalog.json",
        )
        with open(path, "r", encoding="utf-8") as fp:
            catalog_dict = yaml.safe_load(fp)
            catalog_obj = parser.parse_catalog(catalog_dict)
        assert (
            catalog_obj.metadata.dbt_schema_version
            == f"https://schemas.getdbt.com/dbt/catalog/{version}.json"
        )

    def test_parse_catalog_specific(self, version):
        path = os.path.join(
            get_project_root(),
            "tests",
            "resources",
            version,
            "jaffle_shop",
            "catalog.json",
        )
        with open(path, "r", encoding="utf-8") as fp:
            catalog_dict = yaml.safe_load(fp)
            catalog_obj = getattr(parser, f"parse_catalog_{version}")(catalog_dict)
        assert (
            catalog_obj.metadata.dbt_schema_version
            == f"https://schemas.getdbt.com/dbt/catalog/{version}.json"
        )


@pytest.mark.parametrize("version", ["v1", "v2", "v3", "v4", "v5", "v6", "v7"])
class TestManifestParser:
    def test_parse_manifest(self, version):
        path = os.path.join(
            get_project_root(),
            "tests",
            "resources",
            version,
            "jaffle_shop",
            "manifest.json",
        )
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parser.parse_manifest(manifest_dict)
        assert (
            manifest_obj.metadata.dbt_schema_version
            == f"https://schemas.getdbt.com/dbt/manifest/{version}.json"
        )

    def test_parse_manifest_specific(self, version):
        path = os.path.join(
            get_project_root(),
            "tests",
            "resources",
            version,
            "jaffle_shop",
            "manifest.json",
        )
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = getattr(parser, f"parse_manifest_{version}")(manifest_dict)
        assert (
            manifest_obj.metadata.dbt_schema_version
            == f"https://schemas.getdbt.com/dbt/manifest/{version}.json"
        )


@pytest.mark.parametrize("version", ["v1", "v2", "v3", "v4"])
class TestRunResultsParser:
    def test_parse_run_results(self, version):
        path = os.path.join(
            get_project_root(),
            "tests",
            "resources",
            version,
            "jaffle_shop",
            "run_results.json",
        )
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parser.parse_run_results(manifest_dict)
        assert (
            manifest_obj.metadata.dbt_schema_version
            == f"https://schemas.getdbt.com/dbt/run-results/{version}.json"
        )

    def test_parse_run_results_specific(self, version):
        path = os.path.join(
            get_project_root(),
            "tests",
            "resources",
            version,
            "jaffle_shop",
            "run_results.json",
        )
        with open(path, "r", encoding="utf-8") as fp:
            run_results_dict = yaml.safe_load(fp)
            run_results_obj = getattr(parser, f"parse_run_results_{version}")(
                run_results_dict
            )
        assert (
            run_results_obj.metadata.dbt_schema_version
            == f"https://schemas.getdbt.com/dbt/run-results/{version}.json"
        )


# TODO add fixtures of sources.json
# @pytest.mark.parametrize("version", ["v1", "v2", "v3"])
# class TestSourcesParser:
#     def test_parse_sources(self, version):
#         path = os.path.join(
#             get_project_root(),
#             "tests",
#             "resources",
#             version,
#             "jaffle_shop",
#             "sources.json",
#         )
#         with open(path, "r", encoding="utf-8") as fp:
#             sources_dict = yaml.safe_load(fp)
#             sources_obj = parser.parse_sources(sources_dict)
#         assert (
#             sources_obj.metadata.dbt_schema_version
#             == f"https://schemas.getdbt.com/dbt/sources/{version}.json"
#         )

#     def test_parse_sources_specific(self, version):
#         path = os.path.join(
#             get_project_root(),
#             "tests",
#             "resources",
#             version,
#             "jaffle_shop",
#             "sources.json",
#         )
#         with open(path, "r", encoding="utf-8") as fp:
#             sources_dict = yaml.safe_load(fp)
#             sources_obj = getattr(parser, f"parse_sources_{version}")(sources_dict)
#         assert (
#             sources_obj.metadata.dbt_schema_version
#             == f"https://schemas.getdbt.com/dbt/sources/{version}.json"
#         )
