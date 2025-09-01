import pytest

from ..web_app.app_factory import create_app
from ..web_app.extensions import db
from ..web_app.config import TestingConfig
from .factories import RecievedItemFactory


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
        db.session.remove()


@pytest.fixture(scope="class")
def recieved_items():
    recieved_items = RecievedItemFactory.create_batch(10)
    return recieved_items
