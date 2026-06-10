from __future__ import annotations

from langchain_core.tools import BaseTool


class ShellToolkit:
    """STUB. TODO: implement sandboxed run-commands (lint/test)."""

    def get_tools(self) -> list[BaseTool]:
        raise NotImplementedError("ShellToolkit.get_tools is not implemented yet")
