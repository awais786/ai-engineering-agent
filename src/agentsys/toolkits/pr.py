from __future__ import annotations

from langchain_core.tools import BaseTool


class PRToolkit:
    """STUB. TODO: implement GitHub PR APIs (create/comment/merge PR)."""

    def get_tools(self) -> list[BaseTool]:
        raise NotImplementedError("PRToolkit.get_tools is not implemented yet")
