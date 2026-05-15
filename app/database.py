# database.py

import sqlite3


DB_NAME = "stockify.db"


# =====================================================
# CONEXION
# =====================================================

def conectar():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    return conn, cursor


# =====================================================
# CREAR TABLAS
# =====================================================

def crear_tablas():

    conn, cursor = conectar()

    # -------------------------------------------------
    # TABLA USUARIOS
    # -------------------------------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        direccion TEXT,

        telefono TEXT

    )

    """)

    conn.commit()

    conn.close()