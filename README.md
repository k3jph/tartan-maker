# tartan-maker

`tartan-maker` is a small Python package and command-line utility for turning tartan specifications into useful artifacts: validated YAML, SVG artwork, PNG exports, and Scottish Register of Tartans-style pallet/threadcount fields.

It is intentionally **SVG-first**. The renderer builds a clean SVG from structured tartan data, and PNG output is derived from that SVG. There is one rendering model, one source of truth, and no separate raster engine drifting out of sync.

## What it does

- Defines tartans as readable YAML.
- Supports symmetrical setts with explicit pivot markers.
- Supports asymmetrical/direct setts without pivot markers.
- Validates palettes, threadcounts, pivots, unused colors, and repeat sizes.
- Renders SVG with separate warp and weft threadcount groups.
- Exports PNG through the optional CairoSVG backend.
- Emits SRT-compatible `Pallet:` and `Threadcount:` fields.
- Resolves web color names and hex colors.
- Uses `spdlog` for CLI logging.

## Installation

For local development:

```bash
pip install -e .
```

For PNG export support:

```bash
pip install -e ".[png]"
```

For development tools:

```bash
pip install -e ".[dev,png]"
```

## Quick start

Render one of the bundled examples:

```bash
tartan-maker render examples/black-watch-government.yaml -o black-watch.svg
```

Render PNG instead:

```bash
tartan-maker render examples/royal-stewart.yaml -o royal-stewart.png
```

Inspect a tartan:

```bash
tartan-maker inspect examples/buchanan.yaml
```

Generate Scottish Register of Tartans-style fields:

```bash
tartan-maker srt examples/macleod-of-lewis.yaml
```

Parse compact sett notation into YAML pair form:

```bash
tartan-maker parse-sett "B/24 W4 B24 R2 K24 G24 W/2"
```

Resolve a color:

```bash
tartan-maker color darkred
```

Check the installed version:

```bash
tartan-maker --version
```

## YAML format

A tartan spec has four main parts:

```yaml
name: Buchanan
sett_type: asymmetrical

colors:
  B:
    name: Blue
    color: "#2C2C80"
    srt:
      code: B
      name: BLUE
  G:
    name: Green
    color: "#006818"
    srt:
      code: G
      name: GREEN
  K:
    name: Black
    color: "#101010"
    srt:
      code: K
      name: BLACK

sett: "B18 G46 K6 B18 K6 Y40 K6 Y40 K6 B18 K6 R40 W6 R40 K6 B18 K6 G46"

render:
  size: 792
  weave: true
  preserve_aspect_ratio: "xMidYMid meet"
```

### Sett types

`tartan-maker` recognizes two sett types:

- `symmetrical`: encode the half-sett and mark both pivots with `/`, for example `DB/44 ... DB/4`.
- `asymmetrical`: encode the full/direct repeat in order, with no pivot markers.

Symmetrical setts are compiled internally into a direct/full repeat before rendering. Asymmetrical setts are already direct repeats.

## Examples

The `examples/` directory contains reference encodings of published tartans used for testing and demonstration:

| File | Sett type | Source |
| --- | --- | --- |
| `black-watch-government.yaml` | symmetrical | Scottish Register of Tartans ref. 277 |
| `balmoral-original.yaml` | symmetrical | Scottish Register of Tartans ref. 182 |
| `rob-roy-macgregor.yaml` | symmetrical | Scottish Register of Tartans ref. 3516 |
| `buchanan.yaml` | asymmetrical | Scottish Register of Tartans ref. 414 |
| `royal-stewart.yaml` | symmetrical | Scottish Register of Tartans ref. 3958 |
| `macleod-of-lewis.yaml` | symmetrical | Scottish Register of Tartans ref. 2630 |

These examples are not original design filings. They are practical sample inputs for exercising the parser, validator, renderer, and SRT exporter.

## Commands

```text
Usage: tartan-maker [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  render      Render a tartan to SVG or PNG.
  srt         Generate SRT-compatible pallet and threadcount fields.
  inspect     Inspect and validate a tartan spec.
  parse-sett  Parse compact sett notation and print YAML pair form.
  color       Resolve a web color name or hex value to #RRGGBB.
  normalize   Print a normalized YAML view of a tartan spec.
```

## Rendering model

The rendering pipeline is:

```text
YAML sett -> parse -> validate -> compile to direct repeat -> SVG -> PNG
```

SVG output contains separate `weftThreadcounts` and `warpThreadcounts` groups. That matters for asymmetrical setts: the vertical direction is not produced by rotating the horizontal group, so non-palindromic stripe sequences keep their intended order.

Generated SVGs include a generator comment. PNG exports include `tEXt` metadata chunks for `Software` and `Description`.

## Logging

The CLI uses `spdlog` directly. Validation warnings are quiet by default because normal rendering should not be noisy.

Show warnings:

```bash
tartan-maker render examples/royal-stewart.yaml -o royal-stewart.svg --log-level warning
```

Write logs to a file:

```bash
tartan-maker inspect examples/buchanan.yaml --log-file tartan-maker.log --log-level info
```

## Development

Run the tests:

```bash
python -m pytest -q
```

Run the formatter/linter if installed:

```bash
ruff check .
```

Build release distributions:

```bash
python -m build
```

See `CONTRIBUTING.md` for the development checklist and `CHANGELOG.md` for release history.

## License

MIT. See `LICENSE`.
