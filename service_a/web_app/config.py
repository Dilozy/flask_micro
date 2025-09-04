import os


class BaseConfig:
    RABBIT_HOST = "rabbitmq"
    RABBIT_USER = os.getenv("RABBIT_USER")
    RABBIT_PASS = os.getenv("RABBIT_PASS")
    CELERY_CONF = {
        "broker_url": f"amqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASS')}@{RABBIT_HOST}:5672//",
        "task_ignore_result": True,
    }
    SERVICE_A_TASKS_QUEUE = "service_a_tasks"
    BEAT_SCHEDULE = {
        "check-unprocessed-outbox-events-every-10-seconds": {
            "task": "web_app.tasks.check_unprocessed_outbox_events",
            "schedule": int(os.getenv("CHECK_OUTBOX_EVENTS_EVERY", "10")),
            "options": {"queue": SERVICE_A_TASKS_QUEUE},
        },
    }
    CREATE_ITEM_EVENTS_EXCHANGE = "create_item_events_exchange"
    CREATE_ITEM_EVENTS_ROUTING_KEY = "create_item_event"
    IS_EXCHANGE_DURABLE = True
    IS_QUEUE_DURABLE = True
    IS_QUEUE_AUTO_DELETE = False
    IS_EXCHANGE_AUTO_DELETE = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    CREATE_ITEM_EVENTS_EXCHANGE = "create_item_events_exchange_test"
    CREATE_ITEM_EVENTS_ROUTING_KEY = "create_item_even_test"
    CREATE_ITEM_EVENTS_QUEUE = "create_item_events_queue_test"
    IS_EXCHANGE_DURABLE = False
    IS_EXCHANGE_AUTO_DELETE = True
    IS_QUEUE_DURABLE = False
    IS_QUEUE_AUTO_DELETE = True
