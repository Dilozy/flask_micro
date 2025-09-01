from flask import Blueprint, jsonify, request

from web_app.repositories import RecievedItemsRepo
from web_app.misc import model_to_dict


recieved_items_bp = Blueprint("/items", __name__)


@recieved_items_bp.route("/items", methods=["GET"])
def list_recieved_items():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    
    items = [model_to_dict(item) for item in RecievedItemsRepo.list_paginated(page, page_size)]

    response = {"items": items,
                "page": page,
                "page_size": page_size}
    return jsonify(response)
