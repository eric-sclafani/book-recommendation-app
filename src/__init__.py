from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_flask_app() -> Flask:
    """Construct core Flask application."""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    return app


def attach_dash_app(app) -> Flask:
    """Attaches the Dash dashboard to Flask app (not 100% sure how it works though)"""
    with app.app_context():
        from . import models, routes
        from .plotlydash.dashboard import init_dashboard

        app = init_dashboard(app)
        return app  # type:ignore


app = init_flask_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"  # tells flask which view function handles logins
app = attach_dash_app(app)
