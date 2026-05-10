"""web/main.py

FastAPI entrypoint para el sitio web (login/registro/recuperación).

- Server-rendered con Jinja2: renderiza HTML para login/registro/forgot/reset.
- Este archivo arma la app y monta las rutas.

Notas:
- Para correr local: uvicorn web.main:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web.db.session import init_db
from web.routes.auth import router as auth_router


app = FastAPI(title="Stockify - Auth")

# Inicializa DB al arrancar.
init_db()

# Templates (Jinja2)
templates = Jinja2Templates(directory="web/templates")

# Static (opcional: css/js/imágenes si agregás más adelante)
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Rutas
app.include_router(auth_router)


@app.get("/")
def root():
    # Redirige conceptualmente al login.
    # Para simplificar (sin redirect response), devolvemos texto.
    return {"message": "Ir a /login"}

