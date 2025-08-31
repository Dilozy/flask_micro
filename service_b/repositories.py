from models import ReceivedItem
from extensions import db


class RecievedItemsRepo:
    @staticmethod
    def all():
        return ReceivedItem.query.all()
    
    @staticmethod
    def add(new_item_data):
        new_recieved_item = ReceivedItem(name=new_item_data["name"])
        db.session.add(new_recieved_item)
        db.session.commit()

