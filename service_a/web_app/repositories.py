from sqlalchemy import select
from web_app.extensions import db
from web_app.models import Item, OutboxEvent


class ItemsRepo:
    @staticmethod
    def create(data: dict):
        new_item = Item(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    @staticmethod
    def list_paginated(page=1, page_size=10):
        stmt = select(Item)
        paginated_result = db.paginate(
            stmt, page=page, per_page=page_size, error_out=False,
        )

        return paginated_result.items


class OutboxEventsRepo:
    @staticmethod
    def create(data: dict):
        new_event = OutboxEvent(payload=data)
        db.session.add(new_event)
        db.session.commit()

    @staticmethod
    def list_():
        return OutboxEvent.query.all()

    @staticmethod
    def list_unprocessed():
        stmt = select(OutboxEvent).where(~OutboxEvent.processed)
        return db.session.execute(stmt).scalars().all()

    @staticmethod
    def confirm_processed_for(event):
        event.processed = True
        db.session.commit()
