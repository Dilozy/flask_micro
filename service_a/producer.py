import os
import logging
from contextlib import contextmanager

import pika


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageProducer:
    def __init__(self):
        self.params = pika.ConnectionParameters(
            host="rabbitmq",
            credentials=pika.PlainCredentials(
                username=os.getenv("RABBIT_USER"),
                password=os.getenv("RABBIT_PASS")
            )
        )

    @contextmanager
    def channel(self):
        connection = pika.BlockingConnection(self.params)
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange="create_item_events_exchange",
                exchange_type="direct",
                durable=True,
                auto_delete=False
            )
            yield channel
        finally:
            connection.close()

    def produce_event_message(self, event_payload):
        with self.channel() as ch:
            logger.info("Creating connection with RabbitMQ")

            ch.basic_publish(
                exchange="create_item_events_exchange",
                routing_key="create_item_event",
                body=event_payload
            )

            logger.info("New event message has been published")
