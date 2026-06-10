from __future__ import annotations

from pydantic import BaseModel


class RunRequest(BaseModel):
    board: str = "github"
    item_id: str


class RunCreated(BaseModel):
    run_id: str
