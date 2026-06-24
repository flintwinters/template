from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.backend.database import initialize_database

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "dist" / "frontend"
STATIC_DIST = FRONTEND_DIST / "static"
INDEX_HTML = FRONTEND_DIST / "index.html"


def create_app() -> FastAPI:
    initialize_database()

    app = FastAPI(title="{{ project_title }}")

    if STATIC_DIST.exists():
        app.mount("/static", StaticFiles(directory=STATIC_DIST), name="static")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str) -> FileResponse:
        if INDEX_HTML.exists():
            return FileResponse(INDEX_HTML)

        fallback = PROJECT_ROOT / "src" / "frontend" / "index.html"
        return FileResponse(fallback)

    return app


app = create_app()
