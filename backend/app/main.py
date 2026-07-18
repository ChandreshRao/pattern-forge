from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import init_db
from app.routes import campaigns, health, progress, quests, submit


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="PatternForge API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(campaigns.router)
    app.include_router(quests.router)
    app.include_router(progress.router)
    app.include_router(submit.router)

    @app.on_event("startup")
    def _startup() -> None:
        init_db()

    return app


app = create_app()
