from flask import Flask

from web_app.extensions import db, migrate
from web_app.celery_app import celery_init_app
from web_app.api import items_bp
from web_app.config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask("service_a")
    app.config.from_object(config_class)
    app.register_blueprint(items_bp, url_prefix="/api/v1")
    
    db.init_app(app)
    migrate.init_app(app, db)
    celery_init_app(app)
    return app
