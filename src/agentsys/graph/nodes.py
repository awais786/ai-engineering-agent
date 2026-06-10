from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, Protocol

import structlog

from agentsys.graph.state import WorkflowState

logger = structlog.get_logger()


class _Agent(Protocol):
    name: str

    async def run(self, state: WorkflowState) -> dict[str, Any]: ...


def make_node(agent: _Agent) -> Callable[[WorkflowState], Awaitable[dict[str, Any]]]:
    async def node(state: WorkflowState) -> dict[str, Any]:
        try:
            return await agent.run(state)
        except Exception as exc:  # noqa: BLE001
            logger.error("agent_failed", agent=agent.name, error=str(exc))
            return {agent.name: {"error": str(exc)}}

    return node
