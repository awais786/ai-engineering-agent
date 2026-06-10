from __future__ import annotations

from psycopg_pool import AsyncConnectionPool


def make_pool(dsn: str) -> AsyncConnectionPool:
    """Create (but do not open) an async Postgres connection pool."""
    return AsyncConnectionPool(conninfo=dsn, open=False)
