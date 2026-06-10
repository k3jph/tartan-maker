"""tartan-maker public API."""

from ._version import __version__
from .colors import normalize_color
from .inspect import inspect_spec
from .model import Color, RenderOptions, SettType, Stripe, TartanSpec, ValidationIssue
from .render_png import render_png, write_png
from .render_svg import render_svg, write_svg
from .sett import parse_sett_string, stripes_to_sett_string, stripes_to_yaml_pairs
from .spec import load_spec, spec_from_dict
from .srt import rotate_to_earliest_color, to_srt_block, to_srt_pallet, to_srt_threadcount
from .validate import expand_symmetrical_sett, expand_to_direct_repeat, validate_spec, visual_repeat, visual_stripes

__all__ = [
    "__version__",
    "Color",
    "RenderOptions",
    "SettType",
    "Stripe",
    "TartanSpec",
    "ValidationIssue",
    "inspect_spec",
    "load_spec",
    "normalize_color",
    "parse_sett_string",
    "render_png",
    "render_svg",
    "rotate_to_earliest_color",
    "spec_from_dict",
    "stripes_to_sett_string",
    "stripes_to_yaml_pairs",
    "to_srt_block",
    "to_srt_pallet",
    "to_srt_threadcount",
    "expand_symmetrical_sett",
    "expand_to_direct_repeat",
    "validate_spec",
    "visual_repeat",
    "visual_stripes",
    "write_png",
    "write_svg",
]
