from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from .repositories import ItemsRepo, OutboxEventsRepo
from .schemas import ItemCreate, ItemRead, OutboxEventRead


items_bp = Blueprint("items", __name__)


@items_bp.route("/items", methods=["POST"])
def create_item():
    try:
        item_data = ItemCreate(**request.get_json())
        new_item = ItemsRepo.create(item_data.model_dump())
        new_item_serialized = ItemRead.model_validate(new_item,
                                                      from_attributes=True).model_dump_json()

        OutboxEventsRepo.create(new_item_serialized)
        
        return jsonify({"detail": "Item was created successfully"}), 201
    except ValidationError:
        return jsonify({
            "error": "Incorrect request"
        }), 400


@items_bp.route("/items", methods=["GET"])
def list_items():
    items = [ItemRead.model_validate(item, from_attributes=True).model_dump()
             for item in ItemsRepo.list()]
    return jsonify(items)


@items_bp.route("/events", methods=["GET"])
def list_events():
    events = [OutboxEventRead.model_validate(event, from_attributes=True).model_dump()
             for event in OutboxEventsRepo.list()]
    return jsonify(events)