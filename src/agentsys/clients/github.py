from __future__ import annotations

import httpx
from pydantic import BaseModel


class Issue(BaseModel):
    number: int
    title: str
    body: str


class GitHubClient:
    """Minimal GitHub Issues client: read an issue, post a comment."""

    def __init__(self, *, token: str, repo: str, http: httpx.AsyncClient) -> None:
        self._token = token
        self._repo = repo  # "owner/name"
        self._http = http

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "authorization": f"Bearer {self._token}",
            "accept": "application/vnd.github+json",
        }

    async def get_issue(self, item_id: str) -> Issue:
        resp = await self._http.get(
            f"/repos/{self._repo}/issues/{item_id}", headers=self._headers
        )
        resp.raise_for_status()
        data = resp.json()
        return Issue(number=data["number"], title=data["title"], body=data.get("body") or "")

    async def post_comment(self, item_id: str, body: str) -> str:
        resp = await self._http.post(
            f"/repos/{self._repo}/issues/{item_id}/comments",
            headers=self._headers,
            json={"body": body},
        )
        resp.raise_for_status()
        return str(resp.json()["html_url"])
