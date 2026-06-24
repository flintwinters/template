# Project Map

This template is organized around a small full-stack application skeleton for
AI-assisted coding projects.

## Root

- `main.py`: CLI entrypoint that starts Uvicorn.
- `build.py`: repeatable build and test entrypoint.
- `database.db`: local SQLite database file.
- `pyproject.toml`: Python package metadata and dependencies.
- `uv.lock`: resolved Python dependency graph.
- `package.json`: frontend scripts and development dependencies.
- `package-lock.json`: resolved frontend dependency graph.
- `tsconfig.json`: TypeScript compiler configuration.
- `eslint.config.js`: frontend TypeScript lint configuration.
- `alembic.ini`: Alembic configuration.
- `README.md`: setup, runtime, and workflow documentation.
- `AGENTS.md`: repository-specific agent directives.
- `SKILLS.md`: this project structure map.

## Backend

- `src/backend/app.py`: FastAPI application factory, `/health` endpoint, and
  frontend asset serving.
- `src/backend/database.py`: SQLite path, SQLAlchemy URL, declarative metadata,
  engine creation, and database initialization.

## Frontend

- `src/frontend/index.html`: browser document shell.
- `src/frontend/app.ts`: TypeScript browser entrypoint.
- `src/frontend/style.css`: human-editable stylesheet.

## Database Migrations

- `migrations/env.py`: Alembic migration runtime wired to backend metadata.
- `migrations/versions/`: generated schema revisions.

## Tests

- `tests/test_health.py`: formal backend health endpoint test.

## Generated Output

- `dist/frontend/`: compiled frontend output produced by `npm run build`.
- `node_modules/`: installed frontend dependencies.
- `.venv/`: local Python environment managed by `uv`.
