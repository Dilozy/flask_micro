import os

from flask import Flask
from dotenv import load_dotenv

from .extensions import db, migrate
from .api import recieved_items_bp


load_dotenv()


def generate_db_uri():
    db_name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    return f"postgresql://{user}:{password}@{host}/{db_name}"


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = generate_db_uri()
    app.register_blueprint(recieved_items_bp, url_prefix="/api/v1")
    
    db.init_app(app)
    migrate.init_app(app, db)

    return app
