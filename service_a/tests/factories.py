import factory
from factory.alchemy import SQLAlchemyModelFactory

from ..extensions import db
from ..models import Item


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class ItemFactory(BaseFactory):
    class Meta:
        model = Item

    name = factory.Faker("word")
