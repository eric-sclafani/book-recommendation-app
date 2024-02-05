from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_app():
    """Construct core Flask application."""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    global db  # let models.py access db
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from . import models, routes
        from .plotlydash.dashboard import init_dashboard

        app = init_dashboard(app)
        return app
