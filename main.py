from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent
RELOAD_DIRECTORIES = (
    PROJECT_ROOT,
    PROJECT_ROOT / "src",
    PROJECT_ROOT / "src" / "backend",
    PROJECT_ROOT / "src" / "frontend",
    PROJECT_ROOT / "tests",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the AI coding template server.")
    parser.add_argument(
        "--port",
        default=8000,
        type=int,
        help="Port for the development server.",
    )
    return parser.parse_args()


def existing_reload_directories() -> list[str]:
    return [str(path) for path in RELOAD_DIRECTORIES if path.exists()]


def main() -> None:
    args = parse_args()

    uvicorn.run(
        "src.backend.app:app",
        host="127.0.0.1",
        port=args.port,
        reload=True,
        reload_dirs=existing_reload_directories(),
    )


if __name__ == "__main__":
    main()
