from flask import Flask

from web_app.extensions import db, migrate
from web_app.api import recieved_items_bp
from web_app.config import DevelopmentConfig
from web_app.consumer import start_message_consumer


def create_app(config_class=DevelopmentConfig):
    app = Flask("service_b")
    app.config.from_object(config_class)
    app.register_blueprint(recieved_items_bp, url_prefix="/api/v1")
    
    db.init_app(app)
    migrate.init_app(app, db)
    start_message_consumer(app)
    return app
