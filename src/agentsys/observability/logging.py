from __future__ import annotations

import logging

import structlog


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(format="%(message)s", level=getattr(logging, level.upper()))
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        cache_logger_on_first_use=True,
    )


def bind_run_context(*, run_id: str, thread_id: str) -> None:
    structlog.contextvars.bind_contextvars(run_id=run_id, thread_id=thread_id)
