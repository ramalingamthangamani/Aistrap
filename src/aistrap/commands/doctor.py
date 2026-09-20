"""``aistrap doctor`` - report on the local developer environment."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass

from ..utils import console


@dataclass(frozen=True)
class Check:
    """A single tool the generated projects may benefit from."""

    name: str
    command: list[str]
    required: bool = False
    hint: str = ""


CHECKS: list[Check] = [
    Check("Python", [sys.executable, "--version"], required=True),
    Check(
        "pip",
        [sys.executable, "-m", "pip", "--version"],
        hint="Install with: python -m ensurepip --upgrade",
    ),
    Check("Git", ["git", "--version"], hint="Install from https://git-scm.com"),
    Check(
        "Docker",
        ["docker", "--version"],
        hint="only needed for the Dockerfile in some templates",
    ),
]


def _first_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def probe(check: Check) -> tuple[bool, str]:
    """Run a check and return ``(found, details)``."""
    executable = check.command[0]
    if executable != sys.executable and shutil.which(executable) is None:
        return False, "not found on PATH"
    try:
        result = subprocess.run(
            check.command,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover - rare
        return False, f"could not run ({exc.__class__.__name__})"
    if result.returncode != 0:
        return False, _first_line(result.stderr) or f"exited with {result.returncode}"
    return True, _first_line(result.stdout) or _first_line(result.stderr) or "available"


def run() -> int:
    """Print the environment report. Missing optional tools are not failures."""
    console.heading("Environment check:")
    console.echo()
    width = max(len(check.name) for check in CHECKS)
    missing_required: list[Check] = []
    missing_optional: list[Check] = []

    for check in CHECKS:
        found, details = probe(check)
        label = check.name.ljust(width)
        if found:
            mark = console.style("OK     ", console.GREEN, console.BOLD)
        elif check.required:
            mark = console.style("MISSING", console.RED, console.BOLD)
            missing_required.append(check)
        else:
            mark = console.style("MISSING", console.YELLOW, console.BOLD)
            missing_optional.append(check)
        console.echo(f"  {mark}  {label}  {details}")

    console.echo()
    console.echo(f"Platform: {platform.platform()}")
    console.echo(f"Python:   {sys.executable}")
    console.echo()

    for check in missing_optional:
        console.warn(f"{check.name} is optional{': ' + check.hint if check.hint else ''}")
    if missing_required:
        for check in missing_required:
            console.error(f"{check.name} is required{': ' + check.hint if check.hint else ''}")
        return 1
    if not missing_optional:
        console.success("Everything looks good.")
    else:
        console.success("Core tooling is available.")
    return 0
