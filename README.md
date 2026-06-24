# {{ project_title }}

{{ project_description }}

This project was generated from a compact production template for AI-assisted
application work. It combines FastAPI, Uvicorn reload, SQLite, SQLAlchemy,
Alembic, TypeScript, ESLint, and a high-contrast dark gruvbox frontend.

## First Setup

Run the interactive setup script once after cloning the template:

```sh
python3 setup.py
```

The script renders Jinja-style project placeholders, runs `uv venv`, runs
`uv sync`, optionally installs frontend dependencies with `npm install`, and
then removes itself.

## Commands

Install Python dependencies:

```sh
uv sync
```

Install frontend dependencies:

```sh
npm install
```

Run the full build and test route:

```sh
uv run python build.py
```

Compile frontend assets only:

```sh
npm run build
```

Start the development server:

```sh
python3 main.py --port 8000
```

The server runs `src.backend.app:app` with aggressive reload coverage for the
source, migration, script, and test directories.

## Runtime

The backend exposes:

- `GET /health` for operational checks.
- Static frontend assets from `dist/frontend` after TypeScript compilation.
- `database.db` as the local SQLite database target.

The editable frontend source lives in `src/frontend`. TypeScript compiles ahead
of time into `dist/frontend/static/app.js`, while `src/frontend/style.css`
stays separate for direct human editing.

## Database

Use SQLAlchemy models with `src.backend.database.Base`. Schema changes should be
made with Alembic revisions under `migrations/versions`.

Create a revision:

```sh
uv run alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```sh
uv run alembic upgrade head
```

Do not mutate schema with one-off scripts when a migration is the correct
artifact.

## Layout

```text
main.py                  Uvicorn CLI entrypoint
setup.py                 One-time interactive template setup script
build.py                 Repeatable build and test command
database.db              Local SQLite database
src/backend/             FastAPI, SQLAlchemy, and backend modules
src/frontend/            TypeScript, HTML, and CSS source
migrations/              Alembic migration environment
tests/                   Formal backend tests
```
