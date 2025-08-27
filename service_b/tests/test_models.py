from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from ..models import ReceivedItem


class TestRecievedItemModel:
    def test_recieved_item_creation(self, session):
        new_recieved_item = ReceivedItem(name="laptop")
        session.add(new_recieved_item)
        session.commit()

        new_recieved_item_db = session.get(ReceivedItem, new_recieved_item.id)
        assert new_recieved_item_db is not None
        assert new_recieved_item_db.name == new_recieved_item.name
        assert isinstance(new_recieved_item_db.recieved_at, datetime)

    def test_recieved_item_creation_without_name(self, session):
        new_recieved_item = ReceivedItem()
        
        with pytest.raises(IntegrityError):
           session.add(new_recieved_item)
           session.commit()
