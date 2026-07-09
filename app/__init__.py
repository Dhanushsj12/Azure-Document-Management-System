from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, bcrypt, migrate

from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.document import document_bp
# Import models so Flask-Migrate can detect them
from app.models.user import User


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(document_bp)
    return app