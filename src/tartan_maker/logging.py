"""Small logging facade with optional spdlog backend."""

from __future__ import annotations

import logging as py_logging
import sys
from typing import Protocol


class Logger(Protocol):
    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...


class NullLogger:
    def debug(self, message: str) -> None: pass
    def info(self, message: str) -> None: pass
    def warning(self, message: str) -> None: pass
    def error(self, message: str) -> None: pass


def make_python_logger(name: str, *, level: str, log_file: str | None) -> Logger:
    logger = py_logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(getattr(py_logging, level.upper()))
    handler: py_logging.Handler
    if log_file:
        handler = py_logging.FileHandler(log_file)
    else:
        handler = py_logging.StreamHandler(sys.stderr)
    handler.setFormatter(py_logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger


def make_spdlog_logger(name: str, *, level: str, log_file: str | None) -> Logger:
    # The exact Python wrapper API can vary; keep it isolated here.
    import spdlog  # type: ignore[import-not-found]

    if log_file:
        logger = spdlog.FileLogger(name, log_file)
    else:
        logger = spdlog.ConsoleLogger(name)
    if hasattr(logger, "set_level"):
        logger.set_level(level)
    return logger


def make_logger(
    name: str = "tartan-maker",
    *,
    backend: str = "auto",
    level: str = "warning",
    log_file: str | None = None,
) -> Logger:
    """Create a logger using Python logging or optional spdlog."""
    backend = backend.lower()
    if backend == "none":
        return NullLogger()
    if backend in {"auto", "spdlog"}:
        try:
            return make_spdlog_logger(name, level=level, log_file=log_file)
        except Exception:
            if backend == "spdlog":
                raise
    return make_python_logger(name, level=level, log_file=log_file)
