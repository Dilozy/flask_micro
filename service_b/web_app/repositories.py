from sqlalchemy import select
from web_app.extensions import db
from web_app.models import ReceivedItem


class RecievedItemsRepo:
    @staticmethod
    def list_paginated(page=1, page_size=10):
        stmt = select(ReceivedItem)
        paginated_result = db.paginate(
            stmt, page=page, per_page=page_size, error_out=False,
        )

        return paginated_result.items

    @staticmethod
    def add(new_item_data):
        new_recieved_item = ReceivedItem(name=new_item_data["name"])
        db.session.add(new_recieved_item)
        db.session.commit()
