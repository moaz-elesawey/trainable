from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config=None) -> Flask:
    """Flask App Factory"""

    app = Flask(__name__)

    if not config:
        raise ValueError("app config is not defined")

    app.config.from_object(config)

    # Initialize extentions
    initialize_app_extentions(app=app)

    # Register SQLAlchemy Events Listener
    from . import events

    events.register_sa_events()

    # Register Blueprints
    register_app_blueprints(app=app)

    # Configure application logger
    configure_app_logger(app=app)

    return app


def initialize_app_extentions(app: Flask) -> None:
    """Initialize Flask application extentions"""

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"


def register_app_blueprints(app: Flask) -> None:
    """Register Blueprints"""

    from .routes import admin, auth, base, staff

    # Register Blueprints
    app.register_blueprint(base.bp, url_prefix="/")
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(staff.bp, url_prefix="/staff")


def configure_app_logger(app: Flask) -> None:
    """Configure Flask application logger"""
    _app = app
