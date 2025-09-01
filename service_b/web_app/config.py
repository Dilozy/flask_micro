import os
from dataclasses import dataclass


@dataclass
class DatabaseURI:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_NAME: str = os.getenv("DB_NAME")
    
    def get_uri(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"


class BaseConfig:
    RABBIT_HOST = "rabbitmq"
    CREATE_ITEM_EVENTS_EXCHANGE = "create_item_events_exchange"
    CREATE_ITEM_EVENTS_ROUTING_KEY = "create_item_event"
    CREATE_ITEM_EVENTS_QUEUE = "create_item_events_queue"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DatabaseURI().get_uri()


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DatabaseURI(DB_NAME=os.getenv("SERVICE_B_TEST_DB_NAME")).get_uri()
    TESTING = True
