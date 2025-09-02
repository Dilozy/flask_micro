import pytest
from flask import Flask

from web_app.app_factory import create_app
from web_app.extensions import db
from web_app.config import TestingConfig


@pytest.fixture
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
def session(app: Flask):
    with app.app_context():
        yield db.session()
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def initial_items_count():
    return 0

