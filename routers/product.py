from flask import Blueprint, request, jsonify
from databases import ProductCRUD, FavoriteCRUD
from utils import UserNotFoundError, UserNotSeller, token_required, ProductFoundError
from sqlalchemy.exc import IntegrityError

product_router = Blueprint("api ecommerce product", __name__)
product_database = ProductCRUD()
favorite_database = FavoriteCRUD()


@product_router.post("/fidea/v1/product")
@token_required()
async def add_product():
    data = request.json
    seller_id = data.get("seller_id")
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    tags = data.get("tags")
    image_url = data.get("image_url")
    stock = data.get("stock")
    try:
        await product_database.insert(
            seller_id,
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
                    "message": f"user {seller_id!r} not found",
                }
            ),
            404,
        )
    except UserNotSeller:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"user {seller_id!r} not seller",
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


@product_router.get("/fidea/v1/product/<string:seller>/<int:seller_id>/<int:user_id>")
async def get_product_by_seller(seller, seller_id, user_id):
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
                            "sold": product.sold,
                            "is_favorite": await favorite_database.get(
                                "is_favorite",
                                user_id=user_id,
                                seller_id=seller_id,
                                product_id=product.id,
                            ),
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
    "/fidea/v1/product/<string:seller>/<int:seller_id>/<int:product_id>/<int:user_id>"
)
async def get_product_id(seller, seller_id, product_id, user_id):
    try:
        data = await product_database.get(
            "product_id", seller=seller, seller_id=seller_id, product_id=product_id
        )
    except ProductFoundError:
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
                        "sold": product.sold,
                        "is_favorite": await favorite_database.get(
                            "is_favorite",
                            user_id=user_id,
                            seller_id=seller_id,
                            product_id=product.id,
                        ),
                        "image_url": product.image_url,
                        "updated_at": product.updated_at,
                        "created_at": product.created_at,
                    },
                }
            ),
            200,
        )


@product_router.get("/fidea/v1/product/search/<string:title>/<int:user_id>")
async def get_title(title, user_id):
    try:
        data = await product_database.get("title", title=title)
    except ProductFoundError:
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
                            "sold": product.sold,
                            "is_favorite": await favorite_database.get(
                                "is_favorite",
                                user_id=user_id,
                                seller_id=store.id,
                                product_id=product.id,
                            ),
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


@product_router.get("/fidea/v1/product/<int:user_id>")
async def get_product(user_id):
    try:
        data = await product_database.get("all")
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"data product not found",
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
                    "message": f"data product found",
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
                            "sold": product.sold,
                            "is_favorite": await favorite_database.get(
                                "is_favorite",
                                user_id=user_id,
                                seller_id=store.id,
                                product_id=product.id,
                            ),
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
