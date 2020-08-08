from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config/config.py')

    db.init_app(app)

    with app.app_context():
        from . import routes
        migrate = Migrate(app, db)

        return app
