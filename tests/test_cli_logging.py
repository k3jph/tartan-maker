import subprocess
import sys


def tartan_stderr(stderr: str) -> str:
    """Return only stderr lines emitted by tartan-maker's logger.

    The execution environment used by ChatGPT may inject unrelated startup
    diagnostics into subprocess stderr. Package tests should assert on the
    package's own logger output, not on host-environment noise.
    """
    return "\n".join(
        line
        for line in stderr.splitlines()
        if "[tartan-maker]" in line
        and (
            "[debug]" in line
            or "[info]" in line
            or "[warning]" in line
            or "[error]" in line
        )
    )


def write_tmp(tmp_path, text):
    path = tmp_path / "tartan.yaml"
    path.write_text(text, encoding="utf-8")
    return path


BIG_REPEAT = """
name: Big Symmetrical
sett_type: symmetrical
colors:
  A: {name: Alpha, color: red}
  B: {name: Beta, color: blue}
sett: "A/100 B108 A/100"
"""


BAD_SYM = """
name: Bad Symmetrical
sett_type: symmetrical
colors:
  A: {name: Alpha, color: red}
  B: {name: Beta, color: blue}
sett: "A/100 B108 A100"
"""


def test_render_quiet_by_default_for_warnings(tmp_path):
    spec = write_tmp(tmp_path, BIG_REPEAT)
    out = tmp_path / "out.svg"
    result = subprocess.run(
        [sys.executable, "-m", "tartan_maker.cli", "render", str(spec), "-o", str(out)],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert tartan_stderr(result.stderr) == ""
    assert out.exists()


def test_render_can_show_warnings(tmp_path):
    spec = write_tmp(tmp_path, BIG_REPEAT)
    out = tmp_path / "out.svg"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tartan_maker.cli",
            "render",
            str(spec),
            "-o",
            str(out),
            "--log-level",
            "warning",
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    logger_output = tartan_stderr(result.stderr)
    assert "[tartan-maker]" in logger_output
    assert "[warning] Visual repeat" in logger_output


def test_render_errors_are_not_duplicated(tmp_path):
    spec = write_tmp(tmp_path, BAD_SYM)
    out = tmp_path / "out.svg"
    result = subprocess.run(
        [sys.executable, "-m", "tartan_maker.cli", "render", str(spec), "-o", str(out)],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    logger_output = tartan_stderr(result.stderr)
    assert logger_output.count("Symmetrical setts must mark the last stripe as a pivot") == 1
    assert "Error: Symmetrical setts" not in logger_output
    assert "[ERROR] Symmetrical setts" not in logger_output
    assert "[tartan-maker]" in logger_output
    assert "[tartan-maker-" not in logger_output
    assert "[error] Symmetrical setts" in logger_output


def test_parse_sett_errors_use_spdlog_not_typer_echo():
    result = subprocess.run(
        [sys.executable, "-m", "tartan_maker.cli", "parse-sett", "A"],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    logger_output = tartan_stderr(result.stderr)
    assert "[tartan-maker]" in logger_output
    assert "[tartan-maker-" not in logger_output
    assert "[error]" in logger_output
    assert "Error:" not in logger_output


def test_color_errors_use_spdlog_not_typer_echo():
    result = subprocess.run(
        [sys.executable, "-m", "tartan_maker.cli", "color", "not-a-real-web-color"],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    logger_output = tartan_stderr(result.stderr)
    assert "[tartan-maker]" in logger_output
    assert "[tartan-maker-" not in logger_output
    assert "[error]" in logger_output
    assert "Error:" not in logger_output


def test_make_logger_reuses_registered_spdlog_logger():
    code = """
from tartan_maker.logging import make_logger
make_logger(level='error').error('first')
make_logger(level='error').error('second')
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    logger_output = tartan_stderr(result.stderr)
    assert "first" in logger_output
    assert "second" in logger_output
    assert logger_output.count("[tartan-maker]") == 2
    assert "[tartan-maker-" not in logger_output
