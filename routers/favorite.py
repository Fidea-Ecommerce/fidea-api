from flask import Blueprint, jsonify, request, abort
from utils import token_required, ProductFoundError, ProductAlready
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
    except DataError:
        abort(415)
    except ProductAlready:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": f"product '{product_id}' already favorite item",
                }
            ),
            400,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"product '{product_id}' not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": f"success add favorite to product '{product_id}'",
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
                    "status_code": 404,
                    "result": f"product '{product_id}' not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": f"success delete favorite to product '{product_id}'",
                }
            ),
            201,
        )


@favorite_router.get("/fidea/v1/user/favorite")
@token_required()
async def get_favorite_item():
    user = request.user
    try:
        data = await favorite_database.get("all", user_id=user.id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"product not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data favorite user '{user.id}' was found",
                    "result": [
                        {
                            "product_id": product.id,
                            "store": store.seller,
                            "store_id": store.id,
                            "favorite_id": favorite.id,
                            "recomendation": product.recomendation,
                            "title": product.title,
                            "description": product.description,
                            "stock": product.stock,
                            "price": product.price,
                            "tags": product.tags,
                            "sold": product.sold,
                            "store_active": store.is_active,
                            "is_favorite": True,
                            "image_url": product.image_url,
                            "updated_at": product.updated_at,
                            "created_at": product.created_at,
                        }
                        for favorite, product, store in data
                    ],
                }
            ),
            200,
        )


@favorite_router.get("/fidea/v1/user/favorite/<int:favorite_id>")
@token_required()
async def get_favorite_item_id(favorite_id):
    user = request.user
    try:
        data = await favorite_database.get(
            "favorite_id", user_id=user.id, favorite_id=favorite_id
        )
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"product not found",
                }
            ),
            404,
        )
    else:
        favorite, product, store = data
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data favorite user '{user.id}' was found",
                    "result": {
                        "product_id": product.id,
                        "store": store.seller,
                        "store_id": store.id,
                        "favorite_id": favorite.id,
                        "recomendation": product.recomendation,
                        "title": product.title,
                        "description": product.description,
                        "stock": product.stock,
                        "price": product.price,
                        "tags": product.tags,
                        "sold": product.sold,
                        "store_active": store.is_active,
                        "is_favorite": True,
                        "image_url": product.image_url,
                        "updated_at": product.updated_at,
                        "created_at": product.created_at,
                    },
                }
            ),
            200,
        )
