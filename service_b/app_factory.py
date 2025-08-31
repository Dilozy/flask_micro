import threading

from flask import Flask

from extensions import db, migrate
from api import recieved_items_bp
from config import DevelopmentConfig
from consumer import MessageConsumer


def create_app(config_class=DevelopmentConfig):
    app = Flask("service_b")
    app.config.from_object(config_class)
    app.register_blueprint(recieved_items_bp, url_prefix="/api/v1")
    
    db.init_app(app)
    migrate.init_app(app, db)

    def consumer_with_context():
        with app.app_context():
            message_consumer = MessageConsumer()
            message_consumer.consume_create_item_event_messages()
    
    thread = threading.Thread(
        target=consumer_with_context,
        daemon=True
    )
    thread.start()

    app.logger.info("RabbitMQ consumer started in background thread")

    return app
