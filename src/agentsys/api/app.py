from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from agentsys.api.routes import router
from agentsys.app_context import build_agents
from agentsys.clients.github import GitHubClient
from agentsys.config.settings import Settings
from agentsys.graph.builder import build_graph
from agentsys.graph.checkpointer import checkpointer_from_dsn
from agentsys.graph.runner import Runner
from agentsys.observability.langfuse import make_langfuse_handler
from agentsys.observability.logging import configure_logging
from agentsys.scheduler.board_scan import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    configure_logging(settings.log_level)

    async with (
        httpx.AsyncClient(base_url="https://api.github.com") as http,
        checkpointer_from_dsn(settings.postgres_dsn) as saver,
    ):
        await saver.setup()
        github = GitHubClient(
            token=settings.github_token, repo=settings.github_repo, http=http
        )
        agents = build_agents(settings, github=github)
        graph = build_graph(agents, checkpointer=saver)
        runner = Runner(graph=graph, langfuse_handler=make_langfuse_handler(settings))
        app.state.runner = runner

        scheduler = start_scheduler(settings, runner)
        try:
            yield
        finally:
            if scheduler is not None:
                scheduler.shutdown(wait=False)


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(title="agentsys", lifespan=lifespan)
    app.state.settings = settings or Settings()
    app.include_router(router)
    return app
