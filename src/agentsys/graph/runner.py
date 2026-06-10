from __future__ import annotations

import asyncio
import uuid
from typing import Any

import structlog

from agentsys.graph.state import WorkflowState
from agentsys.observability.logging import bind_run_context

logger = structlog.get_logger()


class Runner:
    """Starts graph runs as background tasks; reads status from the checkpointer."""

    def __init__(self, *, graph: Any, langfuse_handler: Any | None = None) -> None:
        self._graph = graph
        self._langfuse = langfuse_handler
        self._tasks: set[asyncio.Task[Any]] = set()

    def _config(self, thread_id: str) -> dict[str, Any]:
        cfg: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
        if self._langfuse is not None:
            cfg["callbacks"] = [self._langfuse]
        return cfg

    async def start_run(self, *, board: str, item_id: str, wait: bool = False) -> str:
        run_id = uuid.uuid4().hex
        bind_run_context(run_id=run_id, thread_id=run_id)
        initial = WorkflowState(run_id=run_id, board=board, item_id=item_id)

        async def _invoke() -> None:
            await self._graph.ainvoke(initial, config=self._config(run_id))

        if wait:
            await _invoke()
        else:
            task = asyncio.create_task(_invoke())
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
        logger.info("run_started", board=board, item_id=item_id)
        return run_id

    async def get_run(self, run_id: str) -> dict[str, Any] | None:
        snapshot = await self._graph.aget_state(self._config(run_id))
        if not snapshot or not snapshot.values:
            return None
        values = snapshot.values
        return values if isinstance(values, dict) else values.model_dump()
