"""End-to-end tests: generate a project, then run its own test suite.

The ``python-ai`` and ``rag`` templates only need the standard library, so they
always run here. The other two are exercised when their dependencies happen to
be installed.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

from aistrap.cli import main

#: template name -> module that must be importable for its tests to run.
OPTIONAL_DEPENDENCIES = {"fastapi": "fastapi", "ml-project": "sklearn"}


def generate(template: str, destination: Path) -> Path:
    """Create a project from ``template`` inside ``destination``."""
    assert main(["create", "demo", "--template", template, "--directory", str(destination)]) == 0
    return destination / "demo"


def run_pytest(project: Path) -> subprocess.CompletedProcess[str]:
    """Run the generated project's test suite in a subprocess."""
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )


@pytest.mark.parametrize("template", ["python-ai", "fastapi", "rag", "ml-project"])
def test_generated_project_tests_pass(tmp_path: Path, template: str) -> None:
    dependency = OPTIONAL_DEPENDENCIES.get(template)
    if dependency and importlib.util.find_spec(dependency) is None:
        pytest.skip(f"{dependency} is not installed")

    result = run_pytest(generate(template, tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("template", ["python-ai", "rag"])
def test_generated_project_runs_from_any_directory(tmp_path: Path, template: str) -> None:
    """``python -m app.main`` must work regardless of the current directory."""
    project = generate(template, tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "app.main"],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
        env={**os.environ, "PYTHONPATH": str(project)},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip()
