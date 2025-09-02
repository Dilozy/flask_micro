import logging
from contextlib import contextmanager
import json

import pika


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageProducer:
    def __init__(self, config):
        self.config = config
        self.params = pika.ConnectionParameters(
            host=self.config.RABBIT_HOST,
            credentials=pika.PlainCredentials(
                username=self.config.RABBIT_USER,
                password=self.config.RABBIT_PASS
            )
        )

    @contextmanager
    def channel(self):
        connection = pika.BlockingConnection(self.params)
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.config.CREATE_ITEM_EVENTS_EXCHANGE,
                exchange_type="direct",
                durable=self.config.IS_EXCHANGE_DURABLE,
                auto_delete=self.config.IS_EXCHANGE_AUTO_DELETE
            )
            yield channel
        finally:
            connection.close()

    def produce_event_message(self, event_payload):        
        with self.channel() as ch:
            logger.info("Creating connection with RabbitMQ")

            if not isinstance(event_payload, str):
                event_payload = json.dumps(event_payload)

            ch.basic_publish(
                exchange=self.config.CREATE_ITEM_EVENTS_EXCHANGE,
                routing_key=self.config.CREATE_ITEM_EVENTS_ROUTING_KEY,
                body=event_payload
            )

            logger.info("New event message has been published")
