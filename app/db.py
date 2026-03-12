from __future__ import annotations

from fastapi import HTTPException, Request, status
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings


def create_engine_from_settings(settings: Settings) -> Engine:
    if not settings.database_url:
        raise ValueError("DATABASE_URL is not configured")
    return create_engine(settings.database_url, pool_pre_ping=True)


def check_db_connection(engine: Engine) -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def init_db_schema(engine: Engine) -> None:
    from app.models import Base

    Base.metadata.create_all(engine)


def create_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db(request: Request):
    session_maker = getattr(request.app.state, "db_sessionmaker", None)
    if session_maker is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="DATABASE_URL not configured",
        )

    db: Session = session_maker()
    try:
        yield db
    finally:
        db.close()
