from flask import Blueprint, request, jsonify
from databases import ProductCRUD
import databases
from utils import UserNotFoundError, UserNotSeller, token_required, ProductFoundError
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


@product_router.get("/fidea/v1/product/<string:seller>/<int:seller_id>")
async def get_product(seller, seller_id):
    try:
        data = await product_database.get("product", seller=seller, seller_id=seller_id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"data store {seller_id!r} not found",
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
                    "message": f"data store {seller_id!r} was found",
                    "result": [
                        {
                            "product_id": product.id,
                            "store": store.seller,
                            "store_id": store.id,
                            "recomendation": product.recomendation,
                            "title": product.title,
                            "description": product.description,
                            "stock": product.stock,
                            "price": product.price,
                            "tags": product.tags,
                            "image_url": product.image_url,
                            "updated_at": product.updated_at,
                            "created_at": product.created_at,
                        }
                        for product, store in data
                    ],
                }
            ),
            200,
        )


@product_router.get(
    "/fidea/v1/product/<string:seller>/<int:seller_id>/<int:product_id>"
)
async def get_product_id(seller, seller_id, product_id):
    try:
        data = await product_database.get(
            "product_id", seller=seller, seller_id=seller_id, product_id=product_id
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
        product, store = data
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data store {seller_id!r} was found",
                    "result": {
                        "product_id": product.id,
                        "store": store.seller,
                        "store_id": store.id,
                        "recomendation": product.recomendation,
                        "title": product.title,
                        "description": product.description,
                        "stock": product.stock,
                        "price": product.price,
                        "tags": product.tags,
                        "image_url": product.image_url,
                        "updated_at": product.updated_at,
                        "created_at": product.created_at,
                    },
                }
            ),
            200,
        )


@product_router.get("/fidea/v1/product/search/<string:title>")
async def get_title(title):
    try:
        data = await product_database.get("title", title=title)
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
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"data product {title} found",
                    "result": [
                        {
                            "product_id": product.id,
                            "store": store.seller,
                            "store_id": store.id,
                            "recomendation": product.recomendation,
                            "title": product.title,
                            "description": product.description,
                            "stock": product.stock,
                            "price": product.price,
                            "tags": product.tags,
                            "image_url": product.image_url,
                            "updated_at": product.updated_at,
                            "created_at": product.created_at,
                        }
                        for product, store in data
                    ],
                }
            ),
            200,
        )
