"""Deploy AthenaHero."""
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
logging.basicConfig(level=logging.INFO)

# TODO:
# write tests


def create_app(config_file="config/config.py"):
    """Athenahero Flask App factory."""
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    db.app = app

    with app.app_context():
        from .home import home
        from .query_execution_loader import query_execution_loader

        migrate = Migrate(app, db)  # noqa: F841

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        # Register Jobs
        query_execution_loader.register_query_execution_job()

        return app
