import json

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from repositories import ItemsRepo, OutboxEventsRepo
from schemas import ItemCreate
from misc import model_to_dict


items_bp = Blueprint("items", __name__)


@items_bp.route("/items", methods=["POST"])
def create_item():
    try:
        item_data = ItemCreate(**request.get_json())
        new_item = ItemsRepo.create(item_data.model_dump())
        new_item_serialized = json.dumps(model_to_dict(new_item))

        OutboxEventsRepo.create(new_item_serialized)
        
        return jsonify({"detail": "Item was created successfully"}), 201
    except (ValidationError, TypeError) as err:
        return jsonify({
            "error": str(err)
        }), 400


@items_bp.route("/items", methods=["GET"])
def list_items():
    items = [model_to_dict(item) for item in ItemsRepo.list()]
    return jsonify(items)


@items_bp.route("/events", methods=["GET"])
def list_events():
    events = [model_to_dict(event) for event in OutboxEventsRepo.list()]
    return jsonify(events)
