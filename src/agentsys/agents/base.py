from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool

from agentsys.config.settings import Settings
from agentsys.graph.state import WorkflowState
from agentsys.llm.factory import get_chat_model


class BaseAgent(ABC):
    name: str = "base"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @abstractmethod
    async def run(self, state: WorkflowState) -> dict[str, Any]:
        """Return a partial state update scoped to this agent's namespace."""

    def get_model(self) -> BaseChatModel:
        llm = self.settings.model_for(self.name)
        api_key = (
            self.settings.anthropic_api_key
            if llm.provider == "anthropic"
            else self.settings.openai_api_key
        )
        return get_chat_model(llm, api_key=api_key)

    def get_tools(self) -> list[BaseTool]:
        return []

    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([("system", "You are an agent.")])
