from flask import Flask

from web_app.config import TestingConfig
from web_app.api import items_bp


class TestAppFactory:
    def test_app_creation(self, app):
        assert isinstance(app, Flask)
        assert app.name == "service_a"

    def test_app_extensions(self, app):
        assert hasattr(app, "extensions")
        assert "sqlalchemy" in app.extensions
        assert "migrate" in app.extensions
        assert "celery" in app.extensions

    def test_app_config(self, app):
        assert app.config["TESTING"] is True
        
        for key in TestingConfig.__dict__:
            if key.isupper():
                assert app.config[key] == getattr(TestingConfig, key)
    
    def test_app_blueprints(self, app):
        assert items_bp == app.blueprints["items_bp"]
        assert app.url_map._rules_by_endpoint.get("items_bp.list_items") is not None
        assert app.url_map._rules_by_endpoint.get("items_bp.list_events") is not None
        assert app.url_map._rules_by_endpoint.get("items_bp.create_item") is not None
