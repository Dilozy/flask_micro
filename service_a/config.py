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


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = DatabaseURI().get_uri()


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = DatabaseURI(DB_NAME="flask_micro_test_db").get_uri()
    TESTING = True


class CeleryConfig:
    broker_url = f'amqp://{os.getenv("RABBIT_USER")}:{os.getenv("RABBIT_PASS")}@rabbitmq:5672//'
    result_backend = f'redis://redis:6379/{os.getenv("SERVICE_A_REDIS_DB")}'


class CeleryBeatConfig:
    BEAT_SCHEDULE = {
        "check-unprocessed-outbox-events-every-10-seconds": {
        "task": "tasks.check_unprocessed_outbox_events",
        "schedule": int(os.getenv("CHECK_OUTBOX_EVENTS_EVERY", 10)),
        "options": {"queue": "service_a_tasks"}
        },
    }