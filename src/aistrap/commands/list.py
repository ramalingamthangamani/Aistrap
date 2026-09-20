"""``aistrap list`` - show the bundled templates."""

from __future__ import annotations

from ..utils import console
from ..utils.registry import DEFAULT_TEMPLATE, available_templates


def run() -> int:
    """Print every available template with its description."""
    templates = available_templates()
    if not templates:
        console.warn("No templates are bundled with this installation.")
        return 1

    console.heading("Available templates:")
    console.echo()
    width = max(len(template.name) for template in templates)
    for template in templates:
        name = console.style(template.name.ljust(width), console.CYAN)
        default = " (default)" if template.name == DEFAULT_TEMPLATE else ""
        console.echo(f"  {name}  {template.description}{default}")
    console.echo()
    console.echo("Create a project with:")
    console.echo(f"  aistrap create my-project --template {templates[0].name}")
    return 0
