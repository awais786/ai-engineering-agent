from __future__ import annotations

from typing import Any

from agentsys.agents.base import BaseAgent
from agentsys.graph.state import WorkflowState


class ReviewerAgent(BaseAgent):
    name = "reviewer"

    async def run(self, state: WorkflowState) -> dict[str, Any]:
        # STUB. TODO: review open PR, post review comments.
        return {"reviewer": {"note": "reviewer stub: not implemented"}}
