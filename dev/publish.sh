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
set -e
set -x

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"

cd "$MODULE_DIR"

# Arguments
target=${1:?"target is not set"}

# SEE https://flit.readthedocs.io/en/latest/reproducible.html
SOURCE_DATE_EPOCH=$(date +%s)
export SOURCE_DATE_EPOCH

if [[ "$target" == "pypi" ]] ; then
  flit publish --repository "${target}" --pypirc "${MODULE_DIR}/.pypirc" --setup-py
elif [[ "$target" == "testpypi" ]] ; then
  flit publish --repository "${target}" --pypirc "${MODULE_DIR}/.pypirc" --setup-py
else
  echo "No such target ${target}"
  exit 1
fi
