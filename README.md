# tartan-maker

`tartan-maker` is a Python package and command-line tool for defining, validating, rendering, and exporting tartan designs.

The package treats a tartan as structured data: a palette, a threadcount, and a sett type. From one YAML source file, it can generate SVG artwork, PNG artwork derived from the SVG, Scottish Register of Tartans-compatible pallet/threadcount fields, and inspection reports.

## Install locally

```bash
pip install -e .
```

The CLI uses `spdlog` for logging; it is installed as a required dependency.

For optional PNG output:

```bash
pip install -e ".[png]"
```

## Example YAML

```yaml
name: Basu-Howard Tartan
sett_type: asymmetrical

colors:
  W:
    name: White
    color: white
  LB:
    name: Light Blue
    color: "#1959B9"
  MB:
    name: Medium Blue
    color: "#154C9E"
  DB:
    name: Dark Blue
    color: "#103A79"
  Y:
    name: Gold
    color: "#FEE46E"
  DY:
    name: Dark Gold
    color: "#AC8800"

sett: "W8 LB20 MB28 DB36 DY4 Y8 DY4 DB36 DY4 Y8 DY4 DB36 MB28 LB20"

render:
  size: 792
  weave: true
```

## Commands

```bash
tartan-maker inspect basu-howard.yaml
tartan-maker render basu-howard.yaml -o basu-howard.svg
tartan-maker render basu-howard.yaml -o basu-howard.png
tartan-maker srt basu-howard.yaml --rotate-asymmetrical
tartan-maker parse-sett "B/24 W4 B24 R2 K24 G24 W/2"
tartan-maker color darkred
```

## Design rule

SVG is the canonical rendering format. PNG output is generated from SVG output. There is no separate raster drawing engine.

## 0.2.1 renderer note

Version 0.2.1 generates warp and weft rectangles explicitly. Earlier output reused the horizontal threadcount group with a 90-degree rotation for the vertical direction, which could reverse or offset the stripe sequence for non-palindromic setts. The SVG renderer now emits separate `weftThreadcounts` and `warpThreadcounts` groups.

Generated SVGs include an XML comment identifying `tartan-maker` as the generator. PNG exports are still derived from SVG and include PNG `tEXt` metadata chunks for `Software` and `Description`.


## 0.2.1 orientation note

Version 0.2.1 removes the experimental axis-reversal orientation compensation introduced in 0.2.1/0.2.1. The renderer now draws direct/full setts in supplied order on both axes: top-to-bottom for weft and left-to-right for warp.
