"""web/routes/auth.py

Rutas de autenticación:
- GET/POST /login
- GET/POST /register
- GET/POST /forgot-password
- GET/POST /reset-password

Para mantener el ejemplo simple:
- El login exitoso devuelve un mensaje y (opcional) un cookie.

Si querés que el sitio complete flujo con cookies/JWT, lo extendemos luego.
"""

from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from web.core.config import SECRET_KEY, PASSWORD_RESET_TTL_SECONDS
from web.db.session import get_db
from web.db.models import User, PasswordResetToken
from web.services.security import (
    hash_password,
    verify_password,
    generate_reset_token,
    hash_token,
)
from web.services.email_service import send_password_reset_email

from sqlalchemy.orm import Session


router = APIRouter(prefix="")

templates = Jinja2Templates(directory="web/templates")


@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})


@router.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Credenciales inválidas."},
        )

    if not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Credenciales inválidas."},
        )

    # Nota: Para este primer armado estructural, no implementamos sesión/cookies.
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "" , "success": f"Bienvenido/a, {user.name}!"},
    )


@router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": ""})


@router.post("/register", response_class=HTMLResponse)
def register_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db),
):
    name = name.strip()
    email_norm = email.strip().lower()
    address = address.strip()
    phone = phone.strip()

    if not name or not email_norm or not password:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Faltan datos."})

    if password != password_confirm:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Las contraseñas no coinciden."})

    existing = db.query(User).filter(User.email == email_norm).first()
    if existing:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Ya existe un usuario con ese mail."})

    user = User(
        name=name,
        email=email_norm,
        password_hash=hash_password(password),
        address=address,
        phone=phone,
    )
    db.add(user)
    db.commit()

    return templates.TemplateResponse("register.html", {"request": request, "error": "", "success": "Cuenta creada. Ahora inicia sesión."})


@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_get(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request, "message": ""})


@router.post("/forgot-password", response_class=HTMLResponse)
def forgot_post(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    email_norm = email.strip().lower()
    user = db.query(User).filter(User.email == email_norm).first()

    # Mensaje genérico para evitar enumeración de usuarios.
    if user:
        reset_token = generate_reset_token()
        reset_token_hash = hash_token(reset_token)

        expires_at = dt.datetime.utcnow() + dt.timedelta(seconds=PASSWORD_RESET_TTL_SECONDS)

        token_row = PasswordResetToken(
            user_id=user.id,
            token_hash=reset_token_hash,
            expires_at=expires_at,
        )
        db.add(token_row)
        db.commit()

        # Link de reset (ajustar host si hace falta).
        reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
        send_password_reset_email(user.email, reset_link)

    return templates.TemplateResponse(
        "forgot_password.html",
        {"request": request, "message": "Si el mail existe, recibirás instrucciones para recuperar la contraseña."},
    )


@router.get("/reset-password", response_class=HTMLResponse)
def reset_get(request: Request, token: str = ""):
    return templates.TemplateResponse(
        "reset_password.html",
        {"request": request, "error": "", "token": token},
    )


@router.post("/reset-password", response_class=HTMLResponse)
def reset_post(
    request: Request,
    token: str = Form(...),
    new_password: str = Form(...),
    new_password_confirm: str = Form(...),
    db: Session = Depends(get_db),
):
    if new_password != new_password_confirm:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Las contraseñas no coinciden.", "token": token},
        )

    token_hash = hash_token(token)
    token_row = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == token_hash)
        .order_by(PasswordResetToken.id.desc())
        .first()
    )

    if not token_row:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Token inválido.", "token": token},
        )

    if token_row.used_at is not None:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Este token ya fue utilizado.", "token": token},
        )

    if token_row.expires_at < dt.datetime.utcnow():
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Token expirado.", "token": token},
        )

    user = token_row.user
    user.password_hash = hash_password(new_password)
    token_row.used_at = dt.datetime.utcnow()
    db.add(user)
    db.add(token_row)
    db.commit()

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "", "success": "Contraseña actualizada. Iniciá sesión."},
    )

