# ai-engineering-agent

An AI-driven PM + Engineering multi-agent system built on LangGraph.

The full agent graph runs end-to-end: **PM → Dev → Reviewer → Fixer → Merge**.
The PM agent is real — it reads a GitHub Issue, generates a technical spec, and posts it back as a comment. Dev, Reviewer, and Fixer are stubs ready for implementation.

## Quickstart

```bash
git clone git@github.com:awais786/ai-engineering-agent.git
cd ai-engineering-agent

cp .env.example .env          # fill in GITHUB_TOKEN, GITHUB_REPO, ANTHROPIC_API_KEY
docker compose up -d          # start Postgres + Chroma
uv sync --all-extras --dev
uv run uvicorn agentsys.api.app:create_app --factory --host 0.0.0.0 --port 8080
```

Trigger a run against a GitHub issue:

```bash
curl -X POST localhost:8080/runs \
  -H 'content-type: application/json' \
  -d '{"board":"github","item_id":"42"}'
# -> {"run_id":"..."}

curl localhost:8080/runs/<run_id>
# -> {"status":"completed", "pm": {"spec":"...", "comment_url":"..."}, ...}
```

## Development

```bash
uv run pytest                  # run all tests
uv run ruff check .            # lint
uv run ruff format .           # format
uv run mypy src                # type check
```

## Architecture

```
POST /runs
    └── Runner.start_run()
            └── LangGraph: pm → dev → reviewer → fixer → merge
                    ├── PMAgent       ← REAL: reads issue, generates spec, posts comment
                    ├── DevAgent      ← STUB: implement codebase exploration + PR opening
                    ├── ReviewerAgent ← STUB: implement PR review + comments
                    └── FixerAgent    ← STUB: implement feedback fixes + commits
```

**3-layer tool pattern:**
`clients/` (plain async) → `toolkits/` (`@tool` wrappers) → agents bind toolkits

## What needs to be implemented

See [`TASKS.md`](TASKS.md) for the full task list and [`CLAUDE.md`](CLAUDE.md) for architecture rules.

| Stub | What to build |
|------|--------------|
| `agents/dev.py` | Codebase exploration + PR opening |
| `agents/reviewer.py` | PR review + comment posting |
| `agents/fixer.py` | Address review feedback + push fixes |
| `toolkits/git.py` | Branch, commit operations |
| `toolkits/pr.py` | Create/comment/merge PR |
| `toolkits/codebase.py` | Semantic/regex codebase search |
| `toolkits/shell.py` | Sandboxed lint/test runner |
| `toolkits/messaging.py` | Slack/Teams notifications |
| `clients/object_storage.py` | S3/GCS |
| `clients/redis.py` | Redis cache/queue |

## Plane tasks

https://projects.arbisoft.com/arbisoft/browse/ARBISOFTOPEN-384/

## Docs

- [`docs/2026-06-10-ai-pm-engineering-multi-agent-boilerplate-design.md`](docs/2026-06-10-ai-pm-engineering-multi-agent-boilerplate-design.md) — architecture and design decisions
- [`docs/2026-06-10-ai-pm-engineering-multi-agent-boilerplate.md`](docs/2026-06-10-ai-pm-engineering-multi-agent-boilerplate.md) — task-by-task TDD implementation plan
