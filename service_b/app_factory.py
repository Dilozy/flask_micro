from flask import Flask

from extensions import db, migrate
from api import recieved_items_bp
from config import DevelopmentConfig
from consumer import start_message_consumer


def create_app(config_class=DevelopmentConfig):
    app = Flask("service_b")
    app.config.from_object(config_class)
    app.register_blueprint(recieved_items_bp, url_prefix="/api/v1")
    
    db.init_app(app)
    migrate.init_app(app, db)
    start_message_consumer(app)
    return app
