from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from service_a.models import Item, OutboxEvent
from service_a.schemas import ItemRead


class TestItemModel:
    def test_item_creation(self, session):
        item = Item(name="laptop")
        session.add(item)
        session.commit()
        
        retrieved_item = session.get(Item, item.id)
        assert retrieved_item is not None
        assert retrieved_item.name == "laptop"
        assert isinstance(retrieved_item.created_at, datetime)

    def test_item_creation_without_name(self, session):
        item = Item()
        
        with pytest.raises(IntegrityError):
            session.add(item)
            session.commit()


class TestOutboxEventModel:
    def test_event_creation(self, session):
        item = Item(name="laptop")
        session.add(item)
        session.commit()

        dumped_item_data = ItemRead.model_validate(
            item, from_attributes=True
            ).model_dump_json()
        
        new_outbox_event = OutboxEvent(payload=dumped_item_data)
        session.add(new_outbox_event)
        session.commit()

        retrieved_event = session.get(OutboxEvent, new_outbox_event.id)
        assert retrieved_event is not None
        assert retrieved_event.payload == dumped_item_data
        assert isinstance(retrieved_event.created_at, datetime)
        assert not retrieved_event.processed

    def test_event_creation_without_payload(self, session):
        outbox_event = OutboxEvent()

        with pytest.raises(IntegrityError):
            session.add(outbox_event)
            session.commit()