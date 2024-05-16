from flask import Blueprint, request, jsonify
from databases import ProductCRUD
import databases
from utils import UserNotFoundError, UserNotSeller, token_required
from sqlalchemy.exc import IntegrityError

product_router = Blueprint("api ecommerce product", __name__)
product_database = ProductCRUD()


@product_router.post("/fidea/v1/product")
@token_required()
async def add_product():
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    tags = data.get("tags")
    image_url = data.get("image_url")
    stock = data.get("stock")
    try:
        await product_database.insert(
            user_id,
            description,
            title,
            price,
            tags,
            image_url,
            stock,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"the product {title!r} already exists",
                }
            ),
            400,
        )
    except UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {user_id!r} not found",
                }
            ),
            404,
        )
    except UserNotSeller:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"user {user_id!r} not seller",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success add {title!r} product",
                }
            ),
            201,
        )


@product_router.delete("/fidea/v1/product/stock")
@token_required()
async def remove_stock():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    amount = data.get("amount")
    try:
        await product_database.update(
            "product", username=username, id=id, amount=amount
        )
    except databases.product.ProductNotAvaible:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"stock not avaible with product {id}",
                }
            ),
            400,
        )
    except databases.product.ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"product {id} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success remove stock {id!r} product",
                }
            ),
            201,
        )


@product_router.delete("/fidea/v1/product")
@token_required()
async def delete_product():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    try:
        result = await product_database.delete("product", id=id, username=username)
    except databases.product.ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"data store {username!r} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success delete {result.title!r} item",
                }
            ),
            201,
        )


@product_router.get("/fidea/v1/product/<string:username>")
async def get_product(username):
    try:
        data = await product_database.get("product", username=username)
    except databases.product.ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"data store {username!r} not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        arr = [
            {
                "id": d.id,
                "username": d.username,
                "recomendation": d.recomendation,
                "title": d.title,
                "description": d.description,
                "stock": d.stock,
                "price": d.price,
                "tags": d.tags,
                "image_url": d.image_url,
                "updated_at": d.updated_at,
                "created_at": d.created_at,
            }
            for d in data
        ]
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data store {username!r} was found",
                    "result": arr,
                }
            ),
            200,
        )


@product_router.get("/fidea/v1/product/<string:username>/<int:product_id>")
async def get_product_id(username, product_id):
    try:
        data = await product_database.get(
            "product_id", username=username, product_id=product_id
        )
    except databases.product.ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"data product {product_id} not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data store {username!r} was found",
                    "result": {
                        "id": data.id,
                        "username": data.username,
                        "recomendation": data.recomendation,
                        "title": data.title,
                        "description": data.description,
                        "stock": data.stock,
                        "price": data.price,
                        "tags": data.tags,
                        "image_url": data.image_url,
                        "updated_at": data.updated_at,
                        "created_at": data.created_at,
                    },
                }
            ),
            200,
        )


@product_router.get("/fidea/v1/product/search/<string:username>/<string:title>")
async def get_title(username, title):
    try:
        data = await product_database.get("title", username=username, title=title)
    except databases.product.ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"data product {title} not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        arr = [
            {
                "id": d.id,
                "username": d.username,
                "recomendation": d.recomendation,
                "title": d.title,
                "description": d.description,
                "stock": d.stock,
                "price": d.price,
                "tags": d.tags,
                "image_url": d.image_url,
                "updated_at": d.updated_at,
                "created_at": d.created_at,
            }
            for d in data
        ]
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data product {title} found",
                    "result": arr,
                }
            ),
            200,
        )
