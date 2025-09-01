import sys
import os

import pytest
from flask import Flask

from service_a.app_factory import create_app
from service_a.extensions import db
from service_a.config import TestingConfig


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
def session(app: Flask):
    with app.app_context():
        yield db.session()
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def initial_items_count():
    return 0
