"""``aistrap create`` - generate a new project from a template."""

from __future__ import annotations

import sys
from pathlib import Path

from ..utils import console
from ..utils.errors import TargetDirectoryError
from ..utils.registry import DEFAULT_TEMPLATE, get_template
from ..utils.render import (
    build_context,
    check_destination,
    is_empty_directory,
    render_template,
    validate_project_name,
)
from ..utils.tree import format_tree


def _confirm(question: str) -> bool:
    """Ask a yes/no question. Returns ``False`` when input is not interactive."""
    if not sys.stdin or not sys.stdin.isatty():
        return False
    try:
        answer = input(f"{question} [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        console.echo()
        return False
    return answer in {"y", "yes"}


def run(
    project_name: str,
    template_name: str = DEFAULT_TEMPLATE,
    *,
    directory: Path | None = None,
    force: bool = False,
) -> int:
    """Create ``project_name`` from ``template_name``. Returns an exit code."""
    name = validate_project_name(project_name)
    template = get_template(template_name)

    base = Path(directory) if directory is not None else Path.cwd()
    destination = (base / project_name).expanduser().resolve()

    if destination.is_dir() and not is_empty_directory(destination) and not force:
        console.warn(f"Directory {destination} already exists and is not empty.")
        if _confirm("Write the template into it anyway?"):
            force = True
    check_destination(destination, force=force)

    destination.mkdir(parents=True, exist_ok=True)
    created = render_template(template, destination, build_context(name))
    if not created:
        raise TargetDirectoryError(f"Template {template.name!r} contains no files.")

    console.success(
        f"Created {console.style(name, console.BOLD)} "
        f"from the {console.style(template.name, console.CYAN)} template"
    )
    console.echo()
    console.echo(format_tree(created, name, unicode=console.supports_unicode()))
    console.echo()
    console.echo(f"{len(created)} files written to {destination}")
    console.echo()
    console.heading("Next steps:")
    console.echo(f"  cd {name}")
    console.echo("  python -m venv .venv")
    console.echo(
        r"  .venv\Scripts\activate" if sys.platform == "win32" else "  source .venv/bin/activate"
    )
    console.echo("  pip install -r requirements.txt")
    console.echo("  cp .env.example .env")
    return 0
