import json
from datetime import datetime

import pytest
from sqlalchemy import select, func

from web_app.models import Item, OutboxEvent


class TestCreatItemAPI:
    def test_create_with_correct_request(self, session, client, initial_items_count):
        initial_outbox_events_count = 0
        
        request_data = {"name": "vacuum cleaner"}
        response = client.post("api/v1/items", json=request_data)

        assert response.status_code == 201
        assert response.json["detail"] == "Item was created successfully"
        
        new_item_count = session.execute(select(func.count(Item.id))).scalar()
        assert new_item_count == initial_items_count + 1
        
        outbox_events_count = session.execute(select(func.count(OutboxEvent.id))).scalar()
        assert outbox_events_count == initial_outbox_events_count + 1

        new_outbox_event = session.execute(select(OutboxEvent)).scalar_one_or_none()
        assert new_outbox_event
        
        new_event_payload = json.loads(new_outbox_event.payload)

        stmt = select(Item).where(Item.id == new_event_payload["id"])
        new_item = session.execute(stmt).scalar_one_or_none()
        assert new_item

        new_event_payload["created_at"] = datetime.fromisoformat(new_event_payload["created_at"])
        
        for key, val in new_event_payload.items():
            assert hasattr(new_item, key) and getattr(new_item, key) ==  val

    @pytest.mark.parametrize("request_data", [
        {"nanameme": "vacuum cleaner"},
        {},
        {"name": "smartphone", "aa": "aabb"},
        "jhjkljklj"
    ])
    def test_create_with_incorrect_request(self, session, client,
                                           request_data, initial_items_count):
        response = client.post("api/v1/items", json=request_data)

        assert response.status_code == 400
        assert response.json["error"] == "Incorrect request"
        
        stmt = select(func.count(Item.id))
        assert session.execute(stmt).scalar() == initial_items_count

        stmt = select(func.count(OutboxEvent.id))
        assert session.execute(stmt).scalar() == 0


class TestListinitial_items_countAPI:
    def test_endpoint_response(self, client, initial_items_count):
        response = client.get("api/v1/items")
        assert response.status_code == 200
        assert len(response.json) == initial_items_count

    @pytest.mark.parametrize("request_data", [
        {"name": "abracadavra"},
    ])
    def test_endpoint_after_adding_new_item(self, client, initial_items_count, request_data):
        client.post("api/v1/items", json=request_data)

        response = client.get("api/v1/items")
        assert len(response.json) == initial_items_count + 1
        assert response.json[-1]["name"] == request_data["name"]