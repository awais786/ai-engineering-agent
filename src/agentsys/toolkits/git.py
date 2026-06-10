from __future__ import annotations

from langchain_core.tools import BaseTool


class GitToolkit:
    """STUB. TODO: implement git operations (branch, commit) for the Dev agent."""

    def get_tools(self) -> list[BaseTool]:
        raise NotImplementedError("GitToolkit.get_tools is not implemented yet")
