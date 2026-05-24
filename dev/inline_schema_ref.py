#!/usr/bin/env python3
"""Inline a top-level JSON Schema $ref while preserving $defs for datamodel-codegen."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def inline_root_ref(schema_path: Path) -> dict:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    ref = schema.get("$ref")
    if not ref or not ref.startswith("#/$defs/"):
        return schema
    def_name = ref.removeprefix("#/$defs/")
    defs = schema.get("$defs", {})
    if def_name not in defs:
        raise SystemExit(f"Missing $defs/{def_name} in {schema_path}")

    root = defs[def_name]
    inlined: dict = {"$defs": defs}
    for key in ("$schema", "$id"):
        if key in schema:
            inlined[key] = schema[key]
    for key in ("type", "title", "description", "properties", "required", "additionalProperties"):
        if key in root:
            inlined[key] = root[key]
    return inlined


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(f"Usage: {sys.argv[0]} <input.json> <output.json>")
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    dest.write_text(json.dumps(inline_root_ref(src), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
