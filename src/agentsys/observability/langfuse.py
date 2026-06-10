from __future__ import annotations

from typing import Any

from agentsys.config.settings import Settings

try:
    from langfuse.langchain import CallbackHandler as _CallbackHandler
except Exception:  # pragma: no cover
    _CallbackHandler = None  # type: ignore[assignment, misc]


def make_langfuse_handler(settings: Settings) -> Any | None:
    """Return a Langfuse LangChain callback handler, or None if disabled."""
    if not (settings.langfuse_public_key and settings.langfuse_secret_key):
        return None
    if _CallbackHandler is None:  # pragma: no cover
        return None
    return _CallbackHandler(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )
