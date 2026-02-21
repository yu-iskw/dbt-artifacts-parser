#!/usr/bin/env bash
set -e

cd "${CLAUDE_PROJECT_DIR:-.}"

output=$(pre-commit run --all-files 2>&1)
status=$?
if [ "$status" -ne 0 ]; then
  echo "$output" >&2
  exit 2
fi
exit 0
