# {{ project_title }} Agents

## Project Goal

{{ project_title }} is a uvicorn typescript app. It should stay small, explicit,
production-oriented, and easy for both humans and agents to audit.

## Working Rules

- Make incremental changes and commit each focused file separately.
- Prefer existing source modules and shared configuration before adding new
  structure.
- Use `uv run python build.py` for the repeatable build and test route.
- Keep frontend source under `src/frontend` and backend source under
  `src/backend`.
- Keep database schema changes explicit with Alembic migrations.

## UI Rules

- Use high-contrast dark gruvbox.
- Keep `src/frontend/style.css` separate and directly editable.
- Do not use animations or transitions.
- Avoid noisy borders, nested cards, and unnecessary labels.
- Keep screens dense, responsive, and stable at narrow widths.

## Runtime Rules

- `python3 main.py --port 8000` starts Uvicorn with reload enabled.
- Development reloads use watchfiles polling by default to avoid dependence on
  shared host inotify limits; set `WATCHFILES_FORCE_POLLING=false` to opt into
  native filesystem notifications.
- `/health` is the public operational endpoint.
- `src/frontend/favicon.png` is the single replaceable favicon source served at
  both `/favicon.png` and `/favicon.ico`.
- TypeScript must be compiled ahead of time before serving production assets.
- Do not expose database IDs or implementation details in user-facing UI.

## Setup State

- The initial `setup.py` pass applies only `{{ project_title }}` and preserves
  every other template slot for later routines.
- Setup renames `microservice.service` to `{{ project_title }}.service` before
  rendering its description.
- `{{ microservice_dir }}` and `{{ service_port }}` remain deferred service
  configuration inputs after initial setup.
