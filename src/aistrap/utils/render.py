"""Rendering a bundled template into a real project directory.

The "template language" is deliberately tiny: ``{{ variable }}`` placeholders
are replaced with values from a context dictionary. That keeps the tool
dependency-free and makes templates obvious to read and edit.
"""

from __future__ import annotations

import datetime as _datetime
import re
import sys
from pathlib import Path

from .errors import TargetDirectoryError
from .registry import TEMPLATE_SUFFIX, Template

_PLACEHOLDER = re.compile(r"\{\{\s*(\w+)\s*\}\}")
_INVALID_NAME_CHARS = re.compile(r"[^A-Za-z0-9._-]")


def package_name_for(project_name: str) -> str:
    """Turn a project name into a valid Python package/module name."""
    candidate = re.sub(r"[^0-9a-zA-Z]+", "_", project_name).strip("_").lower()
    if not candidate or candidate[0].isdigit():
        candidate = f"app_{candidate}".rstrip("_")
    return candidate


def validate_project_name(name: str) -> str:
    """Validate the final path component of ``name`` and return it.

    Raises:
        TargetDirectoryError: if the name cannot be used as a directory name.
    """
    cleaned = name.strip().rstrip("/\\")
    if not cleaned:
        raise TargetDirectoryError("Project name must not be empty.")
    final = Path(cleaned).name
    if final in {"", ".", ".."}:
        raise TargetDirectoryError(f"Invalid project name: {name!r}.")
    if _INVALID_NAME_CHARS.search(final):
        raise TargetDirectoryError(
            f"Invalid project name: {name!r}. Use letters, digits, '.', '-' and '_'."
        )
    return final


def build_context(project_name: str) -> dict[str, str]:
    """Build the placeholder values available to every template file."""
    return {
        "project_name": project_name,
        "package_name": package_name_for(project_name),
        "project_title": project_name.replace("_", " ").replace("-", " ").title(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "year": str(_datetime.date.today().year),
    }


def render_text(text: str, context: dict[str, str]) -> str:
    """Replace every known ``{{ placeholder }}`` in ``text``.

    Unknown placeholders are left untouched so that template files can contain
    literal braces (for example in generated JSON or shell snippets).
    """

    def _replace(match: re.Match[str]) -> str:
        return context.get(match.group(1), match.group(0))

    return _PLACEHOLDER.sub(_replace, text)


def is_empty_directory(path: Path) -> bool:
    """Return ``True`` when ``path`` is a directory containing nothing."""
    return path.is_dir() and not any(path.iterdir())


def check_destination(destination: Path, *, force: bool) -> None:
    """Make sure ``destination`` can be written to.

    Raises:
        TargetDirectoryError: if the path is a file, or a non-empty directory
            and ``force`` is not set.
    """
    if destination.exists() and not destination.is_dir():
        raise TargetDirectoryError(f"{destination} already exists and is not a directory.")
    if destination.is_dir() and not is_empty_directory(destination) and not force:
        raise TargetDirectoryError(
            f"Directory {destination} already exists and is not empty. "
            "Re-run with --force to write into it anyway."
        )


def render_template(template: Template, destination: Path, context: dict[str, str]) -> list[Path]:
    """Render ``template`` into ``destination``.

    Returns the created paths, relative to ``destination`` and sorted.
    """
    created: list[Path] = []
    for source in template.source_files():
        relative = source.relative_to(template.path)
        target_relative = relative.with_name(relative.name[: -len(TEMPLATE_SUFFIX)])
        target = destination / Path(render_text(str(target_relative), context))
        target.parent.mkdir(parents=True, exist_ok=True)
        rendered = render_text(source.read_text(encoding="utf-8"), context)
        target.write_bytes(rendered.encode("utf-8"))
        created.append(target.relative_to(destination))
    return sorted(created)
