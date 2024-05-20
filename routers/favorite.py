from flask import Blueprint, jsonify, request, abort
from utils import token_required, ProductFoundError
from databases import FavoriteCRUD
from sqlalchemy.exc import IntegrityError, DataError

favorite_router = Blueprint("api favorite item", __name__)
favorite_database = FavoriteCRUD()


@favorite_router.post("/fidea/v1/user/favorite")
@token_required()
async def add_favorite_item():
    data = request.json
    user = request.user
    seller_id = data.get("seller_id")
    product_id = data.get("product_id")
    try:
        await favorite_database.insert(user.id, seller_id, product_id)
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": f"product {product_id} already favorite item",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": f"success add favorite to {product_id}",
                }
            ),
            201,
        )


@favorite_router.delete("/fidea/v1/user/favorite")
@token_required()
async def remove_favorite_item():
    data = request.json
    user = request.user
    seller_id = data.get("seller_id")
    product_id = data.get("product_id")
    try:
        await favorite_database.delete(user.id, seller_id, product_id)
    except DataError:
        abort(415)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": f"product {product_id} not found",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": f"success delete favorite to {product_id}",
                }
            ),
            201,
        )
