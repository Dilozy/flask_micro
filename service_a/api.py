from flask import Blueprint


bp = Blueprint("items", __name__)


@bp.route("/items", methods=["POST"])
def create_item():
    