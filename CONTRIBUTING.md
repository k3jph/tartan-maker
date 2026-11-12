# Contributing

`tartan-maker` is intentionally small. Changes should preserve the central rule: SVG is the canonical renderer, and PNG output is derived from SVG.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,png]"
```

## Before committing

Run the test suite:

```bash
python -m pytest -q
```

Run the linter if available:

```bash
ruff check .
```

For changes that affect the CLI, check the visible help:

```bash
tartan-maker --help
tartan-maker render --help
tartan-maker --version
```

For renderer changes, render both a symmetrical and an asymmetrical example:

```bash
tartan-maker render examples/black-watch.yaml -o /tmp/black-watch.svg
tartan-maker render examples/buchanan.yaml -o /tmp/buchanan.svg
```

## Release checklist

1. Create a release branch from `main` using Git Flow.
2. Update `src/tartan_maker/_version.py`, `pyproject.toml`, and `CHANGELOG.md` together.
3. Run `python -m pytest -q` and `ruff check .`.
4. Build distributions with `python -m build` and validate with `python -m twine check --strict dist/*`.
5. Install the built wheel in a fresh virtual environment and smoke-test `tartan-maker --version` and an SVG render.
6. Review the release PR, verify GitHub Actions, merge to `main`, and arrange the PyPI Trusted Publisher (see [release guide](docs/publishing.md)).
7. Publish a GitHub Release tagged `v<version>` from the tested `main` commit. The `publish.yml` workflow checks the tag against the package version and uses PyPI's short-lived OIDC credentials. Verify the live PyPI installation before announcing the release.

No PyPI API tokens belong in the repository, its secrets, or its documentation. Do not publish until the trusted publisher and protected GitHub environment are configured.

## Example tartans

Bundled source examples should be useful for testing the renderer, validator, and SRT exporter. Prefer examples with clear sources, stable threadcounts, and comments showing where the data came from.

Published tartans in `examples/` are reference inputs, not original design filings.
