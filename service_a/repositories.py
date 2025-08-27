from .extensions import db
from .models import Item, OutboxEvent


class ItemsRepo:
    @staticmethod
    def create(data: dict):
        new_item = Item(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item
    
    @staticmethod
    def list():
        return Item.query.all()


class OutboxEventsRepo:
    @staticmethod
    def create(data: dict):
        new_event = OutboxEvent(payload=data)
        db.session.add(new_event)
        db.session.commit()

    @staticmethod
    def list():
        return OutboxEvent.query.all()