# Installation

## Local development install

From the repository root:

```bash
pip install -e .
```

## PNG support

PNG output is generated from SVG using CairoSVG. Install the optional PNG extra when you want raster exports:

```bash
pip install -e ".[png]"
```

## Development tools

For tests, linting, and type checking:

```bash
pip install -e ".[dev,png]"
```

## Documentation tools

The documentation site uses MkDocs:

```bash
pip install -e ".[png]"
pip install mkdocs mkdocs-material mkdocstrings[python]
```

Run the site locally:

```bash
mkdocs serve
```

Build the static site:

```bash
mkdocs build --strict
```
