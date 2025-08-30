from flask import Blueprint, jsonify

from repositories import RecievedItemsRepo
from schemas import RecievedItemRead
from tasks import sum_two


recieved_items_bp = Blueprint("/items", __name__)


@recieved_items_bp.route("/items", methods=["GET"])
def list_recieved_items():
    items = [RecievedItemRead.model_validate(item).model_dump()
             for item in RecievedItemsRepo.all()]
    try:
        sum_two.delay()
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify(items)
