"""SVG renderer for tartan-maker."""

from __future__ import annotations

from html import escape
from pathlib import Path

from .model import Stripe, TartanSpec
from .validate import visual_repeat, visual_stripes


def _style(spec: TartanSpec) -> str:
    rows = [
        "#threadcounts rect { shape-rendering: crispEdges; }",
        "#weave rect { shape-rendering: crispEdges; }",
    ]
    for code, color in spec.colors.items():
        rows.append(f".{code} {{ fill: {color.hex}; }}")
    return "\n      ".join(rows)


def _thread_rects(stripes: list[Stripe], spec: TartanSpec) -> str:
    y = 0
    rows: list[str] = []
    for stripe in stripes:
        if spec.render.css_classes:
            rows.append(
                f'      <rect class="{escape(stripe.color)}" y="{y}" height="{stripe.count}" width="100%"/>'
            )
        else:
            color = spec.colors[stripe.color].hex
            rows.append(
                f'      <rect fill="{color}" y="{y}" height="{stripe.count}" width="100%"/>'
            )
        y += stripe.count
    return "\n".join(rows)


def render_svg(spec: TartanSpec) -> str:
    """Return an SVG string for the tartan."""
    stripes = visual_stripes(spec)
    repeat = visual_repeat(spec)
    center = repeat / 2
    size = spec.render.size
    title = f"  <title>{escape(spec.name)}</title>\n" if spec.render.title else ""
    style = _style(spec) if spec.render.css_classes else "#threadcounts rect { shape-rendering: crispEdges; }"
    rects = _thread_rects(stripes, spec)
    mask_attr = ' mask="url(#weave)"' if spec.render.weave else ""
    weave_defs = ""
    if spec.render.weave:
        weave_defs = f'''
    <pattern id="weaveGrain" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="scale(0.5)">
      <polygon points="0,4 0,8 8,0 4,0" fill="white"/>
      <polygon points="4,8 8,8 8,4" fill="white"/>
    </pattern>
    <mask id="weave">
      <rect width="100%" height="100%" fill="url(#weaveGrain)"/>
    </mask>'''

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" version="1.1" id="tartan-svg" preserveAspectRatio="{escape(spec.render.preserve_aspect_ratio)}">
{title}  <defs>
    <style>
      {style}
    </style>{weave_defs}
    <g id="threadcounts">
{rects}
    </g>
    <pattern id="settHorizontal" patternUnits="userSpaceOnUse" patternContentUnits="userSpaceOnUse" width="{repeat}" height="{repeat}">
      <use href="#threadcounts" x="0" y="0"/>
    </pattern>
    <pattern id="settVertical" patternUnits="userSpaceOnUse" patternContentUnits="userSpaceOnUse" width="{repeat}" height="{repeat}">
      <use href="#threadcounts" x="0" y="0" transform="rotate(90 {center:g} {center:g})"{mask_attr}/>
    </pattern>
    <pattern id="fullSett" patternUnits="userSpaceOnUse" patternContentUnits="userSpaceOnUse" width="{repeat}" height="{repeat}">
      <rect fill="url(#settHorizontal)" width="100%" height="100%"/>
      <rect fill="url(#settVertical)" width="100%" height="100%"/>
    </pattern>
  </defs>
  <rect fill="url(#fullSett)" width="100%" height="100%"/>
</svg>
'''


def write_svg(spec: TartanSpec, path: str | Path) -> None:
    """Render and write SVG to disk."""
    Path(path).write_text(render_svg(spec), encoding="utf-8")
