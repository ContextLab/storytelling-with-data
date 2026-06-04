# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP server that exposes datasets and visualization tools via the Model Context Protocol. LLM clients can upload data, specify visualizations, and retrieve rendered results through a contextual workflow.

## Development Workflow

This project uses **SpecKit** (specification-driven development). Features follow a strict lifecycle managed by Claude skills:

1. `/speckit-specify` — create feature spec from natural language description
2. `/speckit-clarify` — identify and resolve ambiguities in the spec
3. `/speckit-plan` — generate architecture and implementation plan (`plan.md`)
4. `/speckit-tasks` — generate ordered task list (`tasks.md`)
5. `/speckit-implement` — execute tasks and generate code
6. `/speckit-analyze` — consistency check across spec/plan/tasks artifacts

Git operations are managed via `/speckit-git-feature` (create branch), `/speckit-git-commit` (auto-commit after workflow phases), and `/speckit-git-validate` (branch naming).

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
specs/001-mcp-data-viz-server/plan.md
<!-- SPECKIT END -->

## Build & Test Commands

```bash
uv venv                        # create virtual environment (first time)
uv pip install -e ".[dev]"     # install package + dev dependencies
pytest                         # run all tests
pytest tests/integration/      # integration tests only
python -m data_viz_mcp         # run the MCP server (stdio transport)
data-viz-mcp                   # same, via installed entry point
```

## Architecture

No source code exists yet. The intended design:

- **MCP server layer**: Exposes tools and resources per the MCP spec for LLM clients to call
- **Dataset layer**: Accepts data uploads and manages in-memory or persisted datasets
- **Visualization layer**: Accepts visualization specs, renders charts/graphs, returns results (likely as image data or structured output)
- **Workflow**: Client uploads data → specifies visualization type/config → server renders → returns result
