# Changelog

All notable changes to `tartan-maker` are collected here.

## 0.9.1 - 2026-06-20

### Added

- Added a MkDocs documentation site with installation, quick-start, YAML-format, CLI, examples, development, and changelog pages.
- Added rendered SVG previews for all bundled example tartans.
- Added GitHub Actions CI for the supported Python versions.
- Added automated GitHub Pages builds and deployment from `main`.

### Changed

- Refreshed the README with project badges, a shorter package overview, and links to the documentation site.

## 0.9.0 - release preparation

This release prepares `tartan-maker` for a more public Python-package shape.

### Added

- Added a practical `.gitignore` for Python development, packaging, tests, local environments, editor files, and generated render output.
- Added `--version` at the top level of the CLI.
- Added `CHANGELOG.md` as the consolidated release history.
- Added `CONTRIBUTING.md` with a development and release checklist.
- Added `docs/examples.md` documenting the bundled example tartans.
- Added packaged example YAML files for:
  - Black Watch / Government
  - Balmoral (Original)
  - Rob Roy MacGregor
  - Buchanan
  - Royal Stewart
  - MacLeod of Lewis

### Changed

- Replaced the previous personal sample files with published reference tartans in `examples/`.
- Refreshed the README with installation, quick-start, YAML format, examples, commands, rendering model, logging, and development sections.
- Bumped package metadata to `0.9.0`.
- Added package classifiers, keywords, project URLs, and explicit sdist include rules.
- Consolidated the previous per-version `RELEASE-0.2.x.md` files into this changelog.

## 0.2.6

### Changed

- Reused the registered `tartan-maker` `spdlog` logger instead of creating suffixed names such as `tartan-maker-1`.
- Removed the explicit `spdlog` pattern override so output uses the binding's default format unless configured by `spdlog` itself.

## 0.2.5

### Changed

- Ensured CLI error logging is emitted through `spdlog` rather than manually prefixed messages.
- Removed leftover Typer echo-based error reporting from utility commands.
- Used `spdlog` formatting for console and file logger output.

## 0.2.4

### Added

- Added a top-level `--version` option.
- Centralized the package version used by the CLI and generated SVG/PNG metadata.

### Changed

- Kept the plain command-line help style introduced in 0.2.3.

## 0.2.3

### Changed

- Switched Typer help output to plain Click-style command-line help.
- Removed shell-completion helper options from the top-level help screen.
- Added `-h` as a standard alias for `--help`.

## 0.2.2

### Changed

- Made `spdlog>=2.0` a required dependency.
- Removed the Python `logging` fallback and backend selection path.
- Removed the `--log-backend` CLI option.
- Kept `--log-level` and `--log-file`, now backed directly by `spdlog`.

## 0.2.1

### Changed

- Set CLI `--log-level` to default to `error`.
- Kept validation warnings quiet by default.
- Routed validation diagnostics through the logging facade for `render`, `srt`, and `inspect`.
- Generated warp and weft rectangles explicitly instead of reusing one rotated threadcount group.
- Removed the experimental axis-reversal orientation compensation; direct/full setts now draw in supplied order on both axes.

## 0.2.0

### Changed

- Established the SVG-first renderer architecture.
- Used one canonical direct/full-repeat rendering path.
- Compiled symmetrical setts into direct repeats before rendering.
- Made `expand_to_direct_repeat()` the preferred renderer input API.
- Kept `visual_stripes()` as a backward-compatible alias.
- Encoded Black Watch and Balmoral examples as symmetrical half-setts with explicit pivots.
- Added SVG and PNG generator metadata.

The core architectural rule introduced here is:

```text
YAML sett -> parse -> validate -> compile to direct repeat -> SVG -> PNG
```
