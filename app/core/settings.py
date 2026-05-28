from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _to_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _default_database_url() -> str:
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{data_dir / 'ecommerce_ai.db'}"


@dataclass
class Settings:
    app_name: str
    app_description: str
    app_version: str
    host: str
    port: int
    reload: bool
    log_level: str
    database_url: str
    api_key: str | None
    require_api_key: bool


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "E-commerce AI Agents API"),
        app_description=os.getenv(
            "APP_DESCRIPTION",
            "Backend API for a modular multi-agent e-commerce orchestration system.",
        ),
        app_version=os.getenv("APP_VERSION", "2.0.0"),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=_to_bool(os.getenv("RELOAD"), default=False),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        database_url=os.getenv("DATABASE_URL", _default_database_url()),
        api_key=os.getenv("API_KEY"),
        require_api_key=_to_bool(os.getenv("REQUIRE_API_KEY"), default=False),
    )


def reset_settings_cache() -> None:
    get_settings.cache_clear()
