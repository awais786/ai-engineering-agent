from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from agentsys.config.settings import Settings

logger = structlog.get_logger()


async def _default_discover() -> list[str]:
    # STUB. TODO: query the board for new/changed items since the last scan.
    return []


async def scan_board(
    runner: Any,
    *,
    discover: Callable[[], Awaitable[list[str]]] = _default_discover,
) -> None:
    item_ids = await discover()
    for item_id in item_ids:
        await runner.start_run(board="github", item_id=item_id)
        logger.info("scheduled_run_triggered", item_id=item_id)


def start_scheduler(settings: Settings, runner: Any) -> AsyncIOScheduler | None:
    if not settings.board_scan_enabled:
        return None
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scan_board,
        "interval",
        seconds=settings.board_scan_interval_seconds,
        args=[runner],
    )
    scheduler.start()
    return scheduler
