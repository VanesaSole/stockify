"""Application factory for the Stockify Flask app.

Provides create_app and registers extensions, blueprints, and commands.
"""

from pathlib import Path

from flask import Flask, redirect, url_for
from flask_login import current_user

from config import Config
from extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    create_required_folders(app)
    init_extensions(app)
    configure_login()
    register_blueprints(app)
    register_main_routes(app)
    register_cli_commands(app)

    return app


def create_required_folders(app):
    database_path = Path(app.config["DATABASE_DIR"])
    remitos_path = Path(app.config["REMITOS_DIR"])

    database_path.mkdir(parents=True, exist_ok=True)
    remitos_path.mkdir(parents=True, exist_ok=True)


def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def configure_login():
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Debes iniciar sesion para acceder."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        from models.usuario import Usuario

        return Usuario.query.get(int(user_id))


def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.productos import productos_bp
    from routes.pedidos import pedidos_bp
    from routes.remitos import remitos_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(remitos_bp)
    app.register_blueprint(admin_bp)


def register_main_routes(app):
    @app.route("/")
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if current_user.rol == "administrador":
            return redirect(url_for("admin.dashboard"))

        if current_user.rol == "vendedor":
            return redirect(url_for("pedidos.mis_pedidos"))

        return redirect(url_for("auth.logout"))


def register_cli_commands(app):
    @app.cli.command("init-db")
    def init_db():
        from models import (
            usuario,
            producto,
            pedido,
            detalle_pedido,
            historial_pedido,
            movimiento_stock,
            remito,
        )

        with app.app_context():
            db.create_all()
            print("Base de datos inicializada correctamente.")


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)