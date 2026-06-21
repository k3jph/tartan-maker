# Development

## Run tests

```bash
python -m pytest -q
```

## Lint

```bash
ruff check .
```

## Type check

```bash
mypy src
```

## Build package artifacts

```bash
python -m build
```

## Build documentation locally

```bash
pip install -e ".[png]"
pip install mkdocs mkdocs-material mkdocstrings[python]
mkdocs serve
```

## GitHub Actions

The provided workflow does two things:

1. Runs unit tests on every push, pull request, and manual dispatch.
2. Builds and deploys the MkDocs site to GitHub Pages only on pushes to `main`.

Before the Pages deployment works, set the repository's Pages source to **GitHub Actions** in repository settings.
