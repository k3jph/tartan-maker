"""Validation and computed properties."""

from __future__ import annotations

from .model import SettType, Stripe, TartanSpec, ValidationIssue


def _split_pivot(stripe: Stripe) -> tuple[Stripe, Stripe]:
    """Split a pivot stripe across the repeat boundary.

    Symmetrical SRT notation gives a reflective half-sett. For rendering, that
    half-sett is compiled into a direct/full repeat. The first pivot lies on the
    pattern boundary, so half of it appears at the beginning of the direct repeat
    and half appears at the end.

    Odd pivot counts cannot split evenly into integer thread counts. In that case
    the leading side receives the smaller half and the trailing side receives the
    larger half, preserving the original total.
    """
    leading = stripe.count // 2
    trailing = stripe.count - leading
    return (
        Stripe(stripe.color, leading, pivot=False),
        Stripe(stripe.color, trailing, pivot=False),
    )


def expand_symmetrical_sett(stripes: list[Stripe]) -> list[Stripe]:
    """Compile a symmetrical half-sett into a direct/full repeat.

    The returned sequence contains no pivot markers and can be rendered by the
    same direct/asymmetrical renderer used for full setts.

    Given:

        A/10 B20 C/6

    the expanded direct repeat is:

        A5 B20 C6 B20 A5

    More generally:

        first_pivot/2 + interior + last_pivot + reverse(interior) + first_pivot/2
    """
    if len(stripes) < 2:
        return list(stripes)

    first = stripes[0]
    last = stripes[-1]
    interior = [Stripe(s.color, s.count, pivot=False) for s in stripes[1:-1]]
    first_leading, first_trailing = _split_pivot(first)

    expanded: list[Stripe] = []
    if first_leading.count:
        expanded.append(first_leading)
    expanded.extend(interior)
    expanded.append(Stripe(last.color, last.count, pivot=False))
    expanded.extend(reversed(interior))
    if first_trailing.count:
        expanded.append(first_trailing)

    return expanded


def expand_to_direct_repeat(spec: TartanSpec) -> list[Stripe]:
    """Compile any tartan spec into the direct/full repeat used by renderers.

    Asymmetrical setts are already direct repeats. Symmetrical setts are first
    expanded into direct repeats so the SVG renderer only has one rendering path.
    """
    if spec.sett_type == SettType.ASYMMETRICAL:
        return [Stripe(s.color, s.count, pivot=False) for s in spec.sett]
    return expand_symmetrical_sett(spec.sett)


def visual_stripes(spec: TartanSpec) -> list[Stripe]:
    """Backward-compatible alias for expand_to_direct_repeat()."""
    return expand_to_direct_repeat(spec)


def visual_repeat(spec: TartanSpec) -> int:
    """Return the total thread count of the rendered repeat."""
    return sum(stripe.count for stripe in visual_stripes(spec))


def colors_used(spec: TartanSpec) -> set[str]:
    """Return color codes used in the submitted sett."""
    return {stripe.color for stripe in spec.sett}


def colors_unused(spec: TartanSpec) -> set[str]:
    """Return defined color codes not used in the submitted sett."""
    return set(spec.colors) - colors_used(spec)


def earliest_used_srt_code(spec: TartanSpec) -> str | None:
    """Return alphabetically earliest used SRT display code."""
    used = colors_used(spec)
    codes = [spec.colors[color].srt_display_code for color in used if color in spec.colors]
    return min(codes) if codes else None


def first_used_srt_code(spec: TartanSpec) -> str | None:
    """Return the SRT display code of the first stripe."""
    if not spec.sett:
        return None
    color = spec.colors.get(spec.sett[0].color)
    return color.srt_display_code if color else None


def validate_spec(spec: TartanSpec) -> list[ValidationIssue]:
    """Return validation issues. Errors should block rendering/export."""
    issues: list[ValidationIssue] = []

    if not spec.name.strip():
        issues.append(ValidationIssue("error", "Name cannot be empty", "name-empty"))
    if len(spec.colors) < 2:
        issues.append(ValidationIssue("error", "At least two colors must be defined", "colors-too-few"))
    if len(spec.sett) < 2:
        issues.append(ValidationIssue("error", "Sett must contain at least two stripes", "sett-too-short"))

    used = colors_used(spec)
    if len(used) < 2:
        issues.append(ValidationIssue("error", "Sett must use at least two colors", "sett-colors-too-few"))

    for stripe in spec.sett:
        if stripe.color not in spec.colors:
            issues.append(
                ValidationIssue(
                    "error",
                    f"Stripe uses undefined color code {stripe.color}",
                    "undefined-color",
                )
            )
        if stripe.count < 1:
            issues.append(
                ValidationIssue("error", "Stripe count must be positive", "invalid-stripe-count")
            )

    for code in sorted(colors_unused(spec)):
        issues.append(ValidationIssue("warning", f"Color {code} is defined but not used", "unused-color"))

    pivots = [stripe for stripe in spec.sett if stripe.pivot]
    if spec.sett_type == SettType.SYMMETRICAL:
        if len(pivots) != 2:
            issues.append(
                ValidationIssue(
                    "error",
                    "Symmetrical setts must have exactly two pivot stripes",
                    "symmetrical-pivot-count",
                )
            )
        if spec.sett and not spec.sett[0].pivot:
            issues.append(
                ValidationIssue(
                    "error",
                    "Symmetrical setts must mark the first stripe as a pivot",
                    "symmetrical-first-pivot",
                )
            )
        if spec.sett and not spec.sett[-1].pivot:
            issues.append(
                ValidationIssue(
                    "error",
                    "Symmetrical setts must mark the last stripe as a pivot",
                    "symmetrical-last-pivot",
                )
            )
    else:
        if pivots:
            issues.append(
                ValidationIssue(
                    "error",
                    "Asymmetrical setts must not contain pivot stripes",
                    "asymmetrical-pivots",
                )
            )
        first = first_used_srt_code(spec)
        earliest = earliest_used_srt_code(spec)
        if first and earliest and first != earliest:
            issues.append(
                ValidationIssue(
                    "warning",
                    f"Asymmetrical SRT threadcount starts with {first}, but earliest used code is {earliest}",
                    "asymmetrical-start-code",
                )
            )

    repeat = visual_repeat(spec)
    if repeat < 100:
        issues.append(
            ValidationIssue(
                "warning",
                f"Visual repeat is {repeat} threads, which may be check-like or small for registration guidance",
                "repeat-small",
            )
        )
    elif repeat < 220 or repeat > 280:
        issues.append(
            ValidationIssue(
                "warning",
                f"Visual repeat is {repeat} threads, outside the rough 240-260 six-inch guidance range",
                "repeat-size",
            )
        )

    return issues


def raise_for_errors(issues: list[ValidationIssue]) -> None:
    """Raise ValidationError if any error issues exist."""
    from .errors import ValidationError

    errors = [issue.message for issue in issues if issue.severity == "error"]
    if errors:
        raise ValidationError("; ".join(errors))
