from typing import Tuple

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_flask_app() -> Flask:
    """Construct core Flask application."""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    return app


def init_db_migrate(app: Flask) -> Tuple[SQLAlchemy, Migrate]:
    """Initializes and returns the database and migration class"""
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    return db, migrate


def attach_dash_app(app) -> Flask:
    """Attaches the Dash dashboard to Flask app (not 100% sure how it works though)"""
    with app.app_context():
        from . import models, routes
        from .plotlydash.dashboard import init_dashboard

        app = init_dashboard(app)
        return app  # type:ignore


app = init_flask_app()
db, migrate = init_db_migrate(app)
app = attach_dash_app(app)
