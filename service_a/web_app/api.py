import json

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from web_app.misc import model_to_dict
from web_app.repositories import ItemsRepo, OutboxEventsRepo
from web_app.schemas import ItemCreate

items_bp = Blueprint("items_bp", __name__)


@items_bp.route("/items", methods=["POST"])
def create_item():
    try:
        item_data = ItemCreate(**request.get_json())
        new_item = ItemsRepo.create(item_data.model_dump())
        new_item_serialized = json.dumps(model_to_dict(new_item))

        OutboxEventsRepo.create(new_item_serialized)

        return jsonify({"detail": "Item was created successfully"}), 201
    except (ValidationError, TypeError):
        return jsonify({"error": "Invalid request"}), 400


@items_bp.route("/items", methods=["GET"])
def list_items():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)

    items = [model_to_dict(item) for item in ItemsRepo.list_paginated(page, page_size)]

    response = {"items": items, "page": page, "page_size": page_size}
    return jsonify(response)


@items_bp.route("/events", methods=["GET"])
def list_events():
    events = [model_to_dict(event) for event in OutboxEventsRepo.list_()]
    return jsonify(events)
