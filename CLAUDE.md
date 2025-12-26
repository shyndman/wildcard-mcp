# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
uv sync --dev                                    # Install dependencies
uv run pytest -v                                 # Run all tests
uv run pytest tests/test_server.py::test_name   # Run single test
ruff check --fix && ruff format                 # Lint and format
uv run python -m wildcard_mcp.server            # Run server locally
```

## Architecture

**Entry point:** `src/wildcard_mcp/__main__.py` calls `create_server()` and runs it.

**Server creation** (`src/wildcard_mcp/server.py`):
- `find_config_path()` uses `WILDCARD_CONFIG_PATH` (defaults to `/config/config.toml`), falls back to local `config.toml`
- `create_server(config_path)` is a factory that loads config, registers the `randomize` tool, and returns a FastMCP instance
- Transport defaults to SSE; override with `WILDCARD_TRANSPORT` env var (e.g., `stdio`)

**Config loading** (`src/wildcard_mcp/config.py`):
- `load_config()` parses TOML, validates `[categories]` section
- `load_category_data()` reads text files (one item per line), paths relative to config file

## Code Style

- 2-space indentation, 100-char line length (ruff)
- Pre-commit hooks run ruff automatically

## Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Capitalize the first word of the description.
