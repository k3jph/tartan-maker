"""Core data model for tartan-maker."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal


class SettType(StrEnum):
    """The two SRT-relevant sett types."""

    SYMMETRICAL = "symmetrical"
    ASYMMETRICAL = "asymmetrical"


@dataclass(frozen=True)
class Color:
    """A resolved tartan color."""

    code: str
    name: str
    source: str
    hex: str
    srt_code: str | None = None
    srt_name: str | None = None

    @property
    def srt_display_code(self) -> str:
        return self.srt_code or self.code

    @property
    def srt_display_name(self) -> str:
        return self.srt_name or self.name.upper()


@dataclass(frozen=True)
class Stripe:
    """A single stripe in a threadcount."""

    color: str
    count: int
    pivot: bool = False


@dataclass(frozen=True)
class RenderOptions:
    """Rendering options for SVG and derived PNG output."""

    size: int = 792
    weave: bool = True
    preserve_aspect_ratio: str = "xMidYMid meet"
    css_classes: bool = True
    title: bool = True


@dataclass(frozen=True)
class TartanSpec:
    """A complete tartan specification."""

    name: str
    sett_type: SettType
    colors: dict[str, Color]
    sett: list[Stripe]
    render: RenderOptions = field(default_factory=RenderOptions)
    description: str | None = None


@dataclass(frozen=True)
class ValidationIssue:
    """A structured validation issue."""

    severity: Literal["warning", "error"]
    message: str
    code: str
