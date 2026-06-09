"""Inspection reports for tartan specs."""

from __future__ import annotations

from .model import TartanSpec
from .validate import (
    colors_unused,
    colors_used,
    earliest_used_srt_code,
    first_used_srt_code,
    validate_spec,
    visual_repeat,
    visual_stripes,
)


def inspect_spec(spec: TartanSpec) -> str:
    """Return a human-readable inspection report."""
    issues = validate_spec(spec)
    rows = [
        f"Name: {spec.name}",
        f"Sett type: {spec.sett_type.value}",
        f"Defined colors: {len(spec.colors)}",
        f"Used colors: {len(colors_used(spec))}",
        f"Unused colors: {len(colors_unused(spec))}",
        f"Stripes in submitted sett: {len(spec.sett)}",
        f"Stripes in rendered repeat: {len(visual_stripes(spec))}",
        f"Visual repeat: {visual_repeat(spec)}",
    ]
    first = first_used_srt_code(spec)
    earliest = earliest_used_srt_code(spec)
    if first is not None:
        rows.append(f"SRT first used code: {first}")
    if earliest is not None:
        rows.append(f"SRT earliest used code: {earliest}")
    for issue in issues:
        rows.append(f"{issue.severity.title()}: {issue.message}")
    return "\n".join(rows)
