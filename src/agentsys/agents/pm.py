from __future__ import annotations

from typing import Any, Protocol

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool

from agentsys.agents.base import BaseAgent
from agentsys.clients.github import Issue
from agentsys.config.settings import Settings
from agentsys.graph.state import WorkflowState
from agentsys.toolkits.board import BoardToolkit

_SYSTEM = (
    "You are a senior product manager. Use the available tools to read the board "
    "item, then produce a concise, actionable technical specification: problem, "
    "proposed approach, acceptance criteria, and suggested tickets. Output Markdown. "
    "When finished, respond with only the specification and make no further tool calls."
)


class _BoardClient(Protocol):
    async def get_issue(self, item_id: str) -> Issue: ...
    async def post_comment(self, item_id: str, body: str) -> str: ...


class PMAgent(BaseAgent):
    name = "pm"

    def __init__(
        self,
        settings: Settings,
        *,
        github: _BoardClient,
        model: BaseChatModel | None = None,
        max_iterations: int = 5,
    ) -> None:
        super().__init__(settings)
        self._github = github
        self._model = model or self.get_model()
        self._max_iterations = max_iterations

    def get_tools(self) -> list[BaseTool]:
        # PM only needs to READ the board; posting is done deterministically after the loop
        return [
            t
            for t in BoardToolkit(github=self._github).get_tools()
            if t.name == "read_board_item"
        ]

    async def run(self, state: WorkflowState) -> dict[str, Any]:
        tools = {t.name: t for t in self.get_tools()}
        model = self._model.bind_tools(list(tools.values()))
        messages: list[Any] = [
            SystemMessage(content=_SYSTEM),
            HumanMessage(
                content=f"Read board item {state.item_id} and write its technical spec."
            ),
        ]

        spec = ""
        for _ in range(self._max_iterations):
            response = await model.ainvoke(messages)
            messages.append(response)
            tool_calls = getattr(response, "tool_calls", None)
            if not tool_calls:
                spec = (
                    response.content
                    if isinstance(response.content, str)
                    else str(response.content)
                )
                break
            for call in tool_calls:
                tool = tools[call["name"]]
                result = await tool.ainvoke(call["args"])
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=call["id"])
                )

        comment_url = await self._github.post_comment(state.item_id, spec)
        return {"pm": {"spec": spec, "comment_url": comment_url}}
