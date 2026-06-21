# YAML format

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

## Fields

### `name`

Human-readable tartan name.

### `sett_type`

Either `symmetrical` or `asymmetrical`.

### `colors`

A mapping from short color codes to color definitions. Each entry has a display name and a hex color. The optional `srt` block preserves Scottish Register-style pallet naming.

### `sett`

Compact stripe notation. Each stripe is a color code followed by a threadcount.

### `render`

Rendering options, including output size, weave effect, and SVG `preserveAspectRatio` behavior.

## Symmetrical setts

Symmetrical setts encode the half-sett and mark both pivots with `/`.

```text
DB/44 R4 DB4 R4 DB4 G24 R4 G24 R4 DB/4
```

The first and last stripes must be pivots. `tartan-maker` compiles the half-sett to a full direct repeat internally before rendering.

## Asymmetrical setts

Asymmetrical setts encode the full/direct repeat in order and do not use pivot markers.

```text
B18 G46 K6 B18 K6 Y40 K6 Y40 K6 B18 K6 R40 W6 R40 K6 B18 K6 G46
```

That distinction matters because an asymmetrical tartan is not a mirrored half-sett.
