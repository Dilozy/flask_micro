from flask import Flask

from .extensions import db, migrate
from .api import items_bp
from .config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(items_bp, url_prefix="/api/v1")
    
    db.init_app(app)
    migrate.init_app(app, db)

    return app