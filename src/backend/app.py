from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.backend.agent_tools_index import ToolIndexResponse, build_tool_index
from src.backend.database import initialize_database

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "dist" / "frontend"
STATIC_DIST = FRONTEND_DIST / "static"
FRONTEND_SOURCE = PROJECT_ROOT / "src" / "frontend"


def frontend_asset(name: str) -> Path:
    built_asset = FRONTEND_DIST / name
    return built_asset if built_asset.exists() else FRONTEND_SOURCE / name


def create_app() -> FastAPI:
    initialize_database()

    app = FastAPI(title="{{ project_title }}")

    if STATIC_DIST.exists():
        app.mount("/static", StaticFiles(directory=STATIC_DIST), name="static")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/agent/tools", response_model=ToolIndexResponse)
    def tools() -> ToolIndexResponse:
        return build_tool_index(app.openapi())

    @app.get("/favicon.ico", include_in_schema=False)
    @app.get("/favicon.png", include_in_schema=False)
    def favicon() -> FileResponse:
        return FileResponse(frontend_asset("favicon.png"), media_type="image/png")

    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str) -> FileResponse:
        return FileResponse(frontend_asset("index.html"))

    return app


app = create_app()
