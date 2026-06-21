from typer.testing import CliRunner

from tartan_maker._version import __version__
from tartan_maker.cli import app


def test_top_level_help_is_plain_click_style():
    result = CliRunner().invoke(app, ["--help"], color=False)

    assert result.exit_code == 0
    assert "Usage: tartan-maker [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
    assert "╭" not in result.output
    assert "╰" not in result.output
    assert "--install-completion" not in result.output
    assert "--show-completion" not in result.output
    assert "-h, --help" in result.output


def test_command_help_is_plain_click_style():
    result = CliRunner().invoke(app, ["render", "--help"], color=False)

    assert result.exit_code == 0
    assert "Usage: tartan-maker render [OPTIONS] INPUT_FILE" in result.output
    assert "Arguments:" in result.output
    assert "Options:" in result.output
    assert "╭" not in result.output
    assert "╰" not in result.output


def test_version_option():
    result = CliRunner().invoke(app, ["--version"], color=False)

    assert result.exit_code == 0
    assert result.output == f"tartan-maker {__version__}\n"


def test_top_level_help_mentions_version():
    result = CliRunner().invoke(app, ["--help"], color=False)

    assert result.exit_code == 0
    assert "--version" in result.output
