from __future__ import annotations

from typing import Any

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


def checkpointer_from_dsn(dsn: str) -> Any:
    """Return an async context manager yielding an AsyncPostgresSaver.

    Usage:
        async with checkpointer_from_dsn(dsn) as saver:
            await saver.setup()
            graph = build_graph(..., checkpointer=saver)
    """
    return AsyncPostgresSaver.from_conn_string(dsn)
