# aistrap

A small command line tool that generates clean, ready-to-use AI/ML project
structures from templates.

```bash
aistrap create my-rag-app --template rag
cd my-rag-app
```

You get a project that runs immediately: source layout, tests, configuration,
`.env.example`, `.gitignore`, `requirements.txt` and a README that already knows
your project's name.

## Why this project exists

Starting a new AI project means making the same decisions again and again:
where does the source go, how are settings loaded, where do datasets live, how
do the tests find the code. Copying the last project's folders usually drags
along things you no longer need.

`aistrap` gives you a sensible starting point in one command. The
templates are deliberately small - you are meant to read them, understand every
file in a couple of minutes, and then replace the parts you disagree with.

## Features

- **Four templates** covering plain Python AI projects, FastAPI backends,
  retrieval-augmented generation and scikit-learn workflows.
- **Generated projects actually run.** Every template ships working code and a
  passing test suite - no stubs to fill in before you can check that it works.
- **No paid APIs, no accounts.** The RAG template retrieves with
  standard-library TF-IDF; the ML template trains on a bundled dataset.
- **No runtime dependencies.** The CLI itself uses only the standard library.
- **Safe by default.** It refuses to write into a non-empty directory unless you
  confirm or pass `--force`.
- **An environment check** (`doctor`) that tells you what is installed without
  failing because an optional tool is missing.

## Installation

```bash
pip install aistrap
```

Or install from source:

```bash
git clone https://github.com/ramalingamthangamani/Aistrap.git
cd aistrap
pip install .
```

Requires Python 3.9 or newer.

## Quick start

```bash
# See what is available
aistrap list

# Create a project (defaults to the python-ai template)
aistrap create my-ai-app

# Or pick a template
aistrap create my-rag-app --template rag

cd my-rag-app
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m app.main "What is retrieval-augmented generation?"
```

## CLI commands

### `create`

```bash
aistrap create NAME [--template NAME] [--directory PATH] [--force]
```

| Option | Description |
| --- | --- |
| `-t`, `--template` | Template to use. Defaults to `python-ai`. |
| `-d`, `--directory` | Parent directory to create the project in. Defaults to the current directory. |
| `-f`, `--force` | Write into an existing non-empty directory without asking. |

If the target directory exists and is not empty, the command asks for
confirmation. When it is not running interactively it stops instead, so nothing
is overwritten by accident in a script.

```console
$ aistrap create my-rag-app --template rag
OK Created my-rag-app from the rag template

my-rag-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── main.py
│   └── retrieval.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── documents/
│   └── getting-started.md
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt

15 files written to /home/you/my-rag-app

Next steps:
  cd my-rag-app
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env
```

### `list`

```console
$ aistrap list
Available templates:

  python-ai   Basic Python AI project (default)
  fastapi     FastAPI AI backend
  rag         Retrieval-Augmented Generation project
  ml-project  Machine learning project
```

### `doctor`

Checks for Python, pip, Git and Docker and reports what it finds. Missing
optional tools are reported but do not fail the command.

```console
$ aistrap doctor
Environment check:

  OK       Python  Python 3.12.3
  OK       pip     pip 24.0
  OK       Git     git version 2.43.0
  MISSING  Docker  not found on PATH
```

### `--version` and `--help`

```bash
aistrap --version
aistrap --help
aistrap create --help
```

## Templates

| Template | Description | Good for |
| --- | --- | --- |
| `python-ai` | Basic Python AI project | Experiments, scripts, a place to start |
| `fastapi` | FastAPI AI backend | Serving a model or an agent over HTTP |
| `rag` | Retrieval-Augmented Generation project | Question answering over your own documents |
| `ml-project` | Machine learning project | Training, evaluating and using a model |

### `python-ai`

A minimal application package with settings, a working entry point, tests and
folders for data, notebooks and configuration.

```bash
aistrap create my-ai-app
cd my-ai-app && pip install -r requirements.txt
python -m app.main   # prints the most common words in a sample text
pytest
```

### `fastapi`

A FastAPI service with a `/health` endpoint, a root metadata endpoint, an
application factory, tests using `TestClient`, and a Dockerfile.

```bash
aistrap create my-api --template fastapi
cd my-api && pip install -r requirements.txt
uvicorn app.main:app --reload
curl http://127.0.0.1:8000/health
# {"status":"ok","app":"my-api","version":"0.1.0"}
```

### `rag`

A complete retrieval pipeline - ingestion, chunking, TF-IDF retrieval and prompt
building - written with the standard library only. Drop `.md`, `.txt` or `.rst`
files into `documents/` and ask questions. `build_prompt` in `app/main.py` is
the seam where you plug in the language model of your choice; `Retriever` in
`app/retrieval.py` is the seam for a vector database.

```bash
aistrap create my-rag-app --template rag
cd my-rag-app && pip install -r requirements.txt
python -m app.main "What is retrieval-augmented generation?"
```

### `ml-project`

A scikit-learn workflow that trains a model, reports its accuracy, saves it to
`models/`, and loads it again to make predictions.

```bash
aistrap create my-model --template ml-project
cd my-model && pip install -r requirements.txt
python -m app.train                     # Accuracy: 0.933, model saved
python -m app.predict 5.1 3.5 1.4 0.2   # Prediction: setosa (confidence 0.981)
```

## Generated project examples

See [`examples/`](examples/) for the exact output of each template, the commands
that produced it, and what to run next.

Every generated project follows the same shape:

```
my-project/
├── app/               # Your code
├── config/            # Configuration files
├── data/              # Datasets, git-ignored by default
├── tests/             # A passing pytest suite
├── .env.example       # Copy to .env and edit
├── .gitignore
├── pytest.ini
├── README.md          # Written for your project by name
└── requirements.txt
```

## Development setup

```bash
git clone https://github.com/ramalingamthangamani/Aistrap.git
cd aistrap

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev,templates]"
```

The `dev` extra installs pytest, ruff and `build`. The `templates` extra
installs the dependencies of the generated projects (FastAPI, scikit-learn), so
the test suite can run every template end to end instead of skipping two of them.

## Testing

```bash
pytest                     # the whole suite
pytest -k create           # just the create command
pytest --cov=aistrap
```

The suite covers the CLI (help, version, dispatch), the template registry,
project creation for every template, invalid templates and names, existing
directories, and the `doctor` command. It also runs the installed console script
in a subprocess and runs each generated project's own test suite, so packaging
mistakes and broken templates are caught.

Lint and formatting use [ruff](https://docs.astral.sh/ruff/):

```bash
ruff check .
ruff format --check .
```

## Contributing

Contributions are welcome - especially new templates. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and a
step-by-step guide to adding a template. If you use an AI coding agent, point it
at [AGENTS.md](AGENTS.md).

## Roadmap

Ideas for future releases, roughly in order of usefulness:

- More templates: LLM agent, fine-tuning, data pipeline.
- A flag to preview what a template would create before creating it.
- Optional `git init` and first commit after creating a project.
- Support for user-defined templates in a local directory.
- A `--no-input` flag for fully scripted use.

Suggestions and pull requests for any of these are welcome.

## License

[MIT](LICENSE)
