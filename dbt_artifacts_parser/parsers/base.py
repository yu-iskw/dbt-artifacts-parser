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

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import BaseModel, ConfigDict


class BaseParserModel(BaseModel):
    """
    The base parser class for all dbt artifacts.

    We use this class to centralize the model configuration of all dbt artifacts.
    """


class BaseCatalogParserModel(BaseParserModel):
    """
    The base parser model for catalog artifacts.
    """


class BaseManifestParserModel(BaseParserModel):
    """
    The base parser model for manifest artifacts.
    """

    model_config = ConfigDict(
        # Setting the protected namespaces to an empty tuple to suppress Pydantic warnings
        # related to conflicts with the default protected namespaces.
        protected_namespaces=(),
    )


class BaseRunResultsParserModel(BaseParserModel):
    """
    The base parser model for run results artifacts.
    """


class BaseSourcesParserModel(BaseParserModel):
    """
    The base parser model for source artifacts.
    """
