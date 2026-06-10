from __future__ import annotations

from typing import Any, Protocol


class _ChromaLike(Protocol):
    def get_or_create_collection(self, name: str) -> Any: ...


class VectorStoreClient:
    """Thin wrapper over a Chroma client."""

    def __init__(self, *, chroma: _ChromaLike) -> None:
        self._chroma = chroma

    def add(self, collection: str, *, ids: list[str], documents: list[str]) -> None:
        col = self._chroma.get_or_create_collection(collection)
        col.add(ids=ids, documents=documents)

    @classmethod
    def from_settings(cls, host: str, port: int) -> VectorStoreClient:
        import chromadb

        return cls(chroma=chromadb.HttpClient(host=host, port=port))
