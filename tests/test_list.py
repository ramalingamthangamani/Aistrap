"""Tests for the ``list`` command and the template registry."""

from __future__ import annotations

import pytest

from aistrap.utils.errors import TemplateNotFoundError
from aistrap.utils.registry import (
    DEFAULT_TEMPLATE,
    available_templates,
    get_template,
    template_names,
)

EXPECTED_TEMPLATES = {
    "python-ai",
    "fastapi",
    "rag",
    "ml-project",
    "ai-agent",
    "ai-fullstack",
    "mcp-server",
    "multimodal",
    "chat-stream",
    "llm-eval",
}


def test_list_shows_every_template(run_cli) -> None:
    code, out, _ = run_cli("list")
    assert code == 0
    assert "Available templates:" in out
    for name in EXPECTED_TEMPLATES:
        assert name in out


def test_list_shows_a_description_for_each_template(run_cli) -> None:
    _, out, _ = run_cli("list")
    for template in available_templates():
        assert template.description in out


def test_default_template_is_available() -> None:
    assert DEFAULT_TEMPLATE in template_names()


def test_all_expected_templates_are_bundled() -> None:
    assert EXPECTED_TEMPLATES.issubset(set(template_names()))


def test_every_template_has_a_description_and_files() -> None:
    for template in available_templates():
        assert template.description, f"{template.name} has no description"
        assert template.source_files(), f"{template.name} has no files"


def test_get_template_rejects_unknown_names() -> None:
    with pytest.raises(TemplateNotFoundError) as excinfo:
        get_template("does-not-exist")
    assert "does-not-exist" in str(excinfo.value)
