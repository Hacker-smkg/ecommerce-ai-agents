from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings
from app.db.models import Base

_engine = None
_session_local = None


def _is_sqlite(url: str) -> bool:
    return url.startswith("sqlite")


def get_engine():
    global _engine, _session_local
    settings = get_settings()

    if _engine is None or str(_engine.url) != settings.database_url:
        connect_args = {"check_same_thread": False} if _is_sqlite(settings.database_url) else {}
        _engine = create_engine(
            settings.database_url,
            connect_args=connect_args,
            pool_pre_ping=True,
        )
        _session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
            class_=Session,
        )
    return _engine


def get_session_local():
    if _session_local is None:
        get_engine()
    return _session_local


def init_db() -> None:
    Base.metadata.create_all(bind=get_engine())


def reset_db() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()
