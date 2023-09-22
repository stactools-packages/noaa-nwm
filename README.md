# stactools-noaa-nwm

[![PyPI](https://img.shields.io/pypi/v/stactools-noaa-nwm?style=for-the-badge)](https://pypi.org/project/stactools-noaa-nwm/)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/stactools-packages/noaa-nwm/continuous-integration.yml?style=for-the-badge)

- Name: noaa-nwm
- Package: `stactools.noaa_nwm`
- [stactools-noaa-nwm on PyPI](https://pypi.org/project/stactools-noaa-nwm/)
- Owner: @githubusername
- [Dataset homepage](http://example.com)
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `noaa-nwm:custom`: A custom attribute
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/noaa-nwm/main/examples/collection.json)
- [Browse a notebook demonstrating the example item and collection](https://github.com/stactools-packages/noaa-nwm/tree/main/docs/example.ipynb)

A short description of the package and its usage.

## STAC examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation

```shell
pip install stactools-noaa-nwm
```

## Command-line usage

Description of the command line functions

```shell
stac noaa-nwm create-item source destination
```

Use `stac noaa-nwm --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e '.[dev]'
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```

If you've updated the STAC metadata output, update the examples:

```shell
scripts/update-examples
```
