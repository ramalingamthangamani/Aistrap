"""Tests for the ``create`` command and the rendering it performs."""

from __future__ import annotations

import py_compile
from pathlib import Path

import pytest

from aistrap.commands import create
from aistrap.utils.registry import template_names

#: Files and directories each template promises to generate.
EXPECTED_CONTENTS = {
    "python-ai": [
        "app/__init__.py",
        "app/main.py",
        "tests/test_app.py",
        "data/.gitkeep",
        "notebooks/.gitkeep",
        "config/.gitkeep",
        ".env.example",
        ".gitignore",
        "requirements.txt",
        "README.md",
    ],
    "fastapi": [
        "app/__init__.py",
        "app/main.py",
        "app/api/__init__.py",
        "tests/test_app.py",
        "data/.gitkeep",
        "config/.gitkeep",
        ".env.example",
        ".gitignore",
        "requirements.txt",
        "Dockerfile",
        "README.md",
    ],
    "rag": [
        "app/__init__.py",
        "app/main.py",
        "app/ingestion.py",
        "app/retrieval.py",
        "app/config.py",
        "tests/test_app.py",
        "data/.gitkeep",
        "config/.gitkeep",
        "documents/getting-started.md",
        ".env.example",
        ".gitignore",
        "requirements.txt",
        "README.md",
        "Dockerfile",
    ],
    "ml-project": [
        "app/__init__.py",
        "app/train.py",
        "app/predict.py",
        "app/config.py",
        "data/.gitkeep",
        "models/.gitkeep",
        "notebooks/.gitkeep",
        "tests/test_app.py",
        "config/.gitkeep",
        ".env.example",
        ".gitignore",
        "requirements.txt",
        "README.md",
    ],
    "ai-agent": [
        "app/__init__.py",
        "app/agent.py",
        "app/config.py",
        "app/main.py",
        "app/tools.py",
        "tests/test_app.py",
        "config/.gitkeep",
        "data/.gitkeep",
        ".env.example",
        ".gitignore",
        "pytest.ini",
        "requirements.txt",
        "README.md",
    ],
    "ai-fullstack": [
        "app/__init__.py",
        "app/config.py",
        "app/main.py",
        "tests/test_app.py",
        "static/index.html",
        "static/style.css",
        "static/app.js",
        "config/.gitkeep",
        "data/.gitkeep",
        ".env.example",
        ".gitignore",
        "Dockerfile",
        "pytest.ini",
        "requirements.txt",
        "README.md",
    ],
    "mcp-server": [
        "app/__init__.py",
        "app/config.py",
        "app/main.py",
        "app/protocol.py",
        "app/server.py",
        "tests/test_app.py",
        "config/.gitkeep",
        ".env.example",
        ".gitignore",
        "pytest.ini",
        "requirements.txt",
        "README.md",
    ],
    "multimodal": [
        "app/__init__.py",
        "app/config.py",
        "app/main.py",
        "app/vision.py",
        "tests/test_app.py",
        "config/.gitkeep",
        "data/.gitkeep",
        ".env.example",
        ".gitignore",
        "pytest.ini",
        "requirements.txt",
        "README.md",
    ],
    "chat-stream": [
        "app/__init__.py",
        "app/config.py",
        "app/main.py",
        "app/sessions.py",
        "tests/test_app.py",
        "config/.gitkeep",
        ".env.example",
        ".gitignore",
        "Dockerfile",
        "pytest.ini",
        "requirements.txt",
        "README.md",
    ],
    "llm-eval": [
        "app/__init__.py",
        "app/config.py",
        "app/evaluator.py",
        "app/main.py",
        "app/metrics.py",
        "tests/test_app.py",
        "config/.gitkeep",
        "data/golden_dataset.json",
        ".env.example",
        ".gitignore",
        "pytest.ini",
        "requirements.txt",
        "README.md",
    ],
}


def test_create_uses_python_ai_by_default(run_cli, workdir: Path) -> None:
    code, out, _ = run_cli("create", "my-project")
    assert code == 0
    assert "python-ai" in out
    assert (workdir / "my-project" / "app" / "main.py").is_file()
    assert not (workdir / "my-project" / "app" / "api").exists()


def test_create_prints_what_it_created(run_cli, workdir: Path) -> None:
    _, out, _ = run_cli("create", "my-project")
    assert "my-project/" in out
    assert "requirements.txt" in out
    assert "files written to" in out
    assert "Next steps:" in out


@pytest.mark.parametrize("template", sorted(EXPECTED_CONTENTS))
def test_each_template_generates_its_promised_files(run_cli, workdir: Path, template: str) -> None:
    code, _, _ = run_cli("create", "demo", "--template", template)
    assert code == 0
    project = workdir / "demo"
    for relative in EXPECTED_CONTENTS[template]:
        assert (project / relative).exists(), f"{template} is missing {relative}"


@pytest.mark.parametrize("template", sorted(EXPECTED_CONTENTS))
def test_generated_python_files_compile(run_cli, workdir: Path, template: str) -> None:
    run_cli("create", "demo", "--template", template)
    sources = list((workdir / "demo").rglob("*.py"))
    assert sources, f"{template} generated no Python files"
    for source in sources:
        py_compile.compile(str(source), doraise=True)


