"""Tests for the top-level CLI: help, version and command dispatch."""

from __future__ import annotations

import pytest

from aistrap import __version__
from aistrap.cli import build_parser, main


def test_help_exits_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0
    output = capsys.readouterr().out
    assert "aistrap" in output
    for command in ("create", "list", "doctor"):
        assert command in output


def test_version_prints_the_package_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_arguments_shows_help(run_cli) -> None:
    code, out, _ = run_cli()
    assert code == 0
    assert "usage: aistrap" in out


def test_unknown_command_is_a_usage_error() -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["nope"])
    assert excinfo.value.code == 2


def test_create_requires_a_project_name() -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["create"])
    assert excinfo.value.code == 2


def test_parser_defaults_to_the_python_ai_template() -> None:
    args = build_parser().parse_args(["create", "demo"])
    assert args.template == "python-ai"
    assert args.force is False
