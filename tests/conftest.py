"""Shared pytest fixtures."""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Callable

import pytest

from aistrap.cli import main


@pytest.fixture
def run_cli(capsys: pytest.CaptureFixture[str]) -> Callable[..., tuple[int, str, str]]:
    """Run the CLI in-process and return ``(exit_code, stdout, stderr)``."""

    def _run(*args: str) -> tuple[int, str, str]:
        code = main(list(args))
        captured = capsys.readouterr()
        return code, captured.out, captured.err

    return _run


@pytest.fixture
def workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run the test with the current directory set to an empty temp directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def run_installed_cli(
    args: Sequence[str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run the installed ``aistrap`` executable in a subprocess."""
    executable = shutil.which("aistrap")
    command = (
        [executable, *args]
        if executable
        else [
            sys.executable,
            "-m",
            "aistrap",
            *args,
        ]
    )
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=120,
        check=False,
    )
