# tartan-maker

`tartan-maker` turns compact tartan specifications into validated YAML, SVG artwork, PNG exports, and Scottish Register of Tartans-style pallet/threadcount fields.

It is built around one rule: **SVG is the source of truth**. PNG output is generated from the SVG renderer rather than through a separate raster implementation.

<div class="grid cards" markdown>

-   :material-image-filter-hdr: **Render tartans**

    Render symmetrical and asymmetrical setts to clean SVG.

-   :material-check-decagram: **Validate specs**

    Catch missing colors, bad pivots, unused palette entries, and suspicious repeat sizes.

-   :material-format-list-bulleted-square: **Export SRT fields**

    Generate `Pallet:` and `Threadcount:` values suitable for recordkeeping.

-   :material-console: **Use it from the shell**

    A small, normal-looking command-line utility for repeatable work.

</div>

<p align="center">
  <img src="assets/examples/black-watch-government.svg" alt="Black Watch / Government tartan" width="30%">
  <img src="assets/examples/buchanan.svg" alt="Buchanan tartan" width="30%">
  <img src="assets/examples/royal-stewart.svg" alt="Royal Stewart tartan" width="30%">
</p>

## Quick example

```bash
tartan-maker render examples/black-watch-government.yaml -o black-watch.svg
```

```bash
tartan-maker inspect examples/buchanan.yaml
```

```bash
tartan-maker srt examples/macleod-of-lewis.yaml
```
