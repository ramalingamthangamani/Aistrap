# AGENTS.md

Guidance for AI coding agents working in this repository. Humans should read
[CONTRIBUTING.md](CONTRIBUTING.md) instead - it covers the same ground in more
detail.

## What this project is

A command line tool that generates AI/ML project structures from templates. It
has no runtime dependencies and deliberately stays small. The generated projects
must run correctly the moment they are created.

## Architecture

```
src/aistrap/
├── cli.py              # argparse parser, dispatch, error handling, exit codes
├── __main__.py         # enables `python -m aistrap`
├── commands/
│   ├── create.py       # generate a project from a template
│   ├── list.py         # show the available templates
│   └── doctor.py       # report on Python, pip, Git, Docker
├── templates/          # DATA, not code: one directory per template
└── utils/
    ├── console.py      # output helpers, colour and unicode detection
    ├── errors.py       # exceptions that become friendly CLI messages
    ├── registry.py     # template discovery from template.json
    ├── render.py       # placeholder substitution, destination safety checks
    └── tree.py         # ASCII/unicode tree of created files
```

The flow of `create` is: `cli.main` parses arguments -> `commands.create.run`
validates the name and destination -> `utils.registry.get_template` finds the
template -> `utils.render.render_template` writes the files -> `utils.tree`
prints what happened.

## Important directories

- `src/aistrap/templates/` - the templates. Every file ends in
  `.tmpl`; the suffix is stripped at generation time. These files are **not**
  importable modules, and ruff is configured to ignore them. Do not "fix" them
  as if they were part of the CLI.
- `tests/` - the project's own test suite.
- `examples/` - documented example output. Do not paste whole generated projects
  here; the examples reference the templates instead.

## How to run the tests

```bash
pip install -e ".[dev,templates]"
pytest
ruff check .
ruff format --check .
```

`pytest` must pass before you report a change as complete. This is not optional:
the suite generates every template and runs the generated projects' own tests,
so it is the only reliable signal that a template change is correct.

If you changed a template, also verify it by hand:

```bash
aistrap create demo --template <name> --directory /tmp/check
cd /tmp/check/demo && pip install -r requirements.txt && pytest
```

## How to add a template

1. Create `src/aistrap/templates/<name>/`.
2. Add `template.json` with a `description` and an `order`.
3. Add the template files, each ending in `.tmpl`. Use `.gitkeep.tmpl` for
   otherwise-empty directories.
4. Include `README.md.tmpl`, `requirements.txt.tmpl`, `.gitignore.tmpl`,
   `.env.example.tmpl`, `pytest.ini.tmpl` and a passing `tests/` suite.
5. Register it in `tests/test_create.py` (`EXPECTED_CONTENTS`) and
   `tests/test_generated_projects.py`.
6. Document it in `README.md` and `examples/README.md`.

No code changes are needed to register a template - discovery is by directory.

Placeholders available in file contents and in file names: `{{project_name}}`,
`{{project_title}}`, `{{package_name}}`, `{{python_version}}`, `{{year}}`.

## Coding conventions

- Python 3.9 compatible. Start every module with `from __future__ import annotations`.
- Type hints on function signatures.
- Docstrings on modules and public functions, explaining what and why.
- Standard library only in `src/aistrap/`. Do not add a runtime
  dependency; if you think one is unavoidable, say so and stop rather than
  adding it.
- Line length 100. Format with `ruff format`.
- User-facing output goes through `utils/console.py`. Errors go to stderr, never
  stdout. Raise `AistrapError` subclasses for expected failures - the
  CLI turns them into a clean message and exit code 1, with no traceback.
- Keep output ASCII-safe unless `console.supports_unicode()` says otherwise;
  Windows consoles crash on box-drawing characters in legacy code pages.
- Generated code must not use absolute paths. Templates that read files resolve
  them relative to the project root (see `app/config.py` in the `rag` and
  `ml-project` templates), so the project works from any directory.

## Documentation requirements

A change is not finished until the docs match it:

- New or changed command or flag: update `README.md` (CLI commands section) and
  the `--help` text.
- New template: update `README.md`, `examples/README.md` and `CONTRIBUTING.md`
  if the template conventions changed.
- Any user-visible change: add an entry to `CHANGELOG.md` under `Unreleased`.

Never claim adoption numbers, download counts, benchmarks, stars or users in the
documentation, and do not invent URLs for homepages, docs sites or badges. The
repository URLs in `pyproject.toml` are placeholders to be filled in by the
maintainer.

## Rules against unnecessary work

- Do not refactor code you were not asked to change. Unrelated cleanup makes
  review harder and is usually rejected.
- Do not rename files, reorganise the package, or change public function
  signatures unless that is the task.
- Do not add dependencies, plugin systems, configuration frameworks, caching
  layers, async, or abstraction "for the future". This project values being
  small and obvious over being extensible in the abstract.
- Do not add API integrations, authentication, databases or cloud
  infrastructure. The templates are starting points; users add those themselves.
- Do not reformat whole files you barely touched.
- Do not leave `TODO` or `FIXME` in working code paths. Either implement it or
  leave the code honest about what it does.

## Before you report a change as complete

1. `pytest` passes.
2. `ruff check .` and `ruff format --check .` pass.
3. New behaviour has a test.
4. Documentation and `CHANGELOG.md` are updated.
5. If you touched templates, you generated the project and ran it.
6. You state plainly what you changed, what you verified, and anything you did
   not verify.
