"""Scottish Register of Tartans export helpers."""

from __future__ import annotations

from .model import SettType, Stripe, TartanSpec
from .sett import format_stripe
from .validate import earliest_used_srt_code


def to_srt_pallet(spec: TartanSpec) -> str:
    """Return an SRT-compatible pallet string."""
    parts: list[str] = []
    for color in spec.colors.values():
        parts.append(f"{color.srt_display_code}={color.hex}#{color.srt_display_name.upper()};")
    return "".join(parts)


def _stripe_with_srt_code(spec: TartanSpec, stripe: Stripe, *, include_pivots: bool) -> str:
    color = spec.colors[stripe.color]
    return format_stripe(stripe, include_pivots=include_pivots, code=color.srt_display_code)


def rotate_to_earliest_color(stripes: list[Stripe], spec: TartanSpec) -> list[Stripe]:
    """Rotate an asymmetrical sett to the first occurrence of the earliest used SRT code."""
    if not stripes:
        return []
    earliest = earliest_used_srt_code(spec)
    if earliest is None:
        return list(stripes)
    for index, stripe in enumerate(stripes):
        if spec.colors[stripe.color].srt_display_code == earliest:
            return list(stripes[index:]) + list(stripes[:index])
    return list(stripes)


def to_srt_threadcount(spec: TartanSpec, *, rotate_asymmetrical: bool = False) -> str:
    """Return an SRT-compatible threadcount string."""
    if spec.sett_type == SettType.SYMMETRICAL:
        return " ".join(_stripe_with_srt_code(spec, stripe, include_pivots=True) for stripe in spec.sett)

    stripes = rotate_to_earliest_color(spec.sett, spec) if rotate_asymmetrical else list(spec.sett)
    body = " ".join(_stripe_with_srt_code(spec, stripe, include_pivots=False) for stripe in stripes)
    return f"...{body}..."


def to_srt_block(spec: TartanSpec, *, rotate_asymmetrical: bool = False) -> str:
    """Return both SRT fields as a pasteable text block."""
    return (
        "Pallet:\n"
        f"{to_srt_pallet(spec)}\n\n"
        "Threadcount:\n"
        f"{to_srt_threadcount(spec, rotate_asymmetrical=rotate_asymmetrical)}"
    )