@pytest.mark.parametrize("template", sorted(EXPECTED_CONTENTS))
def test_generated_readme_uses_the_project_name(run_cli, workdir: Path, template: str) -> None:
    run_cli("create", "weather-bot", "--template", template)
    readme = (workdir / "weather-bot" / "README.md").read_text(encoding="utf-8")
    assert "weather-bot" in readme
    assert "Weather Bot" in readme


@pytest.mark.parametrize("template", sorted(EXPECTED_CONTENTS))
def test_no_placeholders_are_left_behind(run_cli, workdir: Path, template: str) -> None:
    run_cli("create", "demo", "--template", template)
    for path in (workdir / "demo").rglob("*"):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        assert "{{" not in content, f"unrendered placeholder in {path}"
        assert ".tmpl" not in path.name


@pytest.mark.parametrize("template", sorted(template_names()))
def test_generated_requirements_are_not_empty(run_cli, workdir: Path, template: str) -> None:
    run_cli("create", "demo", "--template", template)
    requirements = (workdir / "demo" / "requirements.txt").read_text(encoding="utf-8")
    packages = [
        line for line in requirements.splitlines() if line.strip() and not line.startswith("#")
    ]
    assert packages


def test_create_refuses_a_non_empty_directory(run_cli, workdir: Path) -> None:
    existing = workdir / "taken"
    existing.mkdir()
    (existing / "important.txt").write_text("do not lose me", encoding="utf-8")

    code, _, err = run_cli("create", "taken")
    assert code == 1
    assert "not empty" in err
    assert (existing / "important.txt").read_text(encoding="utf-8") == "do not lose me"
    assert not (existing / "README.md").exists()


def test_force_writes_into_a_non_empty_directory(run_cli, workdir: Path) -> None:
    existing = workdir / "taken"
    existing.mkdir()
    (existing / "important.txt").write_text("keep me", encoding="utf-8")

    code, _, _ = run_cli("create", "taken", "--force")
    assert code == 0
    assert (existing / "README.md").is_file()
    assert (existing / "important.txt").read_text(encoding="utf-8") == "keep me"


def test_create_accepts_an_existing_empty_directory(run_cli, workdir: Path) -> None:
    (workdir / "empty").mkdir()
    code, _, _ = run_cli("create", "empty")
    assert code == 0
    assert (workdir / "empty" / "README.md").is_file()


def test_create_refuses_to_overwrite_a_file(run_cli, workdir: Path) -> None:
    (workdir / "taken").write_text("I am a file", encoding="utf-8")
    code, _, err = run_cli("create", "taken")
    assert code == 1
    assert "not a directory" in err


def test_unknown_template_lists_the_available_ones(run_cli, workdir: Path) -> None:
    code, _, err = run_cli("create", "demo", "--template", "tensorflow")
    assert code == 1
    assert "Unknown template" in err
    assert "python-ai" in err
    assert not (workdir / "demo").exists()


@pytest.mark.parametrize("name", ["", "   ", ".", "..", "bad/name?", "with space"])
def test_invalid_project_names_are_rejected(run_cli, workdir: Path, name: str) -> None:
    code, _, err = run_cli("create", name)
    assert code == 1
    assert err


def test_directory_option_controls_where_the_project_lands(run_cli, workdir: Path) -> None:
    target = workdir / "workspace" / "projects"
    target.mkdir(parents=True)
    code, _, _ = run_cli("create", "nested", "--directory", str(target))
    assert code == 0
    assert (target / "nested" / "README.md").is_file()
    assert not (workdir / "nested").exists()


def test_confirming_interactively_allows_a_non_empty_directory(
    run_cli, workdir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = workdir / "taken"
    existing.mkdir()
    (existing / "important.txt").write_text("keep me", encoding="utf-8")

    monkeypatch.setattr(create, "_confirm", lambda _question: True)
    code, _, _ = run_cli("create", "taken")

    assert code == 0
    assert (existing / "README.md").is_file()
    assert (existing / "important.txt").read_text(encoding="utf-8") == "keep me"


def test_confirm_says_no_when_input_is_not_interactive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Scripts and CI must never be treated as an implicit 'yes'."""

    class NotATerminal:
        def isatty(self) -> bool:
            return False

    monkeypatch.setattr(create.sys, "stdin", NotATerminal())
    assert create._confirm("Overwrite?") is False


@pytest.mark.parametrize(
    ("answer", "expected"), [("y", True), ("yes", True), ("n", False), ("", False)]
)
def test_confirm_reads_the_answer(
    monkeypatch: pytest.MonkeyPatch, answer: str, expected: bool
) -> None:
    class ATerminal:
        def isatty(self) -> bool:
            return True

    monkeypatch.setattr(create.sys, "stdin", ATerminal())
    monkeypatch.setattr("builtins.input", lambda _prompt: answer)
    assert create._confirm("Overwrite?") is expected
