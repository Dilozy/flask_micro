import pytest
from web_app.models import ReceivedItem


class TestListRecievedItemsAPI:
    def test_endpoint_response(self, client, recieved_items):
        response = client.get("api/v1/items")

        assert response.status_code == 200
        assert len(response.json["items"]) == len(recieved_items)

    def test_endpoint_response_after_adding_a_new_item(
        self, client, session, recieved_items,
    ):
        new_recieved_item = ReceivedItem(name="test_item")
        session.add(new_recieved_item)
        session.commit()

        response = client.get("api/v1/items?page_size=20")

        assert response.status_code == 200
        assert len(response.json["items"]) == len(recieved_items) + 1

    @pytest.mark.parametrize("http_method", ["post", "put", "delete"])
    def test_response_with_unexpected_request_methods(self, client, http_method):
        client_method = getattr(client, http_method)

        response = client_method("api/v1/items")
        assert response.status_code == 405
