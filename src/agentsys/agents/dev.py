from __future__ import annotations

from typing import Any

from agentsys.agents.base import BaseAgent
from agentsys.graph.state import WorkflowState


class DevAgent(BaseAgent):
    name = "dev"

    async def run(self, state: WorkflowState) -> dict[str, Any]:
        # STUB. TODO: pick ticket, explore codebase, implement, open PR.
        return {"dev": {"note": "dev stub: not implemented"}}
