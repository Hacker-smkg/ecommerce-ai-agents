from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    action: str
    data: dict[str, Any] | None = Field(default_factory=dict)
    analytics_data: dict[str, Any] | None = None
    operations_data: dict[str, Any] | None = None
    marketing_data: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


class AgentResponse(BaseModel):
    agent: str
    action: str
    timestamp: str
    status: str
    data: dict[str, Any]
    recommendations: list[str] = Field(default_factory=list)
    next_action: str | None = None
