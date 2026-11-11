# Agent Instructions

This file is the single source of truth for shared AI agent instructions in
this repository.

## Project

This is a Python package and CLI for sending notifications to Slack. The
package uses a `src` layout under `src/notifications`.

## Build, test, and lint

- Sync dependencies: `uv sync`
- Build the package: `uv build` (Hatchling is the configured build backend.)
- Run the CLI: `uv run notify --help`
- Run Ruff: `uv run ruff check`
- Run all pytest tests: `uv run pytest`
- Run one test: `uv run pytest tests/test_module.py::test_function`

Pytest discovers tests under `tests/`, as configured in `pyproject.toml`.

## Architecture

- `pyproject.toml` packages `src/notifications` and exposes the `notify`
  console script through `notifications.cli:main`.
- `src/notifications/cli.py` defines the Typer/Rich command-line interface.
  Its single `slack` command is invoked as `notify "message"`; `--channel`
  selects a destination and defaults to `#general`.
- `src/notifications/environment.py` loads `./.env` and reads
  `SLACK_BOT_TOKEN`. `src/notifications/slack/__init__.py` exposes the Slack
  connection API. The CLI and library both use `SlackConnection`.
- `src/notifications/slack/connection.py` builds Slack message payloads and
  sends them to `chat.postMessage`. Slack API response codes are translated
  to specific exceptions by the error types and factory in
  `src/notifications/slack/error.py`; the CLI catches `SlackError`.
- `README.md` documents end-user setup, CLI usage, and a library example.

## Conventions

- Keep changes consistent with the existing Python 3.13+ code and package
  structure.
- Set `SLACK_BOT_TOKEN` before importing `notifications.slack`: environment
  configuration is loaded during module import, and `SlackConnection` reads
  the token at class definition time. `.env` is local configuration and must
  not be committed.
- `SlackConnection.post_message()` returns `(success, response)` for ordinary
  Slack API responses. Missing credentials and recognized API errors are
  raised as `SlackError` subclasses; callers should account for both paths.
- The default channel and direct-message behavior are described in the
  README. Private-channel posting requires the bot to be invited, and a user
  ID can be used as the channel for a direct message.
- Keep the README accurate when changing setup or CLI behavior.
- Never add real Slack tokens to source control. Use `SLACK_BOT_TOKEN` from
  the environment; local `.env` files are ignored.
