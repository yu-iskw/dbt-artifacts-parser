[![Test python](https://github.com/yu-iskw/dbt-artifacts-parser/actions/workflows/test.yml/badge.svg)](https://github.com/yu-iskw/dbt-artifacts-parser/actions/workflows/test.yml)
<a href="https://pypi.org/project/dbt-artifacts-parser" target="_blank">
<img src="https://img.shields.io/pypi/v/dbt-artifacts-parser?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/dbt-artifacts-parser" target="_blank">
<img src="https://img.shields.io/pypi/pyversions/dbt-artifacts-parser.svg?color=%2334D058" alt="Supported Python versions">
</a>


# dbt-artifacts-parser
This is a dbt artifacts parse in python.
It enables us to deal with `catalog.json`, `manifest.json`, `run-results.json` and `sources.json` as python objects.

## Installation

```bash
pip install -U dbt-artifacts-parser
```

## Python classes
Those are the classes to parse dbt artifacts.

### Catalog
- [CatalogV1](dbt_artifacts_parser/parsers/catalog/catalog_v1.py) for catalog.json v1

### Manifest
- [ManifestV1](dbt_artifacts_parser/parsers/manifest/manifest_v1.py) for manifest.json v1
- [ManifestV2](dbt_artifacts_parser/parsers/manifest/manifest_v2.py) for manifest.json v2
- [ManifestV3](dbt_artifacts_parser/parsers/manifest/manifest_v3.py) for manifest.json v3
- [ManifestV4](dbt_artifacts_parser/parsers/manifest/manifest_v4.py) for manifest.json v4
- [ManifestV5](dbt_artifacts_parser/parsers/manifest/manifest_v5.py) for manifest.json v5
- [ManifestV6](dbt_artifacts_parser/parsers/manifest/manifest_v6.py) for manifest.json v6
- [ManifestV7](dbt_artifacts_parser/parsers/manifest/manifest_v7.py) for manifest.json v7
- [ManifestV8](dbt_artifacts_parser/parsers/manifest/manifest_v8.py) for manifest.json v8
- [ManifestV9](dbt_artifacts_parser/parsers/manifest/manifest_v9.py) for manifest.json v9

### Run Results
- [RunResultsV1](dbt_artifacts_parser/parsers/manifest/manifest_v1.py) for run_results.json v1
- [RunResultsV2](dbt_artifacts_parser/parsers/manifest/manifest_v2.py) for run_results.json v2
- [RunResultsV3](dbt_artifacts_parser/parsers/manifest/manifest_v3.py) for run_results.json v3
- [RunResultsV4](dbt_artifacts_parser/parsers/manifest/manifest_v4.py) for run_results.json v4

### Sources
- [SourcesV1](dbt_artifacts_parser/parsers/sources/sources_v1.py) for sources.json v1
- [SourcesV2](dbt_artifacts_parser/parsers/sources/sources_v2.py) for sources.json v2
- [SourcesV3](dbt_artifacts_parser/parsers/sources/sources_v3.py) for sources.json v3

## Examples

### Parse catalog.json
```python
import json

# parse any version of catalog.json
from dbt_artifacts_parser.parser import parse_catalog

with open("path/to/catalog.json", "r") as fp:
    catalog_dict = json.load(fp)
    catalog_obj = parse_catalog(catalog=catalog_dict)

# parse catalog.json v1
from dbt_artifacts_parser.parser import parse_catalog_v1

with open("path/to/catalog.json", "r") as fp:
    catalog_dict = json.load(fp)
    catalog_obj = parse_catalog_v1(catalog=catalog_dict)
```

### Parse manifest.json

```python
import json

# parse any version of manifest.json
from dbt_artifacts_parser.parser import parse_manifest

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest(manifest=manifest_dict)

# parse manifest.json v1
from dbt_artifacts_parser.parser import parse_manifest_v1

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v1(manifest=manifest_dict)

# parse manifest.json v2
from dbt_artifacts_parser.parser import parse_manifest_v2

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v2(manifest=manifest_dict)

# parse manifest.json v3
from dbt_artifacts_parser.parser import parse_manifest_v3

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v3(manifest=manifest_dict)

# parse manifest.json v4
from dbt_artifacts_parser.parser import parse_manifest_v4

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v4(manifest=manifest_dict)

# parse manifest.json v5
from dbt_artifacts_parser.parser import parse_manifest_v5

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v5(manifest=manifest_dict)

# parse manifest.json v6
from dbt_artifacts_parser.parser import parse_manifest_v6

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v6(manifest=manifest_dict)

# parse manifest.json v7
from dbt_artifacts_parser.parser import parse_manifest_v7

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v7(manifest=manifest_dict)

# parse manifest.json v8
from dbt_artifacts_parser.parser import parse_manifest_v8

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v8(manifest=manifest_dict)

# parse manifest.json v9
from dbt_artifacts_parser.parser import parse_manifest_v9

with open("path/to/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v9(manifest=manifest_dict)
```

### Parse run-results.json

```python
import json

# parse any version of run-results.json
from dbt_artifacts_parser.parser import parse_run_results

with open("path/to/run-resultsjson", "r") as fp:
    run_results_dict = json.load(fp)
    run_results_obj = parse_run_results(run_results=run_results_dict)

# parse run-results.json v1
from dbt_artifacts_parser.parser import parse_run_results_v1

with open("path/to/run-results.json", "r") as fp:
    run_results_dict = json.load(fp)
    run_results_obj = parse_run_results_v1(run_results=run_results_dict)

# parse run-results.json v2
from dbt_artifacts_parser.parser import parse_run_results_v2

with open("path/to/run-results.json", "r") as fp:
    run_results_dict = json.load(fp)
    run_results_obj = parse_run_results_v2(run_results=run_results_dict)

# parse run-results.json v3
from dbt_artifacts_parser.parser import parse_run_results_v3

with open("path/to/run-results.json", "r") as fp:
    run_results_dict = json.load(fp)
    run_results_obj = parse_run_results_v3(run_results=run_results_dict)

# parse run-results.json v4
from dbt_artifacts_parser.parser import parse_run_results_v4

with open("path/to/run-results.json", "r") as fp:
    run_results_dict = json.load(fp)
    run_results_obj = parse_run_results_v4(run_results=run_results_dict)
```

### Parse sources.json

```python
import json

# parse any version of sources.json
from dbt_artifacts_parser.parser import parse_sources

with open("path/to/sources.json", "r") as fp:
    sources_dict = json.load(fp)
    sources_obj = parse_sources(sources=sources_dict)

# parse sources.json v1
from dbt_artifacts_parser.parser import parse_sources_v1

with open("path/to/sources.json", "r") as fp:
    sources_dict = json.load(fp)
    sources_obj = parse_sources_v1(sources=sources_dict)

# parse sources.json v2
from dbt_artifacts_parser.parser import parse_sources_v2

with open("path/to/sources.json", "r") as fp:
    sources_dict = json.load(fp)
    sources_obj = parse_sources_v2(sources=sources_dict)

# parse sources.json v3
from dbt_artifacts_parser.parser import parse_sources_v3

with open("path/to/sources.json", "r") as fp:
    sources_dict = json.load(fp)
    sources_obj = parse_sources_v3(sources=sources_dict)
```

## Contributors
<!-- readme: contributors -start -->
<table>
<tr>
    <td align="center">
        <a href="https://github.com/yu-iskw">
            <img src="https://avatars.githubusercontent.com/u/1523515?v=4" width="100;" alt="yu-iskw"/>
            <br />
            <sub><b>Yu Ishikawa</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/bbrewington">
            <img src="https://avatars.githubusercontent.com/u/10573749?v=4" width="100;" alt="bbrewington"/>
            <br />
            <sub><b>Brent Brewington</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/judahrand">
            <img src="https://avatars.githubusercontent.com/u/17158624?v=4" width="100;" alt="judahrand"/>
            <br />
            <sub><b>Judah Rand</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/nabilm">
            <img src="https://avatars.githubusercontent.com/u/987369?v=4" width="100;" alt="nabilm"/>
            <br />
            <sub><b>Mohamed Nabil Mahmoud Hafez</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/dlawin">
            <img src="https://avatars.githubusercontent.com/u/11282254?v=4" width="100;" alt="dlawin"/>
            <br />
            <sub><b>Null</b></sub>
        </a>
    </td></tr>
</table>
<!-- readme: contributors -end -->
