import factory
from factory.alchemy import SQLAlchemyModelFactory
from web_app.extensions import db
from web_app.models import ReceivedItem


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class RecievedItemFactory(BaseFactory):
    class Meta:
        model = ReceivedItem

    name = factory.Faker("word")
