from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db import init_db
from app.routes import auth, campaigns, health, progress, quests, submit


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
    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(campaigns.router, prefix="/api")
    app.include_router(quests.router, prefix="/api")
    app.include_router(progress.router, prefix="/api")
    app.include_router(submit.router, prefix="/api")

    static_root = settings.static_root
    if static_root is not None:
        static_dir = Path(static_root)
        if static_dir.is_dir():
            assets = static_dir / "assets"
            if assets.is_dir():
                app.mount("/assets", StaticFiles(directory=assets), name="assets")

            @app.get("/{full_path:path}")
            async def spa_fallback(full_path: str) -> FileResponse:
                # API is already registered above; this catches client-side routes.
                candidate = static_dir / full_path
                if full_path and candidate.is_file():
                    return FileResponse(candidate)
                return FileResponse(static_dir / "index.html")

    @app.on_event("startup")
    def _startup() -> None:
        init_db()

    return app


app = create_app()
