import os


class BaseConfig:
    RABBIT_HOST = "rabbitmq"
    CREATE_ITEM_EVENTS_EXCHANGE = "create_item_events_exchange"
    CREATE_ITEM_EVENTS_ROUTING_KEY = "create_item_event"
    CREATE_ITEM_EVENTS_QUEUE = "create_item_events_queue"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")


class TestingConfig(BaseConfig):
    TESTING = True
