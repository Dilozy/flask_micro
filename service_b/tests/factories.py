import factory
from factory.alchemy import SQLAlchemyModelFactory

from ..extensions import db
from ..models import ReceivedItem


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class RecievedItemFactory(BaseFactory):
    class Meta:
        model = ReceivedItem

    name = factory.Faker("word")
