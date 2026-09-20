"""Tests for the small helper modules."""

from __future__ import annotations

from pathlib import Path

import pytest

from aistrap.utils.errors import TargetDirectoryError
from aistrap.utils.render import (
    build_context,
    check_destination,
    is_empty_directory,
    package_name_for,
    render_text,
    validate_project_name,
)
from aistrap.utils.tree import format_tree


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        ("my-rag-app", "my_rag_app"),
        ("My Project", "my_project"),
        ("weather.bot", "weather_bot"),
        ("2fast", "app_2fast"),
    ],
)
def test_package_name_for(project: str, expected: str) -> None:
    assert package_name_for(project) == expected


def test_render_text_replaces_known_placeholders() -> None:
    context = {"project_name": "demo"}
    assert render_text("# {{project_name}}", context) == "# demo"
    assert render_text("# {{ project_name }}", context) == "# demo"


def test_render_text_leaves_unknown_placeholders_alone() -> None:
    assert render_text("{{unknown}}", {"project_name": "demo"}) == "{{unknown}}"


def test_build_context_has_the_documented_keys() -> None:
    context = build_context("my-rag-app")
    assert context["project_name"] == "my-rag-app"
    assert context["package_name"] == "my_rag_app"
    assert context["project_title"] == "My Rag App"
    assert context["year"].isdigit()


def test_validate_project_name_returns_the_final_component() -> None:
    assert validate_project_name("demo") == "demo"
    assert validate_project_name(str(Path("nested") / "demo")) == "demo"


@pytest.mark.parametrize("name", ["", "  ", ".", "..", "no*stars"])
def test_validate_project_name_rejects_bad_names(name: str) -> None:
    with pytest.raises(TargetDirectoryError):
        validate_project_name(name)


def test_is_empty_directory(tmp_path: Path) -> None:
    assert is_empty_directory(tmp_path)
    (tmp_path / "file.txt").write_text("x", encoding="utf-8")
    assert not is_empty_directory(tmp_path)


def test_check_destination_allows_new_and_empty_directories(tmp_path: Path) -> None:
    check_destination(tmp_path / "new", force=False)
    check_destination(tmp_path, force=False)


def test_check_destination_blocks_non_empty_directories(tmp_path: Path) -> None:
    (tmp_path / "file.txt").write_text("x", encoding="utf-8")
    with pytest.raises(TargetDirectoryError):
        check_destination(tmp_path, force=False)
    check_destination(tmp_path, force=True)


def test_format_tree_nests_directories() -> None:
    rendered = format_tree(
        [Path("app/main.py"), Path("app/__init__.py"), Path("README.md")],
        "demo",
        unicode=False,
    )
    assert rendered.splitlines()[0] == "demo/"
    assert "|-- app/" in rendered
    assert "`-- README.md" in rendered


def test_format_tree_handles_a_single_file() -> None:
    assert format_tree([Path("README.md")], "demo", unicode=False) == "demo/\n`-- README.md"
