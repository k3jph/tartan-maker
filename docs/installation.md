# Installation

Requires **Python 3.11+**.

## Install from PyPI

For the command-line interface and SVG output:

```bash
python -m pip install tartan-maker
```

For PNG export through CairoSVG:

```bash
python -m pip install "tartan-maker[png]"
```

Check the installed CLI:

```bash
tartan-maker --version
tartan-maker --help
```

The package installs the `tartan-maker` command. No Python source checkout is needed. The repository's `examples/` directory is **not** bundled in the installed wheel; download examples from [GitHub](https://github.com/k3jph/tartan-maker/tree/main/examples) or [write your own YAML](quickstart.md).

## Development checkout

From the repository root:

```bash
python -m pip install -e ".[dev,png]"
```

## Documentation tools

```bash
python -m pip install mkdocs mkdocs-material "mkdocstrings[python]"
mkdocs serve
```

Use `mkdocs build --strict` to build the static site.
