from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config/config.py')

    db.init_app(app)

    with app.app_context():
        from .home import home
        from .query_execution_loader import query_execution_loader_controller
        migrate = Migrate(app, db)

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(query_execution_loader_controller.query_execution_loader_bp)

        return app
