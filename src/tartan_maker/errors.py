"""Exception types for tartan-maker."""

from __future__ import annotations


class TartanMakerError(Exception):
    """Base exception for tartan-maker."""


class ColorError(TartanMakerError):
    """Raised when a color cannot be resolved or validated."""


class SettParseError(TartanMakerError):
    """Raised when compact sett notation cannot be parsed."""


class SpecLoadError(TartanMakerError):
    """Raised when a YAML spec cannot be loaded."""


class ValidationError(TartanMakerError):
    """Raised when a tartan specification is invalid."""


class RenderError(TartanMakerError):
    """Raised when rendering fails."""
