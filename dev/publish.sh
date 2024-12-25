#!/usr/bin/env bash
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
set -Eo pipefail
set -x

SCRIPT_FILE="$(readlink -f "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_FILE")"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"

cd "$MODULE_DIR" || exit

# Arguments
target=${1:?"target is not set"}

# Ensure uv is installed
pip install uv

# Build the package first
uv build

# Publish to the specified target
if [[ "$target" == "pypi" ]]; then
  uv publish
elif [[ "$target" == "testpypi" ]]; then
  uv publish --publish-url "https://test.pypi.org/legacy/"
else
  echo "No such target ${target}"
  exit 1
fi
