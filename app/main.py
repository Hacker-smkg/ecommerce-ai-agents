from __future__ import annotations

import logging

from fastapi import FastAPI

from app.api.routers import agents, health, reports
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.db.session import init_db

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )

    @application.on_event("startup")
    def on_startup() -> None:
        init_db()
        logger.info("Database initialized successfully.")

    application.include_router(health.router)
    application.include_router(agents.router)
    application.include_router(reports.router)
    return application


app = create_app()
