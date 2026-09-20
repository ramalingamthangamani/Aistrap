# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Renamed the project, CLI, and Python package from `ai-project-starter` to `aistrap`.

## [0.1.0] - 2026-09-20

### Added

- `create` command that generates a project from a template, with `--template`,
  `--directory` and `--force` options.
- `list` command that shows the bundled templates and their descriptions.
- `doctor` command that reports on Python, pip, Git and Docker.
- Four templates: `python-ai`, `fastapi`, `rag` and `ml-project`.
- Test suite covering the CLI, every template, and the generated projects.
- GitHub Actions workflow running lint, tests and a packaging check.
