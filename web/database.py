# app/database.py
# Capa de acceso a datos.
# Para migrar a PostgreSQL: cambiar sqlite3 por psycopg2
# y ajustar los placeholders de ? a %s.

import sqlite3
import os
from flask import g, current_app


# -------------------------------------------------------
# CONEXIÓN
# -------------------------------------------------------

def get_db():
    """Retorna la conexión de la request actual (patrón g de Flask)."""

    if "db" not in g:
        db_url = current_app.config["DATABASE_URL"]

        # Soporta "sqlite:///ruta.db" o ruta directa
        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "")
        else:
            db_path = db_url

        # Si no es absoluta, resolverla desde la raíz del proyecto
        if not os.path.isabs(db_path):
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                db_path
            )

        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # permite acceso por columna nombre

    return g.db


def close_db(e=None):
    """Cierra la conexión al final de la request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


# -------------------------------------------------------
# INIT DB
# -------------------------------------------------------

def init_db():
    """Crea las tablas si no existen. Idempotente."""

    db_url = current_app.config["DATABASE_URL"]
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
    else:
        db_path = db_url

    if not os.path.isabs(db_path):
        db_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            db_path
        )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # --- USUARIOS ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT    NOT NULL,
            email     TEXT    UNIQUE NOT NULL,
            password  TEXT    NOT NULL,
            direccion TEXT,
            telefono  TEXT,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --- CATÁLOGO / PRODUCTOS ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id  INTEGER NOT NULL,
            nombre      TEXT    NOT NULL,
            p_costo     REAL    DEFAULT 0,
            p_venta     REAL    DEFAULT 0,
            p_mayoreo   REAL    DEFAULT 0,
            stock       REAL    DEFAULT 0,
            activo      INTEGER DEFAULT 1,
            creado_en   DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    # --- PEDIDOS (cabecera) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            modo       TEXT    NOT NULL DEFAULT 'PEDIDO',
            cliente    TEXT,
            direccion  TEXT,
            estado     TEXT    DEFAULT 'borrador',
            total      REAL    DEFAULT 0,
            creado_en  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    # --- ÍTEMS DE PEDIDO (detalle) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id   INTEGER NOT NULL,
            producto_id INTEGER,
            nombre      TEXT    NOT NULL,
            cantidad    REAL    NOT NULL,
            p_costo     REAL    DEFAULT 0,
            p_venta     REAL    DEFAULT 0,
            p_mayoreo   REAL    DEFAULT 0,
            total       REAL    DEFAULT 0,
            FOREIGN KEY (pedido_id)   REFERENCES pedidos(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    conn.commit()
    conn.close()

    # Registrar cierre de conexión g
    current_app.teardown_appcontext(close_db)