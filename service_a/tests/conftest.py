import pytest
import pika
from flask import Flask

from web_app.app_factory import create_app
from web_app.extensions import db
from web_app.config import TestingConfig
from web_app.producer import MessageProducer


@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app: Flask):
    with app.app_context():
        yield db.session()
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def initial_items_count():
    return 0


@pytest.fixture
def rabbit_producer():
    return MessageProducer(TestingConfig)


@pytest.fixture
def rabbit_consumer_channel():
    params = pika.ConnectionParameters(
            host=TestingConfig.RABBIT_HOST,
            credentials=pika.PlainCredentials(
                username=TestingConfig.RABBIT_USER,
                password=TestingConfig.RABBIT_PASS
            )
        )
    connection = pika.BlockingConnection(params)
    try:
        channel = connection.channel()
        channel.exchange_declare(
                exchange=TestingConfig.CREATE_ITEM_EVENTS_EXCHANGE,
                exchange_type="direct",
                durable=TestingConfig.IS_EXCHANGE_DURABLE,
                auto_delete=TestingConfig.IS_EXCHANGE_AUTO_DELETE,
            )
        channel.queue_declare(TestingConfig.CREATE_ITEM_EVENTS_QUEUE,
                              exclusive=True)
        channel.queue_bind(
            queue=TestingConfig.CREATE_ITEM_EVENTS_QUEUE,
            exchange=TestingConfig.CREATE_ITEM_EVENTS_EXCHANGE,
            routing_key=TestingConfig.CREATE_ITEM_EVENTS_ROUTING_KEY
        )
        yield channel
    finally:
        connection.close()
