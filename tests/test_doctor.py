"""Tests for the ``doctor`` command."""

from __future__ import annotations

from aistrap.commands import doctor


def test_doctor_reports_on_every_check(run_cli) -> None:
    code, out, _ = run_cli("doctor")
    assert code == 0
    for check in doctor.CHECKS:
        assert check.name in out


def test_doctor_finds_the_running_python() -> None:
    found, details = doctor.probe(doctor.CHECKS[0])
    assert found
    assert "Python" in details


def test_doctor_reports_missing_tools_without_failing(monkeypatch, run_cli) -> None:
    """A missing optional tool must not turn into a non-zero exit code."""
    optional = [check for check in doctor.CHECKS if not check.required]
    monkeypatch.setattr(doctor, "CHECKS", optional)
    monkeypatch.setattr(doctor.shutil, "which", lambda _name: None)

    code, out, _ = run_cli("doctor")
    assert code == 0
    assert "MISSING" in out


def test_doctor_fails_when_a_required_tool_is_missing(monkeypatch, run_cli) -> None:
    required = doctor.Check("Imaginary", ["imaginary-tool", "--version"], required=True)
    monkeypatch.setattr(doctor, "CHECKS", [required])
    monkeypatch.setattr(doctor.shutil, "which", lambda _name: None)

    code, _, err = run_cli("doctor")
    assert code == 1
    assert "Imaginary" in err
