#!/bin/bash
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
set -Eeuo pipefail

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
MODULE_DIR="$(dirname "${SCRIPT_DIR}")"

# Arguments (default: project .venv via uv; use --system for legacy system-site installs)
deps="production"
use_venv=true
while (($# > 0)); do
  if [[ "$1" == "--use-venv" ]]; then
    echo "Warning: --use-venv is deprecated (venv is now the default)." >&2
    shift 1
  elif [[ "$1" == "--system" ]]; then
    use_venv=false
    shift 1
  elif [[ "$1" == "--deps" ]]; then
    if [[ "$2" != "production" && "$2" != "development" ]]; then
      echo "Error: deps must be one of 'production' or 'development'"
      exit 1
    fi
    deps="$2"
    shift 2
  else
    echo "Unknown argument: $1"
    exit 1
  fi
done

# Change to the module directory
cd "${MODULE_DIR}"

# Install uv and dependencies
pip install --force-reinstall -r "${MODULE_DIR}/requirements.setup.txt"

if [[ "${use_venv}" == true ]]; then
  # PEP 735 [dependency-groups] + uv.lock; [tool.uv] default-groups includes dev
  if [[ "${deps}" == "production" ]]; then
    uv sync --no-default-groups
  else
    uv sync
  fi
else
  UV_PIP_OPTIONS=("--force-reinstall" "--system")
  if [[ "${deps}" == "production" ]]; then
    uv pip install "${UV_PIP_OPTIONS[@]}" -e "."
  else
    uv pip install "${UV_PIP_OPTIONS[@]}" -e ".[dev]"
  fi
fi
