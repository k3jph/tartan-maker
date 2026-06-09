"""Parsing and formatting compact tartan sett notation."""

from __future__ import annotations

import re

from .errors import SettParseError
from .model import SettType, Stripe

SETT_TOKEN_RE = re.compile(r"^(?P<color>[A-Z]+)(?P<pivot>/)?(?P<count>[1-9][0-9]*)$")
ELLIPSIS_RE = re.compile(r"^\.\.\.(?P<body>.*)\.\.\.$", re.DOTALL)


def strip_ellipsis(value: str) -> tuple[str, bool]:
    """Strip asymmetrical ellipsis markers, returning body and whether markers existed."""
    stripped = value.strip()
    match = ELLIPSIS_RE.match(stripped)
    if match:
        return match.group("body").strip(), True
    return stripped, False


def parse_sett_string(value: str) -> list[Stripe]:
    """Parse compact sett notation into Stripe objects."""
    body, _ = strip_ellipsis(value)
    if not body:
        raise SettParseError("Sett string cannot be empty")

    stripes: list[Stripe] = []
    for token in body.split():
        match = SETT_TOKEN_RE.match(token)
        if not match:
            raise SettParseError(f"Invalid sett token: {token!r}")
        color = match.group("color")
        count = int(match.group("count"))
        pivot = bool(match.group("pivot"))
        stripes.append(Stripe(color=color, count=count, pivot=pivot))

    if not stripes:
        raise SettParseError("Sett string cannot be empty")
    return stripes


def detect_sett_type(value: str) -> SettType | None:
    """Infer sett type from notation markers, when possible."""
    _, has_ellipsis = strip_ellipsis(value)
    if has_ellipsis:
        return SettType.ASYMMETRICAL
    try:
        stripes = parse_sett_string(value)
    except SettParseError:
        return None
    if any(stripe.pivot for stripe in stripes):
        return SettType.SYMMETRICAL
    return None


def format_stripe(stripe: Stripe, *, include_pivots: bool = True, code: str | None = None) -> str:
    """Format a single stripe as compact notation."""
    color_code = code or stripe.color
    pivot = "/" if include_pivots and stripe.pivot else ""
    return f"{color_code}{pivot}{stripe.count}"


def stripes_to_sett_string(stripes: list[Stripe], *, include_pivots: bool = True) -> str:
    """Convert Stripe objects to compact notation."""
    if not stripes:
        raise SettParseError("Cannot format an empty stripe list")
    return " ".join(format_stripe(stripe, include_pivots=include_pivots) for stripe in stripes)


def stripes_to_yaml_pairs(stripes: list[Stripe]) -> list[list[str | int]]:
    """Convert stripes to compact YAML pair/triple form."""
    rows: list[list[str | int]] = []
    for stripe in stripes:
        row: list[str | int] = [stripe.color, stripe.count]
        if stripe.pivot:
            row.append("pivot")
        rows.append(row)
    return rows


def parse_sett_list(value: list[object]) -> list[Stripe]:
    """Parse YAML list-form setts."""
    stripes: list[Stripe] = []
    for item in value:
        if isinstance(item, dict):
            try:
                color = str(item["color"])
                count = int(item["count"])
            except (KeyError, TypeError, ValueError) as exc:
                raise SettParseError(f"Invalid sett item: {item!r}") from exc
            pivot = bool(item.get("pivot", False))
        elif isinstance(item, list):
            if len(item) < 2 or len(item) > 3:
                raise SettParseError(f"Invalid sett row: {item!r}")
            color = str(item[0])
            try:
                count = int(item[1])
            except (TypeError, ValueError) as exc:
                raise SettParseError(f"Invalid count in sett row: {item!r}") from exc
            pivot = len(item) == 3 and str(item[2]).lower() in {"pivot", "true", "yes"}
        else:
            raise SettParseError(f"Invalid sett item: {item!r}")

        if count < 1:
            raise SettParseError(f"Stripe count must be positive: {item!r}")
        if not SETT_TOKEN_RE.match(f"{color}{count}"):
            raise SettParseError(f"Invalid color code in sett row: {item!r}")
        stripes.append(Stripe(color=color, count=count, pivot=pivot))

    if not stripes:
        raise SettParseError("Sett list cannot be empty")
    return stripes
