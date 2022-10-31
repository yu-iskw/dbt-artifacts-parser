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
import unittest
import os
import yaml

from dbt_artifacts_parser.utils import get_project_root

from dbt_artifacts_parser.parser import (
    parse_catalog, parse_catalog_v1, parse_manifest, parse_manifest_v1,
    parse_manifest_v2, parse_manifest_v3, parse_manifest_v4, parse_manifest_v7, parse_run_results,
    parse_run_results_v1, parse_run_results_v2, parse_run_results_v3,
    parse_run_results_v4, parse_manifest_v5, parse_manifest_v6)


class TestCatalogParser(unittest.TestCase):

    def test_parse_catalog(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v1",
                            "jaffle_shop", "catalog.json")
        with open(path, "r", encoding="utf-8") as fp:
            catalog_dict = yaml.safe_load(fp)
            catalog_obj = parse_catalog(catalog_dict)
        self.assertEqual(catalog_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/catalog/v1.json")

    def test_parse_catalog_v1(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v1",
                            "jaffle_shop", "catalog.json")
        with open(path, "r", encoding="utf-8") as fp:
            catalog_dict = yaml.safe_load(fp)
            catalog_obj = parse_catalog_v1(catalog_dict)
        self.assertEqual(catalog_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/catalog/v1.json")


class TestManifestParser(unittest.TestCase):

    def test_parse_manifest(self):
        versions = ["v1", "v2", "v3", "v4", "v5", "v6", "v7"]
        for version in versions:
            path = os.path.join(get_project_root(), "tests", "resources",
                                version, "jaffle_shop", "manifest.json")
            with open(path, "r", encoding="utf-8") as fp:
                manifest_dict = yaml.safe_load(fp)
                manifest_obj = parse_manifest(manifest_dict)
            self.assertEqual(
                manifest_obj.metadata.dbt_schema_version,
                f"https://schemas.getdbt.com/dbt/manifest/{version}.json")

    def test_parse_manifest_v1(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v1",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v1(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v1.json")

    def test_parse_manifest_v2(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v2",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v2(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v2.json")

    def test_parse_manifest_v3(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v3",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v3(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v3.json")

    def test_parse_manifest_v4(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v4",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v4(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v4.json")

    def test_parse_manifest_v5(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v5",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v5(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v5.json")

    def test_parse_manifest_v6(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v6",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v6(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v6.json")

    def test_parse_manifest_v7(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v7",
                            "jaffle_shop", "manifest.json")
        with open(path, "r", encoding="utf-8") as fp:
            manifest_dict = yaml.safe_load(fp)
            manifest_obj = parse_manifest_v7(manifest_dict)
        self.assertEqual(manifest_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/manifest/v7.json")


class TestRunResultsParser(unittest.TestCase):

    def test_parse_run_results(self):
        versions = ["v1", "v2", "v3", "v4"]
        for version in versions:
            path = os.path.join(get_project_root(), "tests", "resources",
                                version, "jaffle_shop", "run_results.json")
            with open(path, "r", encoding="utf-8") as fp:
                manifest_dict = yaml.safe_load(fp)
                manifest_obj = parse_run_results(manifest_dict)
            self.assertEqual(
                manifest_obj.metadata.dbt_schema_version,
                f"https://schemas.getdbt.com/dbt/run-results/{version}.json")

    def test_parse_run_results_v1(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v1",
                            "jaffle_shop", "run_results.json")
        with open(path, "r", encoding="utf-8") as fp:
            run_results_dict = yaml.safe_load(fp)
            run_results_obj = parse_run_results_v1(run_results_dict)
        self.assertEqual(run_results_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/run-results/v1.json")

    def test_parse_run_results_v2(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v2",
                            "jaffle_shop", "run_results.json")
        with open(path, "r", encoding="utf-8") as fp:
            run_results_dict = yaml.safe_load(fp)
            run_results_obj = parse_run_results_v2(run_results_dict)
        self.assertEqual(run_results_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/run-results/v2.json")

    def test_parse_run_results_v3(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v3",
                            "jaffle_shop", "run_results.json")
        with open(path, "r", encoding="utf-8") as fp:
            run_results_dict = yaml.safe_load(fp)
            run_results_obj = parse_run_results_v3(run_results_dict)
        self.assertEqual(run_results_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/run-results/v3.json")

    def test_parse_run_results_v4(self):
        path = os.path.join(get_project_root(), "tests", "resources", "v4",
                            "jaffle_shop", "run_results.json")
        with open(path, "r", encoding="utf-8") as fp:
            run_results_dict = yaml.safe_load(fp)
            run_results_obj = parse_run_results_v4(run_results_dict)
        self.assertEqual(run_results_obj.metadata.dbt_schema_version,
                         "https://schemas.getdbt.com/dbt/run-results/v4.json")


# TODO add fixtures of sources.json
# class TestSourcesParser(unittest.TestCase):
#
#     def test_parse_sources(self):
#         versions = ["v1", "v2", "v3", "v4"]
#         for version in versions:
#             path = os.path.join(get_project_root(), "tests", "resources", version, "jaffle_shop", "sources.json")
#             with open(path, "r", encoding="utf-8") as fp:
#                 manifest_dict = yaml.safe_load(fp)
#                 manifest_obj = parse_sources(manifest_dict)
#             self.assertEqual(manifest_obj.metadata.dbt_schema_version,
#                              f"https://schemas.getdbt.com/dbt/manifest/{version}.json")
#
#     def test_parse_sources_v1(self):
#         path = os.path.join(get_project_root(), "tests", "resources", "v1", "jaffle_shop", "sources.json")
#         with open(path, "r", encoding="utf-8") as fp:
#             sources_dict = yaml.safe_load(fp)
#             sources_obj = parse_sources_v1(sources_dict)
#         self.assertEqual(sources_obj.metadata.dbt_schema_version,
#                          "https://schemas.getdbt.com/dbt/sources/v1.json")
#
#     def test_parse_sources_v2(self):
#         path = os.path.join(get_project_root(), "tests", "resources", "v2", "jaffle_shop", "sources.json")
#         with open(path, "r", encoding="utf-8") as fp:
#             sources_dict = yaml.safe_load(fp)
#             sources_obj = parse_sources_v2(sources_dict)
#         self.assertEqual(sources_obj.metadata.dbt_schema_version,
#                          "https://schemas.getdbt.com/dbt/sources/v2.json")
#
#     def test_parse_sources_v3(self):
#         path = os.path.join(get_project_root(), "tests", "resources", "v3", "jaffle_shop", "sources.json")
#         with open(path, "r", encoding="utf-8") as fp:
#             sources_dict = yaml.safe_load(fp)
#             sources_obj = parse_sources_v3(sources_dict)
#         self.assertEqual(sources_obj.metadata.dbt_schema_version,
#                          "https://schemas.getdbt.com/dbt/sources/v3.json")
