"""web/db/session.py

Inicialización de la base de datos (SQLite) y creación de sesión.

- SQLAlchemy 2.x con Engine + sessionmaker.
- init_db() crea tablas si no existen.
"""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from web.db.models import Base


DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./stockify.db")


engine = create_engine(
    DB_PATH,
    connect_args={"check_same_thread": False} if DB_PATH.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Crea las tablas en la DB si no existen."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency de FastAPI para obtener una sesión."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

