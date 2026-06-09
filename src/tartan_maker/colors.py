"""Color normalization helpers."""

from __future__ import annotations

import re

import webcolors

from .errors import ColorError

HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")
CODE_RE = re.compile(r"^[A-Z]+$")


def normalize_color(value: str) -> str:
    """Return an uppercase #RRGGBB hex value.

    Accepted inputs are #RRGGBB, RRGGBB, and color names known to webcolors.
    Unknown names fail loudly.
    """
    raw = value.strip()
    if not raw:
        raise ColorError("Color value cannot be empty")

    if HEX_RE.match(raw):
        if not raw.startswith("#"):
            raw = f"#{raw}"
        return raw.upper()

    try:
        return webcolors.name_to_hex(raw).upper()
    except ValueError as exc:
        raise ColorError(f"Unknown color name or invalid hex value: {value!r}") from exc


def validate_color_code(code: str) -> None:
    """Validate an internal or SRT color code."""
    if not CODE_RE.match(code):
        raise ColorError(f"Invalid color code {code!r}; expected capital letters")
