"""web/db/models.py

Modelos SQLAlchemy para la tabla de usuarios y tokens de recuperación.

Requisitos:
- Login con mail + contraseña.
- Registro: nombre, mail, contraseña (confirmación), dirección, teléfono.
- Recuperación: generar token, enviarlo por mail y permitir reset.

Se guardan:
- password_hash: hash seguro de la contraseña.
- PasswordResetToken: token con expiración (guardamos token hasheado).
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import String, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    address: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)

    reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Token hasheado para no guardar el token en texto plano.
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)
    expires_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)

    user = relationship("User", back_populates="reset_tokens")

