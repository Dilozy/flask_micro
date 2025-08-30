from models import ReceivedItem


class RecievedItemsRepo:
    @staticmethod
    def all():
        return ReceivedItem.query.all()
