"""The FastAPI app.

Self-hosted has one local user and no sign-in; accounts arrive with the hosted app (M5).
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from kilndesigner_api import db, schemas
from kilndesigner_api.jobs import ArqRunner, InlineRunner, JobRunner
from kilndesigner_api.routes import InvalidDesignError, router
from kilndesigner_api.settings import Settings, get_settings


async def _invalid_design(_: Request, e: Exception) -> JSONResponse:
    assert isinstance(e, InvalidDesignError)
    body = schemas.InvalidDesign(detail=e.problems)
    return JSONResponse(body.model_dump(), status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)


def create_app(settings: Settings | None = None, runner: JobRunner | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        engine = db.make_engine(settings.database_url)
        sessions = db.make_sessions(engine)
        app.state.settings, app.state.sessions = settings, sessions
        if runner is not None:
            app.state.runner = runner
        elif settings.jobs == "inline":
            app.state.runner = InlineRunner(sessions, settings.data_dir)
        else:
            app.state.runner = await ArqRunner.connect(settings.redis_url)
        yield
        await app.state.runner.close()
        await engine.dispose()

    app = FastAPI(title="Kilndesigner", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(InvalidDesignError, _invalid_design)
    app.include_router(router)
    return app


def run() -> None:
    import uvicorn

    uvicorn.run("kilndesigner_api.main:create_app", factory=True, port=8000, reload=True)
