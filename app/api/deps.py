from __future__ import annotations

from typing import Annotated

from fastapi import Header, HTTPException, status

from app.core.settings import get_settings


def verify_api_key(x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None) -> None:
    settings = get_settings()
    auth_enabled = settings.require_api_key or bool(settings.api_key)
    if not auth_enabled:
        return

    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key auth is enabled but API_KEY is not configured.",
        )

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )
