from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="completed")
    request_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    response_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        index=True,
    )


class ComprehensiveReport(Base):
    __tablename__ = "comprehensive_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        index=True,
    )
