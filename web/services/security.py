"""web/services/security.py

Funciones de seguridad:
- Hash de contraseñas.
- Generación/hasheado de tokens para recuperación.

Usamos passlib (bcrypt) para el hash de contraseñas.
"""

from __future__ import annotations

import secrets
import hashlib

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def generate_reset_token() -> str:
    # Token aleatorio (URL-safe).
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    # Hasheamos para guardarlo en DB.
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

