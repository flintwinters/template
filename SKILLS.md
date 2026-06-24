# Skills

Use this file as the project-level operating guide for AI coding agents.

## Core Practice

- Make small, coherent changes.
- Keep commits focused to one file when practical.
- Prefer existing modules before adding new abstractions.
- Preserve the public user flow when changing backend internals.
- Use `uv run python build.py` as the repeatable verification route.

## Frontend

- Keep the UI high-contrast dark gruvbox.
- Use `src/frontend/style.css` for human-editable styling.
- Compile TypeScript ahead of time with `npm run build`.
- Avoid animations, transitions, noisy borders, nested cards, and unnecessary
  labels.
- Keep UI dense, stable, responsive, and free of implementation details.

## Backend

- Run the app with `python3 main.py --port 8000`.
- Keep `/health` cheap, public, and stable.
- Use `src.backend.database` for database URL, engine, and metadata.
- Use Alembic for schema changes rather than ad hoc migrations.
- Keep blocking work out of user-facing request paths.

## Database

- Store local development data in `database.db`.
- Add SQLAlchemy models against `Base` from `src.backend.database`.
- Generate migrations into `migrations/versions`.
- Review generated migrations before applying them.
