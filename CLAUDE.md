# agentsys — AI-Driven PM + Engineering Multi-Agent System

## What this repo is

A LangGraph-orchestrated multi-agent skeleton: **PM → Dev → Reviewer → Fixer → Merge**.
The full graph runs end-to-end. Only the **PM agent is real** (reads a GitHub Issue, generates a technical spec, posts it back as a comment). Dev, Reviewer, and Fixer are pass-through stubs waiting to be implemented.

## Tech stack

- **Python 3.11+**, `uv` for dependency management
- **LangGraph** — stateful graph with Postgres checkpointer
- **LangChain** — agent framework, tool binding, prompt templates
- **LangChain Anthropic** — default LLM provider (`claude-sonnet-4-6`)
- **FastAPI** — async API (`POST /runs`, `GET /runs/{id}`)
- **Postgres** — LangGraph checkpointer (state persistence per run)
- **Chroma** — vector store (ready, not yet used by PM slice)
- **APScheduler** — in-process board scan job
- **structlog** — JSON logging with `run_id`/`thread_id` bound per run
- **Langfuse** — LLM tracing, env-gated (no-op when keys unset)
- **Ruff** — lint + format
- **mypy strict** — type checking
- **pytest + pytest-asyncio** — all tests offline, LLM and clients mocked

## Project structure

```
src/agentsys/
├── config/settings.py          # pydantic-settings, per-agent model overrides
├── observability/              # structlog + Langfuse factory
├── llm/factory.py              # provider-agnostic chat model factory
├── clients/                    # boundary clients (github/chroma/postgres real; s3/redis stub)
├── toolkits/                   # @tool wrappers (board real; git/pr/codebase/shell/messaging stub)
├── agents/                     # pm real; dev/reviewer/fixer stub
├── graph/                      # state, nodes, builder, checkpointer, runner
├── api/                        # FastAPI app + routes + schemas
├── scheduler/board_scan.py     # APScheduler job
└── app_context.py              # composition root
tests/                          # mirrors src/agentsys/, shared fixtures in conftest.py
docs/                           # design spec + implementation plan
```

## Running locally

```bash
cp .env.example .env            # fill in GITHUB_TOKEN, GITHUB_REPO, ANTHROPIC_API_KEY
docker compose up -d            # start Postgres + Chroma
uv sync --all-extras --dev
uv run uvicorn agentsys.api.app:create_app --factory --host 0.0.0.0 --port 8080
```

## Common commands

```bash
uv run pytest                   # run all tests
uv run pytest tests/agents/     # run a specific module
uv run ruff check .             # lint
uv run ruff format .            # format
uv run mypy src                 # type check
```

## Architecture rules

- **Agents never mutate another agent's namespace** — each `run()` returns a partial update scoped only to its own key (`pm`, `dev`, `reviewer`, `fixer`).
- **3-layer tool pattern**: `clients/` (plain async callables) → `toolkits/` (`@tool` wrappers) → agents bind toolkits via `get_tools()`. Never call a client directly from an agent.
- **All tests are offline** — mock the LLM and all clients at the boundary. Never hit a real API in tests.
- **All agent/graph/client code is async**.
- **No hardcoded secrets** — everything via `Settings` loaded from `.env`.

## What needs to be implemented (stubs)

See `TASKS.md` for the full list. In short:

| File | What to build |
|------|--------------|
| `agents/dev.py` | Codebase exploration + PR opening |
| `agents/reviewer.py` | PR review + comment posting |
| `agents/fixer.py` | Address review feedback + push fixes |
| `toolkits/git.py` | Branch, commit operations |
| `toolkits/pr.py` | Create/comment/merge PR |
| `toolkits/codebase.py` | Semantic/regex search |
| `toolkits/shell.py` | Sandboxed lint/test runner |
| `toolkits/messaging.py` | Slack/Teams notifications |
| `clients/object_storage.py` | S3/GCS |
| `clients/redis.py` | Redis cache/queue |
| `scheduler/board_scan.py` | `_default_discover()` — query board for new items |

## How to implement a stub agent (example: DevAgent)

1. Write the failing test in `tests/agents/test_dev.py` (mock the LLM + clients)
2. Implement `agents/dev.py` — follow the same pattern as `agents/pm.py`
3. Add the toolkits it needs in `get_tools()`
4. Run `uv run pytest tests/agents/test_dev.py -v` — must pass
5. Run `uv run mypy src` and `uv run ruff check .` — must be clean
6. Commit

## Per-agent model overrides

Override the LLM for any agent via env without touching code:

```
AGENT_DEV__MODEL=claude-opus-4-8
AGENT_REVIEWER__MODEL=claude-haiku-4-5
```

## Plane project

Tasks tracked at: https://projects.arbisoft.com/arbisoft/browse/ARBISOFTOPEN-384/
Sub-tasks: ARBISOFTOPEN-385 to ARBISOFTOPEN-395
