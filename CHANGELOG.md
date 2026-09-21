# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Six new templates, bringing the total to ten:
  - `ai-agent`: Autonomous AI agent with ReAct reasoning loop and tool registry.
  - `ai-fullstack`: Fullstack AI application with FastAPI backend and modern Web UI.
  - `mcp-server`: Model Context Protocol server exposing tools and resources over stdio.
  - `multimodal`: Multimodal vision and media AI pipeline.
  - `chat-stream`: Streaming conversational AI with Server-Sent Events (SSE) and session history.
  - `llm-eval`: LLM evaluation and benchmark harness for accuracy, F1, and latency.

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
