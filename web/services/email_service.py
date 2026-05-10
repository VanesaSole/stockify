"""web/services/email_service.py

Servicio para enviar correos de recuperación.

Importante:
- Requiere configurar SMTP (variables de entorno).
- Para no frenar el desarrollo, si no hay SMTP configurado, imprimimos el link por consola.

Esto cumple el requisito de “correo automatico” en producción real; local mostrará el link.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage

from web.core.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_FROM_EMAIL,
)


def send_password_reset_email(to_email: str, reset_link: str) -> None:
    subject = "Recuperación de contraseña - Stockify"
    body = f"Hola. Usá este link para recuperar tu contraseña:\n\n{reset_link}\n\nSi no solicitaste este cambio, ignorá este mensaje."

    # Modo desarrollo si no hay SMTP.
    if not SMTP_HOST or not SMTP_USERNAME or not SMTP_PASSWORD:
        print("[DEV EMAIL] To:", to_email)
        print("[DEV EMAIL] Subject:", subject)
        print("[DEV EMAIL] Body:", body)
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

