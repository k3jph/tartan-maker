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
tartan-maker render examples/black-watch-government.yaml -o /tmp/black-watch.svg
tartan-maker render examples/buchanan.yaml -o /tmp/buchanan.svg
```

## Release checklist

1. Update `src/tartan_maker/_version.py`.
2. Update `pyproject.toml`.
3. Update `CHANGELOG.md`.
4. Run `python -m pytest -q`.
5. Build distributions with `python -m build`.
6. Inspect the generated `dist/` contents before publishing.

## Example tartans

Bundled examples should be useful for testing the renderer, validator, and SRT exporter. Prefer examples with clear sources, stable threadcounts, and comments showing where the data came from.

Published tartans in `examples/` are reference inputs, not original design filings.
