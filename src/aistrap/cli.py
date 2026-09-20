"""Command line entry point for aistrap."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .commands import create as create_cmd
from .commands import doctor as doctor_cmd
from .commands import list as list_cmd
from .utils import console
from .utils.errors import AistrapError
from .utils.registry import DEFAULT_TEMPLATE, template_names

PROGRAM = "aistrap"

DESCRIPTION = "Generate clean, ready-to-use AI/ML project structures from templates."

EPILOG = f"""examples:
  {PROGRAM} create my-ai-app
  {PROGRAM} create my-rag-app --template rag
  {PROGRAM} list
  {PROGRAM} doctor
"""


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the whole CLI."""
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{PROGRAM} {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="command")

    known = ", ".join(template_names()) or "none"
    create = subparsers.add_parser(
        "create",
        help="create a new project from a template",
        description="Create a new project directory from a bundled template.",
    )
    create.add_argument("name", help="name of the project (also the directory name)")
    create.add_argument(
        "-t",
        "--template",
        default=DEFAULT_TEMPLATE,
        metavar="NAME",
        help=f"template to use (default: {DEFAULT_TEMPLATE}; available: {known})",
    )
    create.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=None,
        metavar="PATH",
        help="parent directory to create the project in (default: current directory)",
    )
    create.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="write into an existing non-empty directory without asking",
    )

    subparsers.add_parser(
        "list",
        help="list the available templates",
        description="List the templates bundled with this installation.",
    )
    subparsers.add_parser(
        "doctor",
        help="check the local development environment",
        description="Check for tools that are useful when working on AI projects.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI. Returns the process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "create":
            return create_cmd.run(
                args.name,
                args.template,
                directory=args.directory,
                force=args.force,
            )
        if args.command == "list":
            return list_cmd.run()
        if args.command == "doctor":
            return doctor_cmd.run()
    except AistrapError as exc:
        console.error(str(exc))
        return 1
    except KeyboardInterrupt:  # pragma: no cover - interactive only
        console.error("Cancelled.")
        return 130

    parser.error(f"unknown command: {args.command}")  # pragma: no cover - unreachable
    return 2


def run() -> None:
    """Console-script entry point."""
    sys.exit(main())


if __name__ == "__main__":  # pragma: no cover
    run()
