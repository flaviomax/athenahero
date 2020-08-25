import os

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/athenahero"
SQLALCHEMY_TRACK_MODIFICATIONS = False

ATHENAHERO_USERNAME = os.environ.get("ATHENAHERO_USERNAME")
ATHENAHERO_PASSWORD = os.environ.get("ATHENAHERO_PASSWORD")
