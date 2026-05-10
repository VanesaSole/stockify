"""web/core/config.py

Carga de configuración para la app.

- Usamos variables de entorno para no hardcodear secretos.
- SECRET_KEY para firma (si más adelante usás JWT).
- Config de SMTP para enviar correos de recuperación.

Para desarrollo local:
- Pueden dejarse valores por defecto y reemplazar en .env si lo desean.
"""

import os


def _env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


# Clave para tokens/firmas.
SECRET_KEY = _env("SECRET_KEY", "dev-secret-change-me")

# Duración de tokens de recuperación (segundos).
PASSWORD_RESET_TTL_SECONDS = int(_env("PASSWORD_RESET_TTL_SECONDS", "3600"))

# SMTP (deben configurarlo con su proveedor de correo).
SMTP_HOST = _env("SMTP_HOST", "")
SMTP_PORT = int(_env("SMTP_PORT", "587"))
SMTP_USERNAME = _env("SMTP_USERNAME", "")
SMTP_PASSWORD = _env("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = _env("SMTP_FROM_EMAIL", SMTP_USERNAME or "")

