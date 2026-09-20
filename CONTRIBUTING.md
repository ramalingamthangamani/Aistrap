# Contributing to aistrap

Thanks for wanting to help. This project is small on purpose, so contributing
should be quick - most changes are a template file, a test, and a line of docs.

New to open source? That is fine. Every step below is spelled out, and a pull
request that is not quite right is still welcome; we will help you finish it.

## 1. Clone the repository

```bash
git clone https://github.com/ramalingamthangamani/Aistrap.git
cd aistrap
```

If you plan to open a pull request, fork the repository on GitHub first and
clone your fork instead.

## 2. Set up a development environment

You need Python 3.9 or newer.

```bash
python -m venv .venv

source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

## 3. Install the dependencies

```bash
pip install -e ".[dev,templates]"
```

- `-e` installs the project in editable mode, so your changes take effect
- `dev` brings in pytest, ruff and `build`.
- `templates` brings in FastAPI and scikit-learn, which the generated projects
  use. Without it, two of the end-to-end tests are skipped.

Check that it worked:

```bash
aistrap --version
aistrap list
```

## 4. Run the tests

```bash
pytest
```

Everything should pass before you start, and before you open a pull request.
Useful variations:

```bash
pytest -k create        # only the create command tests
pytest -x               # stop at the first failure
pytest --cov=aistrap
```

## 5. Check style

```bash
ruff format .           # apply formatting
ruff check . --fix      # fix what can be fixed automatically
ruff check .            # confirm nothing is left
```

CI runs `ruff format --check .` and `ruff check .`, so run them locally first.

## Adding a new template

Templates are plain files on disk - no code changes are needed to register one.

### Step 1: Create the directory

```bash
mkdir -p src/aistrap/templates/my-template
```

Use a short, lowercase, hyphenated name. It becomes the value of `--template`.

### Step 2: Describe it

Create `src/aistrap/templates/my-template/template.json`:

```json
{
  "description": "Short description shown by `aistrap list`",
  "order": 50
}
```

`order` controls where the template appears in the list; lower comes first.

### Step 3: Add the files

Every file in the template must end with `.tmpl`. The suffix is stripped when
the project is generated:

| Template file | Generated file |
| --- | --- |
| `README.md.tmpl` | `README.md` |
| `app/main.py.tmpl` | `app/main.py` |
| `.gitignore.tmpl` | `.gitignore` |
| `data/.gitkeep.tmpl` | `data/.gitkeep` |

The suffix keeps template code from being imported or linted as if it were part
of the CLI, and it makes an empty directory easy to express: add a
`.gitkeep.tmpl` file to it.

Inside any file - and in file and directory names - you can use placeholders:

| Placeholder | Example value |
| --- | --- |
| `{{project_name}}` | `my-rag-app` |
| `{{project_title}}` | `My Rag App` |
| `{{package_name}}` | `my_rag_app` |
| `{{python_version}}` | `3.12` |
| `{{year}}` | `2026` |

Unknown placeholders are left alone, so literal braces are safe.

### Step 4: Follow the template conventions

To stay consistent with the existing templates, include:

- a `README.md.tmpl` that uses `{{project_title}}` and explains how to install,
  run and test the generated project;
- a `requirements.txt.tmpl`;
- a `.gitignore.tmpl` and a `.env.example.tmpl`;
- a `pytest.ini.tmpl` with `pythonpath = .`, so a bare `pytest` works;
- a `tests/` directory with tests that pass immediately;
- code that runs without paid APIs, accounts or large downloads.

The last point matters most: someone should be able to generate your template
and see it work within a minute.

### Step 5: Test it

```bash
aistrap list                                   # your template appears
aistrap create demo --template my-template     # it generates
cd demo && pip install -r requirements.txt && pytest      # it works
```

Then add it to the project's own tests. In `tests/test_create.py`, add an entry
to `EXPECTED_CONTENTS` listing the files your template promises, and in
`tests/test_generated_projects.py` add it to the parametrised list (with an
entry in `OPTIONAL_DEPENDENCIES` if it needs a third-party package).

Finally, document it in the Templates section of `README.md` and add an example
to `examples/`.

## Code style

- Format and lint with ruff; the configuration lives in `pyproject.toml`.
- Keep lines under 100 characters.
- Use type hints on function signatures, and `from __future__ import annotations`
  at the top of each module.
- Write docstrings for modules and public functions. Say what something does and
  why, not how.
- Prefer the standard library. The CLI has no runtime dependencies and we would
  like to keep it that way.
- Keep functions small and name things plainly. A beginner should be able to
  read any file here in a few minutes.

## Pull request expectations

Before opening a pull request:

1. `pytest` passes.
2. `ruff check .` and `ruff format --check .` pass.
3. New behaviour has a test.
4. Documentation is updated if you changed behaviour, added a template, or
   changed a command.
5. `CHANGELOG.md` has an entry under `Unreleased`.

In the pull request description, say what changed and why. If it changes CLI
output, paste the before and after. Small, focused pull requests get reviewed
faster than large ones.

Please keep changes scoped to what you set out to do - unrelated refactoring in
the same pull request makes review harder.

## Reporting bugs and suggesting features

Open an issue. For a bug, include:

- what you ran (the exact command),
- what you expected,
- what happened, including the full error,
- your OS and the output of `aistrap doctor`.

For a feature, describe the problem you are trying to solve. That is usually
more useful than a proposed solution.

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
