import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
logging.basicConfig(level=logging.INFO)

# TODO:
# basic auth
# write tests

def create_app(config_file='config/config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    db.app = app

    with app.app_context():
        from .database.models import query_execution
        from .home import home
        from .query_execution_loader import query_execution_loader
        migrate = Migrate(app, db)

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        # TODO: make this download the last 30 dyas when app is started, considering it may have already been done
        query_execution_loader.register_query_execution_job()

        return app
