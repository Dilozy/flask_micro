import json

import pytest
from web_app.config import TestingConfig


class TestMessageProducer:
    def test_produce_message(self, rabbit_producer, rabbit_consumer_channel):
        test_payload = {"test_key": "test_value"}
        rabbit_producer.produce_event_message(test_payload)

        method_frame, body = self._consume_test_message(rabbit_consumer_channel)
        assert method_frame is not None
        assert method_frame.routing_key == TestingConfig.CREATE_ITEM_EVENTS_ROUTING_KEY
        assert method_frame.exchange == TestingConfig.CREATE_ITEM_EVENTS_EXCHANGE
        assert json.loads(body) == test_payload

    def test_produce_message_with_unserializable_payload(self, rabbit_producer):
        test_set = {1, 2, 3}
        with pytest.raises(TypeError):
            rabbit_producer.produce_event_message(test_set)

    def _consume_test_message(self, rabbit_consumer_channel):
        with rabbit_consumer_channel as ch:
            method_frame, _, body = ch.basic_get(
                queue=TestingConfig.CREATE_ITEM_EVENTS_QUEUE,
                auto_ack=True,
            )
            return method_frame, body
