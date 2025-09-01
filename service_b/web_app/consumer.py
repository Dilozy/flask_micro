import os
import logging
import json
import threading
from contextlib import contextmanager

import pika

from web_app.repositories import RecievedItemsRepo
from web_app.config import DevelopmentConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageConsumer:
    def __init__(self):
        self.params = pika.ConnectionParameters(
            host=DevelopmentConfig.RABBIT_HOST,
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
                exchange=DevelopmentConfig.CREATE_ITEM_EVENTS_EXCHANGE,
                exchange_type="direct",
                durable=True,
                auto_delete=False
            )
            yield channel
        finally:
            connection.close()

    def consume_create_item_event_messages(self):
        with self.channel() as ch:
            ch.queue_declare(DevelopmentConfig.CREATE_ITEM_EVENTS_QUEUE,
                             auto_delete=False,
                             durable=True)
            ch.queue_bind(
                queue="create_item_events_queue",
                exchange=DevelopmentConfig.CREATE_ITEM_EVENTS_EXCHANGE,
                routing_key=DevelopmentConfig.CREATE_ITEM_EVENTS_ROUTING_KEY
            )

            ch.basic_consume(queue=DevelopmentConfig.CREATE_ITEM_EVENTS_QUEUE,
                             on_message_callback=self.add_recieved_item,
                             auto_ack=False)
            
            ch.start_consuming()
    
    def add_recieved_item(self, ch, method, properties, body):
        try:
            item_data = json.loads(body)
            RecievedItemsRepo.add(item_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    
def start_message_consumer(app):
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
