"""Tests that exercise the installed ``aistrap`` executable.

These run the real console script in a subprocess, so they catch packaging
problems - a missing entry point or templates that were not shipped - that
in-process tests cannot see.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from aistrap import __version__

from .conftest import run_installed_cli


def test_installed_cli_reports_its_version() -> None:
    result = run_installed_cli(["--version"])
    assert result.returncode == 0
    assert __version__ in result.stdout


def test_installed_cli_shows_help() -> None:
    result = run_installed_cli(["--help"])
    assert result.returncode == 0
    assert "usage: aistrap" in result.stdout


def test_installed_cli_lists_templates() -> None:
    result = run_installed_cli(["list"])
    assert result.returncode == 0
    for name in ("python-ai", "fastapi", "rag", "ml-project"):
        assert name in result.stdout


def test_installed_cli_doctor_succeeds() -> None:
    result = run_installed_cli(["doctor"])
    assert result.returncode == 0
    assert "Python" in result.stdout


@pytest.mark.parametrize("template", ["python-ai", "fastapi", "rag", "ml-project"])
def test_installed_cli_creates_a_project(tmp_path: Path, template: str) -> None:
    result = run_installed_cli(["create", "demo", "--template", template], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "demo" / "README.md").is_file()
    assert (tmp_path / "demo" / "requirements.txt").is_file()


def test_installed_cli_rejects_an_unknown_template(tmp_path: Path) -> None:
    result = run_installed_cli(["create", "demo", "--template", "nope"], cwd=tmp_path)
    assert result.returncode == 1
    assert "Unknown template" in result.stderr
