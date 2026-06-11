# CLI reference

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

## `render`

Render a YAML tartan spec to SVG or PNG.

```bash
tartan-maker render examples/black-watch-government.yaml -o black-watch.svg
```

The output format is inferred from the output filename.

## `srt`

Generate Scottish Register-style pallet and threadcount fields.

```bash
tartan-maker srt examples/buchanan.yaml
```

## `inspect`

Validate and summarize a tartan spec.

```bash
tartan-maker inspect examples/royal-stewart.yaml
```

## `parse-sett`

Parse compact sett notation and print YAML pair form.

```bash
tartan-maker parse-sett "B/24 W4 B24 R2 K24 G24 W/2"
```

## `color`

Resolve a web color name or hex value to normalized `#RRGGBB`.

```bash
tartan-maker color darkred
```

## `normalize`

Print a normalized YAML view of a tartan spec.

```bash
tartan-maker normalize examples/macleod-of-lewis.yaml
```

## Logging

The CLI uses `spdlog` directly.

Show warnings:

```bash
tartan-maker render examples/royal-stewart.yaml -o royal-stewart.svg --log-level warning
```

Write logs to a file:

```bash
tartan-maker inspect examples/buchanan.yaml --log-file tartan-maker.log --log-level info
```
