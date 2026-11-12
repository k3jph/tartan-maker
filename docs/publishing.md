# Publishing to PyPI

This project publishes the Python package `tartan-maker` from the public repository
[**k3jph/tartan-maker**](https://github.com/k3jph/tartan-maker). Stable versions
use [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) release
branches and a reviewed GitHub Release on the tested `main` commit.

## One-time PyPI account setup

The package uses **PyPI Trusted Publishing** (GitHub Actions OIDC), not a
long-lived API token.

1. Sign in to the intended project-owner PyPI account at
   [pypi.org](https://pypi.org/).
2. For a new `tartan-maker` project, open
   [Account → Publishing](https://pypi.org/manage/account/publishing/) and
   add a **pending** GitHub trusted publisher. For a project that already exists
   under your account, use the project's **Manage → Publishing** page.
3. Enter the exact values:

   | PyPI field | Value |
   | --- | --- |
   | PyPI project name (for a pending publisher) | `tartan-maker` |
   | GitHub owner | `k3jph` |
   | GitHub repository | `tartan-maker` |
   | Workflow filename | `publish.yml` |
   | Environment name | `pypi` |

4. In the repository's **Settings → Environments**, configure an environment
   named `pypi`. **Require approval from a trusted maintainer** for deployments,
   and restrict deployment to release tags matching `v*` when supported.

A pending publisher does **not** reserve the package name until the first
successful upload. Do not upload under a different name without updating the
project metadata and trusted publisher together.

## Before creating a release

From a clean checkout of the reviewed release candidate:

```bash
python -m pip install -e ".[dev,png]"
python -m pytest -q
ruff check .
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
```

The GitHub CI workflow also builds the wheel and source distribution, installs
the wheel in a fresh virtual environment, and smoke-tests the `tartan-maker`
console entry point and a sample SVG export.

Verify that `pyproject.toml` and `src/tartan_maker/_version.py` identify the
same version, and that the release notes reflect the final contents.

## Publish

1. Merge the reviewed `release/<version>` branch to `main` only after CI passes.
2. On GitHub, create a new **GitHub Release** based on the verified `main`
   commit, with tag `v<version>` (for example, `v1.0.0`).
3. Publishing the GitHub Release starts
   [`.github/workflows/publish.yml`](https://github.com/k3jph/tartan-maker/blob/main/.github/workflows/publish.yml).
   The workflow checks the release tag against the package version, builds
   the sdist and wheel, validates metadata, and requests approval through the
   `pypi` environment.
4. After the approved publish job succeeds, verify the live project at
   [PyPI](https://pypi.org/project/tartan-maker/) and test in a fresh environment:

   ```bash
   python -m pip install "tartan-maker==1.0.0"
   tartan-maker --version
   ```

Never put PyPI passwords, API tokens, or session cookies in GitHub or
repository files. If the workflow fails with a trusted-publisher identity error,
check the exact owner/repository/workflow/environment fields on PyPI before
retrying. A version already accepted by PyPI cannot be overwritten; fix the
source and publish a new patch version instead.

For the authoritative procedure, see
[PyPI's Trusted Publisher guide](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).
