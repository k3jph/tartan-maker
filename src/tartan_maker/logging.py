"""Logging facade backed by spdlog."""

from __future__ import annotations

from typing import Any, Protocol

import spdlog  # type: ignore[import-not-found]


class Logger(Protocol):
    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...


LOGGER_NAME = "tartan-maker"
_LOGGERS: dict[str, Any] = {}

_LEVELS = {
    "trace": spdlog.LogLevel.TRACE,
    "debug": spdlog.LogLevel.DEBUG,
    "info": spdlog.LogLevel.INFO,
    "warning": spdlog.LogLevel.WARN,
    "warn": spdlog.LogLevel.WARN,
    "error": spdlog.LogLevel.ERR,
    "critical": spdlog.LogLevel.CRITICAL,
    "off": spdlog.LogLevel.OFF,
}


class SpdlogLogger:
    """Tiny adapter around spdlog's Python bindings."""

    def __init__(self, logger: Any) -> None:
        self._logger = logger

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warn(message)

    def error(self, message: str) -> None:
        self._logger.error(message)


def _normalize_level(level: str) -> int:
    normalized = level.lower()
    try:
        return _LEVELS[normalized]
    except KeyError as exc:
        valid = ", ".join(key for key in _LEVELS if key != "warn")
        raise ValueError(f"Invalid log level {level!r}; expected one of: {valid}") from exc


def _registered_logger(name: str) -> Any | None:
    """Return an existing spdlog logger without creating a suffixed duplicate."""
    if name in _LOGGERS:
        return _LOGGERS[name]

    get_logger = getattr(spdlog, "get", None)
    if get_logger is None:
        return None
    try:
        logger = get_logger(name)
    except Exception:
        return None
    if logger is not None:
        _LOGGERS[name] = logger
    return logger


def _create_logger(name: str, log_file: str | None) -> Any:
    if log_file:
        return spdlog.FileLogger(name, log_file)
    return spdlog.ConsoleLogger(name, False, False, False)


def make_logger(
    name: str = LOGGER_NAME,
    *,
    level: str = "warning",
    log_file: str | None = None,
) -> Logger:
    """Return a process-global spdlog-backed logger.

    The spdlog registry requires logger names to be unique. Reusing the
    registered logger prevents output such as ``[tartan-maker-1]`` when CLI
    code asks for the logger more than once in the same process.
    """
    logger = _registered_logger(name)
    if logger is None:
        logger = _create_logger(name, log_file)
        _LOGGERS[name] = logger
    logger.set_level(_normalize_level(level))
    return SpdlogLogger(logger)
