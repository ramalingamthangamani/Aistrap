"""Discovery of the bundled project templates.

A template is just a directory under ``aistrap/templates`` that
contains a ``template.json`` metadata file and a tree of ``*.tmpl`` files.
Adding a template therefore means adding files - no code changes required.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .errors import TemplateNotFoundError

#: Directory holding the bundled templates.
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

#: Metadata file every template directory must provide.
METADATA_FILENAME = "template.json"

#: Suffix marking a file as a template source file.
TEMPLATE_SUFFIX = ".tmpl"

DEFAULT_TEMPLATE = "python-ai"


@dataclass(frozen=True)
class Template:
    """A bundled project template."""

    name: str
    description: str
    path: Path
    order: int = 100

    def source_files(self) -> list[Path]:
        """Return every ``*.tmpl`` file in the template, sorted for stable output."""
        return sorted(p for p in self.path.rglob("*" + TEMPLATE_SUFFIX) if p.is_file())


def _load_template(directory: Path) -> Template | None:
    """Build a :class:`Template` from ``directory`` or return ``None``."""
    metadata_file = directory / METADATA_FILENAME
    if not metadata_file.is_file():
        return None
    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
    return Template(
        name=directory.name,
        description=metadata.get("description", ""),
        path=directory,
        order=int(metadata.get("order", 100)),
    )


def available_templates() -> list[Template]:
    """Return all bundled templates, ordered for display."""
    if not TEMPLATES_DIR.is_dir():
        return []
    templates = [
        template
        for directory in sorted(TEMPLATES_DIR.iterdir())
        if directory.is_dir()
        for template in [_load_template(directory)]
        if template is not None
    ]
    return sorted(templates, key=lambda t: (t.order, t.name))


def template_names() -> list[str]:
    """Return the names of all bundled templates, ordered for display."""
    return [template.name for template in available_templates()]


def get_template(name: str) -> Template:
    """Return the template called ``name``.

    Raises:
        TemplateNotFoundError: if no template with that name is bundled.
    """
    for template in available_templates():
        if template.name == name:
            return template
    known = ", ".join(template_names()) or "none"
    raise TemplateNotFoundError(f"Unknown template: {name!r}. Available templates: {known}.")
