from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "cambiar-esta-clave-en-produccion"

    DATABASE_DIR = BASE_DIR / "database"
    REMITOS_DIR = BASE_DIR / "remitos"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_DIR / 'stockify.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False