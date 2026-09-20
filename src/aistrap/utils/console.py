"""Tiny terminal output helpers.

Colour is opt-out: it is disabled automatically when the output stream is not a
terminal, when ``NO_COLOR`` is set, or when the terminal cannot handle ANSI
escapes. Keeping this in one small module means the commands never have to
think about it.
"""

from __future__ import annotations

import os
import sys
from typing import Final, TextIO

RESET: Final = "\033[0m"
BOLD: Final = "\033[1m"
DIM: Final = "\033[2m"
GREEN: Final = "\033[32m"
YELLOW: Final = "\033[33m"
RED: Final = "\033[31m"
CYAN: Final = "\033[36m"


def _enable_windows_ansi() -> bool:
    """Turn on ANSI escape processing on legacy Windows consoles."""
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        # -11 is STD_OUTPUT_HANDLE, 0x4 is ENABLE_VIRTUAL_TERMINAL_PROCESSING.
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x4))
    except Exception:  # pragma: no cover - depends on the host console
        return False


def color_enabled(stream: TextIO | None = None) -> bool:
    """Return ``True`` when it is safe to write ANSI colour codes."""
    stream = stream or sys.stdout
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return _enable_windows_ansi()


def style(text: str, *codes: str, stream: TextIO | None = None) -> str:
    """Wrap ``text`` in ANSI ``codes`` when colour is available."""
    if not codes or not color_enabled(stream):
        return text
    return f"{''.join(codes)}{text}{RESET}"


def echo(message: str = "", *, stream: TextIO | None = None) -> None:
    """Print ``message`` to stdout (or ``stream``)."""
    print(message, file=stream or sys.stdout)


def success(message: str) -> None:
    echo(f"{style('OK', GREEN, BOLD)} {message}")


def warn(message: str) -> None:
    echo(f"{style('!', YELLOW, BOLD)} {message}")


def error(message: str) -> None:
    """Print an error to stderr."""
    echo(f"{style('x', RED, BOLD)} {message}", stream=sys.stderr)


def heading(message: str) -> None:
    echo(style(message, BOLD))


def supports_unicode(stream: TextIO | None = None) -> bool:
    """Return ``True`` when ``stream`` can encode box-drawing characters.

    Windows consoles often default to a legacy code page, so the CLI falls back
    to plain ASCII output rather than crashing with a ``UnicodeEncodeError``.
    """
    stream = stream or sys.stdout
    encoding = getattr(stream, "encoding", None) or ""
    try:
        "├─└│".encode(encoding)
    except (LookupError, UnicodeEncodeError):
        return False
    return True
