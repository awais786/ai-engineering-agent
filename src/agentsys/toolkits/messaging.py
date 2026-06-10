from __future__ import annotations

from langchain_core.tools import BaseTool


class MessagingToolkit:
    """STUB. TODO: implement Slack/Teams messaging."""

    def get_tools(self) -> list[BaseTool]:
        raise NotImplementedError("MessagingToolkit.get_tools is not implemented yet")
