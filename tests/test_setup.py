from __future__ import annotations

import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

import setup


@pytest.fixture
def project_directory(monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    tests_directory = Path(__file__).resolve().parent

    with tempfile.TemporaryDirectory(dir=tests_directory) as temporary_directory:
        project_root = Path(temporary_directory)
        monkeypatch.setattr(setup, "PROJECT_ROOT", project_root)
        yield project_root


def test_collect_context_only_targets_project_title(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(setup, "prompt", lambda label, default: "Example Service")

    assert setup.collect_context() == {"project_title": "Example Service"}


def test_render_text_preserves_deferred_template_slots(
    project_directory: Path,
) -> None:
    template = project_directory / "settings.txt"
    template.write_text(
        "{{ project_title }}|{{project_slug}}|{{ microservice_dir }}|"
        "{{ service_port }}\n"
    )

    changed = setup.render_text(template, {"project_title": "Example Service"})

    assert changed is True
    assert template.read_text() == (
        "Example Service|{{project_slug}}|{{ microservice_dir }}|"
        "{{ service_port }}\n"
    )


def test_service_file_is_renamed_and_selectively_rendered(
    project_directory: Path,
) -> None:
    source = project_directory / "microservice.service"
    source.write_text(
        "Description={{ project_title }}\n"
        "WorkingDirectory={{ microservice_dir }}\n"
        "ExecStart=uv run main.py --port {{ service_port }}\n"
    )

    destination = setup.rename_service_file("Example Service")
    changed = setup.render_text(destination, {"project_title": "Example Service"})

    assert destination == project_directory / "Example Service.service"
    assert changed is True
    assert not source.exists()
    assert destination.read_text() == (
        "Description=Example Service\n"
        "WorkingDirectory={{ microservice_dir }}\n"
        "ExecStart=uv run main.py --port {{ service_port }}\n"
    )


def test_service_file_rename_refuses_to_overwrite_existing_file(
    project_directory: Path,
) -> None:
    (project_directory / "microservice.service").touch()
    (project_directory / "Example Service.service").touch()

    with pytest.raises(FileExistsError, match="Service file already exists"):
        setup.rename_service_file("Example Service")
