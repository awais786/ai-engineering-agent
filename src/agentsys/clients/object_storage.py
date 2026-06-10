from __future__ import annotations


class ObjectStorageClient:
    """STUB. TODO: implement S3/GCS object storage."""

    async def put(self, key: str, data: bytes) -> str:
        raise NotImplementedError("ObjectStorageClient.put is not implemented yet")

    async def get(self, key: str) -> bytes:
        raise NotImplementedError("ObjectStorageClient.get is not implemented yet")
