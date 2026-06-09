"""PNG export derived from SVG rendering."""

from __future__ import annotations

from pathlib import Path

from .errors import RenderError
from .model import TartanSpec
from .render_svg import render_svg


def render_png(
    spec: TartanSpec,
    *,
    output_width: int | None = None,
    output_height: int | None = None,
    scale: float | None = None,
) -> bytes:
    """Render PNG bytes by first generating SVG."""
    try:
        import cairosvg
    except ImportError as exc:
        raise RenderError(
            'PNG export requires the optional dependency cairosvg. Install with: pip install "tartan-maker[png]"'
        ) from exc

    svg = render_svg(spec)
    kwargs: dict[str, object] = {}
    if output_width is not None:
        kwargs["output_width"] = output_width
    if output_height is not None:
        kwargs["output_height"] = output_height
    if scale is not None:
        kwargs["scale"] = scale
    return cairosvg.svg2png(bytestring=svg.encode("utf-8"), **kwargs)


def write_png(
    spec: TartanSpec,
    path: str | Path,
    *,
    output_width: int | None = None,
    output_height: int | None = None,
    scale: float | None = None,
) -> None:
    """Render PNG from SVG and write it to disk."""
    png = render_png(spec, output_width=output_width, output_height=output_height, scale=scale)
    Path(path).write_bytes(png)
