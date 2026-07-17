from __future__ import annotations

import sys

import pytest

import main


def run_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setattr(main.uvicorn, "run", lambda *args, **kwargs: None)
    main.main()


def test_main_uses_polling_reload_backend_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("WATCHFILES_FORCE_POLLING", raising=False)

    run_main(monkeypatch)

    assert main.os.environ["WATCHFILES_FORCE_POLLING"] == "true"


def test_main_preserves_explicit_reload_backend_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WATCHFILES_FORCE_POLLING", "false")

    run_main(monkeypatch)

    assert main.os.environ["WATCHFILES_FORCE_POLLING"] == "false"
