from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PMState(BaseModel):
    spec: str | None = None
    comment_url: str | None = None
    error: str | None = None


class DevState(BaseModel):
    note: str | None = None
    error: str | None = None


class ReviewerState(BaseModel):
    note: str | None = None
    error: str | None = None


class FixerState(BaseModel):
    note: str | None = None
    error: str | None = None


class WorkflowState(BaseModel):
    run_id: str
    board: str
    item_id: str
    pm: PMState = Field(default_factory=PMState)
    dev: DevState = Field(default_factory=DevState)
    reviewer: ReviewerState = Field(default_factory=ReviewerState)
    fixer: FixerState = Field(default_factory=FixerState)
    status: Literal["running", "completed", "failed"] = "running"
