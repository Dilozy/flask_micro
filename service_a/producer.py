from kombu import Queue, Exchange, Connection, Producer

from config import CeleryConfig


RabbitMQ_url = CeleryConfig.broker_url


def publish_service_a_event_with(event_payload):
    with Connection(RabbitMQ_url) as conn:
        exchange = Exchange("service_a_create_items_events", type="direct")
        queue = Queue("service_a_create_items_events",
                      exchange=exchange,
                      routing_key="service_a_create_items_events")
        
        with conn.channel() as channel:
            exchange.declare(channel=channel)
            queue.declare(channel=channel)
            
            producer = Producer(channel, exchange=exchange, serializer="json")
            producer.publish(
                event_payload,
                routing_key="service_a_create_items_events"
            )