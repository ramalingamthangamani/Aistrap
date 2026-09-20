"""Generate one example project per template, to look at or experiment with.

Run it from anywhere::

    python examples/generate_examples.py
    python examples/generate_examples.py --output /tmp/demos

The generated projects are written to ``examples/generated/`` by default, which
is git-ignored - they are throwaway output, not files to commit.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from aistrap.cli import main as cli_main
from aistrap.utils.registry import template_names

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "generated"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"where to write the example projects (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="delete the output directory first",
    )
    return parser.parse_args()


def generate(output: Path, clean: bool) -> int:
    """Create one project per template under ``output``."""
    if clean and output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    for template in template_names():
        code = cli_main(
            [
                "create",
                f"example-{template}",
                "--template",
                template,
                "--directory",
                str(output),
                "--force",
            ]
        )
        if code != 0:
            return code
        print()

    print(f"All examples are in {output}")
    return 0


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(generate(arguments.output, arguments.clean))
