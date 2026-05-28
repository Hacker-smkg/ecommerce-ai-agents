from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def read_root() -> dict[str, str]:
    return {"message": "E-commerce AI Agents API is running"}


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
