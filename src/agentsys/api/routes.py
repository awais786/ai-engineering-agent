from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from agentsys.api.schemas import RunCreated, RunRequest

router = APIRouter()


def get_runner(request: Request) -> Any:
    return request.app.state.runner


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/runs", response_model=RunCreated, status_code=status.HTTP_202_ACCEPTED)
async def create_run(body: RunRequest, runner: Any = Depends(get_runner)) -> RunCreated:
    run_id = await runner.start_run(board=body.board, item_id=body.item_id)
    return RunCreated(run_id=run_id)


@router.get("/runs/{run_id}")
async def read_run(run_id: str, runner: Any = Depends(get_runner)) -> dict[str, Any]:
    result = await runner.get_run(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="run not found")
    return result
