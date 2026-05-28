from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AgentRuntimeStatus(BaseModel):
    status: str
    last_run: str | None = None


class AgentStatusResponse(BaseModel):
    agents: dict[str, AgentRuntimeStatus]
    data_available: dict[str, bool]


class ComprehensiveReportResponse(BaseModel):
    report_date: str
    analytics: dict[str, Any]
    operations: dict[str, Any]
    marketing: dict[str, Any]
    strategy: dict[str, Any]
