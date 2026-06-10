from __future__ import annotations

from typing import Any

from agentsys.agents.base import BaseAgent
from agentsys.agents.dev import DevAgent
from agentsys.agents.fixer import FixerAgent
from agentsys.agents.pm import PMAgent
from agentsys.agents.reviewer import ReviewerAgent
from agentsys.config.settings import Settings


def build_agents(
    settings: Settings,
    *,
    github: Any,
    pm_model: Any | None = None,
) -> dict[str, BaseAgent]:
    return {
        "pm": PMAgent(settings, github=github, model=pm_model),
        "dev": DevAgent(settings),
        "reviewer": ReviewerAgent(settings),
        "fixer": FixerAgent(settings),
    }
