import threading

from flask import Flask
from web_app.api import recieved_items_bp
from web_app.config import DevelopmentConfig
from web_app.consumer import MessageConsumer
from web_app.extensions import db, migrate


def create_app(config_class=DevelopmentConfig):
    app = Flask("service_b")
    app.config.from_object(config_class)
    app.register_blueprint(recieved_items_bp, url_prefix="/api/v1")

    db.init_app(app)
    migrate.init_app(app, db)
    start_message_consumer(app)
    return app


def start_message_consumer(app):
    def consumer_with_context():
        with app.app_context():
            message_consumer = MessageConsumer()
            message_consumer.consume_create_item_event_messages()

    thread = threading.Thread(target=consumer_with_context, daemon=True)
    thread.start()
