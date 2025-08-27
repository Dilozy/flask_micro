import pytest

from ..app import create_app
from ..extensions import db
from ..config import TestingConfig
from .factories import ItemFactory


@pytest.fixture(scope="function")
def app():
    app = create_app(config_class=TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


@pytest.fixture()
def items(session):
    items = ItemFactory.create_batch(10)
    session.commit()
    return items
