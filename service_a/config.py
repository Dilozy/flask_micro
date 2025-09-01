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
    CELERY_CONF = dict(
        broker_url=f'amqp://{os.getenv("RABBIT_USER")}:{os.getenv("RABBIT_PASS")}@{RABBIT_HOST}:5672//',
        task_ignore_result=True
        )
    SERVICE_A_TASKS_QUEUE= "service_a_tasks"
    BEAT_SCHEDULE = {
        "check-unprocessed-outbox-events-every-10-seconds": {
        "task": "tasks.check_unprocessed_outbox_events",
        "schedule": int(os.getenv("CHECK_OUTBOX_EVENTS_EVERY", 10)),
        "options": {"queue": SERVICE_A_TASKS_QUEUE}
        },
    }
    CREATE_ITEM_EVENTS_EXCHANGE = "create_item_events_exchange"
    CREATE_ITEM_EVENTS_ROUTING_KEY = "create_item_event"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DatabaseURI().get_uri()


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DatabaseURI(DB_NAME="flask_micro_test_db").get_uri()
    TESTING = True
