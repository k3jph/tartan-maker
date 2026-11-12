# Quick start

This example works after installing `tartan-maker` from PyPI; no repository checkout is required.

## Create a tartan definition

Save the following as `my-tartan.yaml`:

```yaml
name: My First Tartan
sett_type: symmetrical

colors:
  K: {name: Black, color: "#101010"}
  B: {name: Blue, color: "#23579A"}
  Y: {name: Yellow, color: "#F6E27A"}

sett: "K/32 B16 Y4 B16 K/32"

render:
  size: 792
  weave: true
  preserve_aspect_ratio: "xMidYMid meet"
```

The two `/` markers indicate the symmetrical sett's pivots.

## Render SVG

```bash
tartan-maker render my-tartan.yaml -o my-tartan.svg
```

## Render PNG

Install the optional PNG dependency first: `python -m pip install "tartan-maker[png]"`.

```bash
tartan-maker render my-tartan.yaml -o my-tartan.png
```

## Inspect the design

```bash
tartan-maker inspect my-tartan.yaml
```

## Generate SRT-style fields

```bash
tartan-maker srt my-tartan.yaml
```

## Additional utilities

```bash
tartan-maker parse-sett "B/24 W4 B24 R2 K24 G24 W/2"
tartan-maker color darkred
tartan-maker --version
```

For examples of published tartans, see [the repository examples](examples.md). Those example YAML files are included in source checkouts, not in the installed wheel.
