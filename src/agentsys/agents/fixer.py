from __future__ import annotations

from typing import Any

from agentsys.agents.base import BaseAgent
from agentsys.graph.state import WorkflowState


class FixerAgent(BaseAgent):
    name = "fixer"

    async def run(self, state: WorkflowState) -> dict[str, Any]:
        # STUB. TODO: address reviewer feedback, push fix commits.
        return {"fixer": {"note": "fixer stub: not implemented"}}
