from __future__ import annotations

from pathlib import Path

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import DeclarativeBase

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


class Base(DeclarativeBase):
    pass


def create_database_engine() -> Engine:
    return create_engine(DATABASE_URL)


def initialize_database() -> None:
    engine = create_database_engine()

    with engine.begin() as connection:
        connection.execute(text("SELECT 1"))
