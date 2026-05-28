from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.models import AgentRun, ComprehensiveReport

AGENTS = ("analytics", "operations", "marketing", "strategy")


def create_agent_run(
    db: Session,
    *,
    agent: str,
    action: str,
    status: str,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any],
) -> AgentRun:
    record = AgentRun(
        agent=agent,
        action=action,
        status=status,
        request_payload=request_payload,
        response_payload=response_payload,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_latest_run(db: Session, agent: str) -> AgentRun | None:
    stmt = (
        select(AgentRun)
        .where(AgentRun.agent == agent)
        .order_by(desc(AgentRun.created_at), desc(AgentRun.id))
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_latest_agent_data(db: Session, agent: str) -> dict[str, Any]:
    latest = get_latest_run(db, agent)
    if latest is None:
        return {}
    response_payload = latest.response_payload or {}
    if isinstance(response_payload, dict):
        data = response_payload.get("data", {})
        if isinstance(data, dict):
            return data
    return {}


def get_agents_status(db: Session) -> tuple[dict[str, dict[str, str | None]], dict[str, bool]]:
    agents_payload: dict[str, dict[str, str | None]] = {}
    data_available: dict[str, bool] = {}

    for agent in AGENTS:
        latest = get_latest_run(db, agent)
        last_run = latest.created_at.isoformat() if latest else None
        agents_payload[agent] = {"status": "active", "last_run": last_run}
        data_available[agent] = bool(get_latest_agent_data(db, agent))

    return agents_payload, data_available


def create_comprehensive_report(db: Session, payload: dict[str, Any]) -> ComprehensiveReport:
    report = ComprehensiveReport(report_payload=payload)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_latest_comprehensive_report(db: Session) -> dict[str, Any] | None:
    stmt = select(ComprehensiveReport).order_by(desc(ComprehensiveReport.created_at)).limit(1)
    report = db.execute(stmt).scalar_one_or_none()
    if report is None:
        return None
    payload = report.report_payload
    if isinstance(payload, dict):
        return payload
    return None
