import logging

from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.db import (
    check_db_connection,
    create_engine_from_settings,
    create_sessionmaker,
    init_db_schema,
)
from app.routers.students import router as students_router

app = FastAPI()

logger = logging.getLogger(__name__)


@app.on_event("startup")
def on_startup() -> None:
    settings = get_settings()
    app.state.settings = settings
    logging.basicConfig(level=settings.log_level)
    logger.info("Starting app env=%s log_level=%s", settings.app_env, settings.log_level)
    if settings.database_url:
        engine = create_engine_from_settings(settings)
        app.state.db_engine = engine
        app.state.db_sessionmaker = create_sessionmaker(engine)
        if settings.app_env == "local":
            init_db_schema(engine)
    else:
        app.state.db_sessionmaker = None

@app.get("/health")
def health():
    return {"ok": True}


@app.get("/health/db")
def health_db():
    settings = app.state.settings
    if not settings.database_url:
        raise HTTPException(status_code=503, detail="DATABASE_URL not configured")

    engine = getattr(app.state, "db_engine", None)
    if engine is None:
        engine = create_engine_from_settings(settings)
        app.state.db_engine = engine

    check_db_connection(engine)
    return {"ok": True}


app.include_router(students_router)