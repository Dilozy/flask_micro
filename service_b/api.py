from flask import Blueprint, jsonify

from .repositories import RecievedItemsRepo
from .schemas import RecievedItemRead


recieved_items_bp = Blueprint("/items", __name__)


@recieved_items_bp.route("/items", methods=["GET"])
def list_recieved_items():
    items = [RecievedItemRead.model_validate(item).model_dump()
             for item in RecievedItemsRepo.all()]
    
    return jsonify(items)
