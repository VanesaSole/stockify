# app/models/user.py

from ..database import get_db
import hashlib


def _hash(password: str) -> str:
    """SHA-256 simple. En producción usar bcrypt o argon2."""
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------------------------------
# CREAR USUARIO
# -------------------------------------------------------

def crear_usuario(nombre, email, password, direccion="", telefono=""):

    db = get_db()

    try:
        db.execute("""
            INSERT INTO usuarios (nombre, email, password, direccion, telefono)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, email, _hash(password), direccion, telefono))

        db.commit()
        return {"ok": True}

    except Exception as e:
        return {"error": str(e)}


# -------------------------------------------------------
# AUTENTICAR
# -------------------------------------------------------

def autenticar_usuario(email, password):

    db = get_db()

    row = db.execute("""
        SELECT * FROM usuarios
        WHERE email = ? AND password = ?
    """, (email, _hash(password))).fetchone()

    if row:
        return dict(row)

    return None


# -------------------------------------------------------
# OBTENER POR ID
# -------------------------------------------------------

def obtener_usuario(usuario_id):

    db = get_db()

    row = db.execute(
        "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
    ).fetchone()

    return dict(row) if row else None