"""Command-line interface for tartan-maker."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
import yaml

from .colors import normalize_color
from .errors import TartanMakerError
from .inspect import inspect_spec
from .logging import make_logger
from .render_png import write_png
from .render_svg import write_svg
from .sett import parse_sett_string, stripes_to_yaml_pairs
from .spec import load_spec
from .srt import to_srt_block, to_srt_pallet, to_srt_threadcount
from .validate import raise_for_errors, validate_spec

app = typer.Typer(no_args_is_help=True)


def _logger(log_level: str, log_backend: str, log_file: Optional[Path]):
    return make_logger(
        backend=log_backend,
        level=log_level,
        log_file=str(log_file) if log_file else None,
    )


def _load_validated(path: Path, *, log_level: str, log_backend: str, log_file: Optional[Path]):
    logger = _logger(log_level, log_backend, log_file)
    logger.info(f"Reading tartan spec: {path}")
    spec = load_spec(path)
    issues = validate_spec(spec)
    for issue in issues:
        getattr(logger, issue.severity)(issue.message)
    raise_for_errors(issues)
    return spec


@app.command()
def render(
    input_file: Path = typer.Argument(..., exists=True, readable=True),
    output: Path = typer.Option(..., "-o", "--output"),
    fmt: str | None = typer.Option(None, "--format", help="svg or png. Defaults to output extension."),
    size: int | None = typer.Option(None, "--size"),
    weave: bool | None = typer.Option(None, "--weave/--no-weave"),
    css_classes: bool | None = typer.Option(None, "--css-classes/--inline-colors"),
    png_width: int | None = typer.Option(None, "--png-width"),
    png_height: int | None = typer.Option(None, "--png-height"),
    png_scale: float | None = typer.Option(None, "--png-scale"),
    log_level: str = typer.Option("warning", "--log-level"),
    log_backend: str = typer.Option("auto", "--log-backend"),
    log_file: Path | None = typer.Option(None, "--log-file"),
) -> None:
    """Render a tartan to SVG or PNG."""
    try:
        spec = _load_validated(input_file, log_level=log_level, log_backend=log_backend, log_file=log_file)
        if size is not None or weave is not None or css_classes is not None:
            from dataclasses import replace
            from .model import RenderOptions
            spec = replace(
                spec,
                render=RenderOptions(
                    size=size if size is not None else spec.render.size,
                    weave=weave if weave is not None else spec.render.weave,
                    preserve_aspect_ratio=spec.render.preserve_aspect_ratio,
                    css_classes=css_classes if css_classes is not None else spec.render.css_classes,
                    title=spec.render.title,
                ),
            )
        chosen = (fmt or output.suffix.removeprefix(".") or "svg").lower()
        if chosen == "svg":
            write_svg(spec, output)
        elif chosen == "png":
            write_png(spec, output, output_width=png_width, output_height=png_height, scale=png_scale)
        else:
            raise typer.BadParameter("Format must be svg or png")
    except TartanMakerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command()
def srt(
    input_file: Path = typer.Argument(..., exists=True, readable=True),
    output: Path | None = typer.Option(None, "-o", "--output"),
    rotate_asymmetrical: bool = typer.Option(False, "--rotate-asymmetrical"),
    pallet_only: bool = typer.Option(False, "--pallet-only"),
    threadcount_only: bool = typer.Option(False, "--threadcount-only"),
    log_level: str = typer.Option("warning", "--log-level"),
    log_backend: str = typer.Option("auto", "--log-backend"),
    log_file: Path | None = typer.Option(None, "--log-file"),
) -> None:
    """Generate SRT-compatible pallet and threadcount fields."""
    try:
        spec = _load_validated(input_file, log_level=log_level, log_backend=log_backend, log_file=log_file)
        if pallet_only and threadcount_only:
            raise typer.BadParameter("Use at most one of --pallet-only or --threadcount-only")
        if pallet_only:
            text = to_srt_pallet(spec)
        elif threadcount_only:
            text = to_srt_threadcount(spec, rotate_asymmetrical=rotate_asymmetrical)
        else:
            text = to_srt_block(spec, rotate_asymmetrical=rotate_asymmetrical)
        if output:
            output.write_text(text + "\n", encoding="utf-8")
        else:
            typer.echo(text)
    except TartanMakerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command()
def inspect(
    input_file: Path = typer.Argument(..., exists=True, readable=True),
) -> None:
    """Inspect and validate a tartan spec."""
    try:
        typer.echo(inspect_spec(load_spec(input_file)))
    except TartanMakerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command("parse-sett")
def parse_sett(value: str) -> None:
    """Parse compact sett notation and print YAML pair form."""
    try:
        rows = stripes_to_yaml_pairs(parse_sett_string(value))
        typer.echo(yaml.safe_dump({"sett": rows}, sort_keys=False).rstrip())
    except TartanMakerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command("color")
def color_command(value: str) -> None:
    """Resolve a web color name or hex value to #RRGGBB."""
    try:
        typer.echo(normalize_color(value))
    except TartanMakerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command()
def normalize(
    input_file: Path = typer.Argument(..., exists=True, readable=True),
    output: Path | None = typer.Option(None, "-o", "--output"),
) -> None:
    """Print a normalized YAML view of a tartan spec."""
    try:
        spec = load_spec(input_file)
        data = {
            "name": spec.name,
            "sett_type": spec.sett_type.value,
            "colors": {
                code: {
                    "name": color.name,
                    "color": color.source,
                    "hex": color.hex,
                    "srt": {"code": color.srt_display_code, "name": color.srt_display_name},
                }
                for code, color in spec.colors.items()
            },
            "sett": stripes_to_yaml_pairs(spec.sett),
            "render": {
                "size": spec.render.size,
                "weave": spec.render.weave,
                "preserve_aspect_ratio": spec.render.preserve_aspect_ratio,
                "css_classes": spec.render.css_classes,
            },
        }
        text = yaml.safe_dump(data, sort_keys=False)
        if output:
            output.write_text(text, encoding="utf-8")
        else:
            typer.echo(text.rstrip())
    except TartanMakerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1) from exc

if __name__ == "__main__":
    app()
