"""YAML spec loading and normalization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .colors import normalize_color, validate_color_code
from .errors import SpecLoadError
from .model import Color, RenderOptions, SettType, TartanSpec
from .sett import detect_sett_type, parse_sett_list, parse_sett_string


def _load_yaml(path: str | Path) -> dict[str, Any]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecLoadError(f"Could not read spec file: {path}") from exc

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise SpecLoadError(f"Could not parse YAML: {path}") from exc

    if not isinstance(data, dict):
        raise SpecLoadError("Top-level YAML document must be a mapping")
    return data


def load_spec(path: str | Path) -> TartanSpec:
    """Load and normalize a tartan specification from YAML."""
    return spec_from_dict(_load_yaml(path))


def spec_from_dict(data: dict[str, Any]) -> TartanSpec:
    """Normalize a mapping into a TartanSpec."""
    name = str(data.get("name", "")).strip()
    if not name:
        raise SpecLoadError("Spec requires a non-empty name")

    colors_data = data.get("colors")
    if not isinstance(colors_data, dict):
        raise SpecLoadError("Spec requires a colors mapping")

    colors: dict[str, Color] = {}
    for code, entry in colors_data.items():
        code = str(code)
        validate_color_code(code)
        if not isinstance(entry, dict):
            raise SpecLoadError(f"Color {code} must be a mapping")
        display_name = str(entry.get("name", code)).strip() or code
        source = str(entry.get("color", entry.get("hex", ""))).strip()
        if not source:
            raise SpecLoadError(f"Color {code} requires a color value")
        hex_value = normalize_color(source)
        srt_data = entry.get("srt", {}) or {}
        if not isinstance(srt_data, dict):
            raise SpecLoadError(f"Color {code} srt field must be a mapping")
        srt_code = srt_data.get("code")
        srt_name = srt_data.get("name")
        if srt_code is not None:
            srt_code = str(srt_code)
            validate_color_code(srt_code)
        if srt_name is not None:
            srt_name = str(srt_name)
        colors[code] = Color(
            code=code,
            name=display_name,
            source=source,
            hex=hex_value,
            srt_code=srt_code,
            srt_name=srt_name,
        )

    raw_sett = data.get("sett")
    if isinstance(raw_sett, str):
        inferred = detect_sett_type(raw_sett)
        sett = parse_sett_string(raw_sett)
    elif isinstance(raw_sett, list):
        inferred = None
        sett = parse_sett_list(raw_sett)
    else:
        raise SpecLoadError("Spec requires sett as a compact string or list")

    raw_sett_type = data.get("sett_type")
    if raw_sett_type is None:
        if inferred is None:
            raise SpecLoadError("Spec requires sett_type when it cannot be inferred")
        sett_type = inferred
    else:
        try:
            sett_type = SettType(str(raw_sett_type).lower())
        except ValueError as exc:
            raise SpecLoadError("sett_type must be symmetrical or asymmetrical") from exc

    render_data = data.get("render", {}) or {}
    if not isinstance(render_data, dict):
        raise SpecLoadError("render must be a mapping")
    render = RenderOptions(
        size=int(render_data.get("size", 792)),
        weave=bool(render_data.get("weave", True)),
        preserve_aspect_ratio=str(render_data.get("preserve_aspect_ratio", "xMidYMid meet")),
        css_classes=bool(render_data.get("css_classes", True)),
        title=bool(render_data.get("title", True)),
    )

    description = data.get("description")
    return TartanSpec(
        name=name,
        sett_type=sett_type,
        colors=colors,
        sett=sett,
        render=render,
        description=str(description) if description is not None else None,
    )
