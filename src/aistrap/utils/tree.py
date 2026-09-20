"""Render a list of relative paths as an ASCII tree."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

_BRANCH = "|-- "
_LAST_BRANCH = "`-- "
_PIPE = "|   "
_SPACE = "    "

_UNICODE = {_BRANCH: "├── ", _LAST_BRANCH: "└── ", _PIPE: "│   "}


def _build(paths: list[PurePosixPath]) -> dict[str, dict]:
    """Group flat paths into a nested ``{name: children}`` mapping."""
    tree: dict[str, dict] = {}
    for path in paths:
        node = tree
        for part in path.parts:
            node = node.setdefault(part, {})
    return tree


def _lines(node: dict[str, dict], prefix: str) -> list[str]:
    lines: list[str] = []
    entries = sorted(node.items(), key=lambda item: (not item[1], item[0].lower()))
    for index, (name, children) in enumerate(entries):
        last = index == len(entries) - 1
        connector = _LAST_BRANCH if last else _BRANCH
        suffix = "/" if children else ""
        lines.append(f"{prefix}{connector}{name}{suffix}")
        if children:
            lines.extend(_lines(children, prefix + (_SPACE if last else _PIPE)))
    return lines


def format_tree(paths: list[Path] | list[PurePosixPath], root: str, *, unicode: bool = True) -> str:
    """Return an ASCII/Unicode tree for ``paths`` under a ``root`` label."""
    normalised = [PurePosixPath(Path(path).as_posix()) for path in paths]
    rendered = "\n".join([f"{root}/", *_lines(_build(normalised), "")])
    if unicode:
        for plain, fancy in _UNICODE.items():
            rendered = rendered.replace(plain, fancy)
    return rendered
