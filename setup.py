from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SKIPPED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
}
SKIPPED_SUFFIXES = {".db", ".pyc", ".sqlite", ".sqlite3"}
PLACEHOLDER_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")


def title_from_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_\s]+", value) if part)


def normalize_slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

    if not normalized:
        raise ValueError("Project slug cannot be empty.")

    return normalized


def prompt(label: str, default: str) -> str:
    response = input(f"{label} [{default}]: ").strip()
    return response or default


def prompt_yes_no(label: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"

    while True:
        response = input(f"{label} [{suffix}]: ").strip().lower()

        if not response:
            return default

        if response in {"y", "yes"}:
            return True

        if response in {"n", "no"}:
            return False

        print("Enter yes or no.")


def collect_context() -> dict[str, str | bool]:
    default_slug = normalize_slug(PROJECT_ROOT.name)
    default_title = title_from_slug(default_slug)

    project_title = prompt("Project title", default_title)
    project_slug = normalize_slug(prompt("Python project slug", default_slug))
    npm_package_name = normalize_slug(prompt("NPM package name", project_slug))
    description = prompt(
        "Project description",
        f"{project_title} application built from the AI coding template.",
    )
    install_frontend = prompt_yes_no("Install frontend dependencies with npm install")

    return {
        "project_title": project_title,
        "project_slug": project_slug,
        "npm_package_name": npm_package_name,
        "project_description": description,
        "install_frontend": install_frontend,
    }


def should_skip(path: Path) -> bool:
    relative_parts = path.relative_to(PROJECT_ROOT).parts

    if any(part in SKIPPED_DIRECTORIES for part in relative_parts):
        return True

    return path.suffix in SKIPPED_SUFFIXES or path.name == Path(__file__).name


def render_text(path: Path, context: dict[str, str | bool]) -> bool:
    try:
        original = path.read_text()
    except UnicodeDecodeError:
        return False

    if "{{" not in original:
        return False

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)

        if key not in context:
            raise KeyError(f"Unknown template variable '{key}' in {path}")

        return str(context[key])

    rendered = PLACEHOLDER_PATTERN.sub(replace, original)

    if rendered == original:
        return False

    path.write_text(rendered)
    return True


def render_project(context: dict[str, str | bool]) -> list[Path]:
    rendered_paths: list[Path] = []

    for path in sorted(PROJECT_ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue

        if render_text(path, context):
            rendered_paths.append(path.relative_to(PROJECT_ROOT))

    return rendered_paths


def run(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def remove_setup_script() -> None:
    Path(__file__).unlink()
    print("Removed setup.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure this cloned template.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render templates and report commands without running setup commands.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    context = collect_context()

    print("\nConfiguration")
    print(f"Project title: {context['project_title']}")
    print(f"Python project slug: {context['project_slug']}")
    print(f"NPM package name: {context['npm_package_name']}")
    print(f"Description: {context['project_description']}")

    if not prompt_yes_no("Apply this setup"):
        raise SystemExit("Setup cancelled.")

    rendered_paths = render_project(context)
    print(f"Rendered {len(rendered_paths)} template files.")

    if args.dry_run:
        print("Dry run complete. setup.py was not removed.")
        return

    run(["uv", "venv"])
    run(["uv", "sync"])

    if context["install_frontend"]:
        run(["npm", "install"])

    remove_setup_script()


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error
    except KeyboardInterrupt:
        raise SystemExit("\nSetup cancelled.") from None
