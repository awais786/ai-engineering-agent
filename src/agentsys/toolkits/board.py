from __future__ import annotations

from typing import Protocol

from langchain_core.tools import BaseTool, StructuredTool

from agentsys.clients.github import Issue


class _BoardClient(Protocol):
    async def get_issue(self, item_id: str) -> Issue: ...
    async def post_comment(self, item_id: str, body: str) -> str: ...


class BoardToolkit:
    """Real toolkit wrapping a board client (GitHub Issues)."""

    def __init__(self, *, github: _BoardClient) -> None:
        self._github = github

    def get_tools(self) -> list[BaseTool]:
        async def read_board_item(item_id: str) -> str:
            """Read a board item (GitHub issue) by its id. Returns title and body."""
            issue = await self._github.get_issue(item_id)
            return f"Title: {issue.title}\n\nBody:\n{issue.body}"

        async def post_board_comment(item_id: str, body: str) -> str:
            """Post a comment on a board item. Returns the comment URL."""
            return await self._github.post_comment(item_id, body)

        return [
            StructuredTool.from_function(
                coroutine=read_board_item,
                name="read_board_item",
                description="Read a board item (GitHub issue) by id; returns title and body.",
            ),
            StructuredTool.from_function(
                coroutine=post_board_comment,
                name="post_board_comment",
                description="Post a comment on a board item by id; returns the comment URL.",
            ),
        ]
