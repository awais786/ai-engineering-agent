# Implementation Tasks

> Skeleton is done. Team implements the items below, one ticket per row.
> Each task: write the failing test first, implement, make it pass, commit.

---

## Done (skeleton — do not re-implement)

- [x] Project scaffolding (uv, pyproject.toml, ruff, mypy, pytest, CI, pre-commit)
- [x] Settings with per-agent model overrides (`config/settings.py`)
- [x] Structlog JSON logging (`observability/logging.py`)
- [x] Langfuse callback factory, env-gated (`observability/langfuse.py`)
- [x] Provider-agnostic LLM factory (`llm/factory.py`)
- [x] GitHub Issues client — read issue, post comment (`clients/github.py`)
- [x] Chroma vector store client (`clients/chroma.py`)
- [x] Postgres connection pool factory (`clients/postgres.py`)
- [x] Board toolkit — `read_board_item`, `post_board_comment` (`toolkits/board.py`)
- [x] PM agent — reads issue, generates spec, posts comment (`agents/pm.py`)
- [x] Graph state with namespaced sub-states (`graph/state.py`)
- [x] Graph node adapter with error capture (`graph/nodes.py`)
- [x] Graph builder PM→Dev→Reviewer→Fixer→Merge (`graph/builder.py`)
- [x] Postgres checkpointer factory (`graph/checkpointer.py`)
- [x] Runner — background start + status read (`graph/runner.py`)
- [x] Composition root (`app_context.py`)
- [x] FastAPI app + `/runs` routes + lifespan wiring (`api/`)
- [x] APScheduler board-scan job (`scheduler/board_scan.py`)
- [x] Shared test fixtures (`tests/conftest.py`)
- [x] docker-compose (Postgres + Chroma)

---

## To Do

### Tests (write tests for the existing skeleton)

- [ ] **TEST-01** — Settings: defaults and per-agent model override (`tests/config/test_settings.py`)
- [ ] **TEST-02** — Structlog: configure logging and bind run context (`tests/observability/test_logging.py`)
- [ ] **TEST-03** — Langfuse: returns None when unset, returns handler when keys present (`tests/observability/test_langfuse.py`)
- [ ] **TEST-04** — LLM factory: anthropic provider, openai provider, unknown raises (`tests/llm/test_factory.py`)
- [ ] **TEST-05** — GitHub client: get_issue parses response, post_comment returns URL (`tests/clients/test_github.py`)
- [ ] **TEST-06** — Stub clients: object storage and redis raise NotImplementedError (`tests/clients/test_stubs.py`)
- [ ] **TEST-07** — Chroma client: get_or_create_collection delegates correctly (`tests/clients/test_chroma.py`)
- [ ] **TEST-08** — Board toolkit: get_tools returns BaseTool list, tools invoke client (`tests/toolkits/test_board.py`)
- [ ] **TEST-09** — Stub toolkits: all five raise NotImplementedError (`tests/toolkits/test_stubs.py`)
- [ ] **TEST-10** — Graph state: default sub-states present and isolated (`tests/graph/test_state.py`)
- [ ] **TEST-11** — Checkpointer: factory builds context manager (`tests/graph/test_checkpointer.py`)
- [ ] **TEST-12** — Stub agents: dev/reviewer/fixer annotate their namespace (`tests/agents/test_stub_agents.py`)
- [ ] **TEST-13** — PM agent: reads via tool, generates spec, posts comment (`tests/agents/test_pm.py`)
- [ ] **TEST-14** — Graph nodes: passes update through, captures error into namespace (`tests/graph/test_nodes.py`)
- [ ] **TEST-15** — Graph builder: traverses all nodes and completes, marks failed on error (`tests/graph/test_builder.py`)
- [ ] **TEST-16** — Runner: start run and get run, unknown run returns None (`tests/graph/test_runner.py`)
- [ ] **TEST-17** — App context: build_agents returns all four agents (`tests/test_app_context.py`)
- [ ] **TEST-18** — API routes: POST /runs, GET /runs/{id}, 404 on missing, GET /health (`tests/api/test_routes.py`)
- [ ] **TEST-19** — Scheduler: scan_board triggers runner, disabled returns None (`tests/scheduler/test_board_scan.py`)

---

### Real Implementations (stubs to fill in)

- [ ] **IMPL-01** — Dev agent: pick ticket, explore codebase, implement, open PR (`agents/dev.py`)
- [ ] **IMPL-02** — Reviewer agent: review open PR, post review comments (`agents/reviewer.py`)
- [ ] **IMPL-03** — Fixer agent: address reviewer feedback, push fix commits (`agents/fixer.py`)
- [ ] **IMPL-04** — Git toolkit: branch and commit operations (`toolkits/git.py`)
- [ ] **IMPL-05** — PR toolkit: create, comment, and merge PR via GitHub API (`toolkits/pr.py`)
- [ ] **IMPL-06** — Codebase toolkit: semantic and regex search over the repo (`toolkits/codebase.py`)
- [ ] **IMPL-07** — Shell toolkit: sandboxed lint and test runner (`toolkits/shell.py`)
- [ ] **IMPL-08** — Messaging toolkit: Slack/Teams notifications (`toolkits/messaging.py`)
- [ ] **IMPL-09** — Object storage client: S3/GCS put and get (`clients/object_storage.py`)
- [ ] **IMPL-10** — Redis client: cache get/set (`clients/redis.py`)
- [ ] **IMPL-11** — Board scan discovery: query board for new/changed items (`scheduler/board_scan.py` → `_default_discover`)

---

## Definition of Done (full system)

- [ ] `uv run pytest` — all tests pass
- [ ] `uv run ruff check .` — no lint errors
- [ ] `uv run mypy src` — no type errors
- [ ] `docker compose up` → `POST /runs` → PM posts spec comment on GitHub issue
- [ ] `GET /runs/{id}` returns `status: completed` with `pm.spec` populated
- [ ] CI green on GitHub Actions
