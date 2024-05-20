from flask import Blueprint, request, jsonify, abort
from databases import CartCRUD, FavoriteCRUD
from utils import (
    ProductFoundError,
    StockNotAvaible,
    token_required,
    NumberMoreThan0,
    UserNotFoundError,
    SellerNotIsActive,
)
from sqlalchemy.exc import IntegrityError, DataError, StatementError, ProgrammingError

cart_router = Blueprint("api cart user", __name__)
cart_database = CartCRUD()
favorite_database = FavoriteCRUD()


@cart_router.get("/fidea/v1/cart")
@token_required()
async def get_product():
    user = request.user
    try:
        result = await cart_database.get("cart", user_id=user.id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user.id}' not found",
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
                    "message": f"cart user '{user.id}' was found",
                    "result": [
                        {
                            "product_id": product.id,
                            "store_id": store.id,
                            "cart_id": cart.id,
                            "store": store.seller,
                            "recomendation": product.recomendation,
                            "title": product.title,
                            "description": product.description,
                            "stock": product.stock,
                            "price": product.price,
                            "tags": product.tags,
                            "sold": product.sold,
                            "is_favorite": await favorite_database.get(
                                "is_favorite",
                                user_id=user.id,
                                seller_id=store.id,
                                product_id=product.id,
                            ),
                            "image_url": product.image_url,
                            "updated_at": product.updated_at,
                            "created_at": product.created_at,
                            "total_price": cart.amount * product.price,
                        }
                        for cart, user, product, store in result
                    ],
                }
            ),
            200,
        )


@cart_router.get("/fidea/v1/cart/<int:cart_id>")
@token_required()
async def get_product_cart_id(cart_id):
    user = request.user
    try:
        result = await cart_database.get("cart_id", user_id=user.id, cart_id=cart_id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user.id}' not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        cart, user, product, store = result
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"cart user '{user.id}' was found",
                    "result": {
                        "product_id": product.id,
                        "store_id": store.id,
                        "cart_id": cart.id,
                        "store": store.seller,
                        "recomendation": product.recomendation,
                        "title": product.title,
                        "description": product.description,
                        "stock": product.stock,
                        "price": product.price,
                        "tags": product.tags,
                        "sold": product.sold,
                        "is_favorite": await favorite_database.get(
                            "is_favorite",
                            user_id=user.id,
                            seller_id=store.id,
                            product_id=product.id,
                        ),
                        "image_url": product.image_url,
                        "updated_at": product.updated_at,
                        "created_at": product.created_at,
                        "total_price": cart.amount * product.price,
                    },
                }
            ),
            200,
        )


@cart_router.put("/fidea/v1/cart/tick")
@token_required()
async def update_cart_tick():
    data = request.json
    mark = data.get("mark")
    user = request.user
    try:
        await cart_database.update("all_tick", user_id=user.id, mark=mark)
    except (DataError, StatementError):
        abort(415)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user '{user.id}' not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success update mark cart user '{user.id}'",
                }
            ),
            201,
        )


@cart_router.get("/fidea/v1/cart/checkout")
@token_required()
async def get_cart_checkout():
    user = request.user
    try:
        result = await cart_database.get("cart_checkout", user_id=user.id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user.id}' not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        price = sum(
            [cart.amount * product.price for cart, user, product, store in result]
        )
        arr = (
            [
                {
                    "product_id": product.id,
                    "store_id": store.id,
                    "cart_id": cart.id,
                    "store": store.seller,
                    "recomendation": product.recomendation,
                    "title": product.title,
                    "description": product.description,
                    "stock": product.stock,
                    "price": product.price,
                    "tags": product.tags,
                    "sold": product.sold,
                    "is_favorite": await favorite_database.get(
                        "is_favorite",
                        user_id=user.id,
                        seller_id=store.id,
                        product_id=product.id,
                    ),
                    "image_url": product.image_url,
                    "updated_at": product.updated_at,
                    "created_at": product.created_at,
                }
                for cart, user, product, store in result
            ],
        )
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"cart user '{user.id}' was found",
                    "result": {"item": arr, "total_price": price},
                }
            ),
            200,
        )


@cart_router.put("/fidea/v1/cart/tick/cart-id")
@token_required()
async def put_cart_bill_tick():
    data = request.json
    user = request.user
    cart_id = data.get("cart_id")
    try:
        await cart_database.update("tick", user_id=user.id, cart_id=cart_id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart id '{cart_id}' not found",
                }
            ),
            404,
        )
    except SellerNotIsActive:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"store from cart id '{cart_id}' not active",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success update mark cart id '{cart_id}'",
                }
            ),
            201,
        )


@cart_router.put("/fidea/v1/cart/amount")
@token_required()
async def put_cart_amount():
    data = request.json
    user = request.user
    cart_id = data.get("cart_id")
    amount = data.get("amount")
    try:
        await cart_database.update(
            "amount", user_id=user.id, cart_id=cart_id, amount=amount
        )
    except (DataError, ProgrammingError):
        abort(415)
    except SellerNotIsActive:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"store from cart id '{cart_id}' not active",
                }
            ),
            400,
        )
    except StockNotAvaible:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"stock cart '{cart_id}' not avaible",
                }
            ),
            400,
        )
    except NumberMoreThan0:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"the number cannot be below 0",
                }
            ),
            400,
        )
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart '{cart_id}' not found",
                }
            ),
            404,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"invalid input",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success update amount cart product '{cart_id}'",
                }
            ),
            201,
        )


@cart_router.delete("/fidea/v1/cart")
@token_required()
async def delete_cart():
    data = request.json
    user = request.user
    cart_id = data.get("cart_id")
    try:
        await cart_database.delete(user.id, cart_id)
    except DataError:
        abort(415)
    except NumberMoreThan0:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"the number cannot be below 0",
                }
            ),
            400,
        )
    except SellerNotIsActive:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"store from cart id '{cart_id}' not active",
                }
            ),
            400,
        )
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart '{cart_id}' not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success delete cart to user '{user.id}' cart",
                }
            ),
            201,
        )


@cart_router.post("/fidea/v1/cart")
@token_required()
async def add_cart():
    data = request.json
    user = request.user
    amount = data.get("amount")
    product_id = data.get("product_id")
    try:
        await cart_database.insert(user.id, amount, product_id)
    except SellerNotIsActive:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"store from product id '{product_id}' not active",
                }
            ),
            400,
        )
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"product '{product_id}' not found",
                }
            ),
            404,
        )
    except (DataError, TypeError):
        abort(415)
    except NumberMoreThan0:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"the number cannot be below 0",
                }
            ),
            400,
        )
    except StockNotAvaible:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"stock product '{product_id}' not avaible",
                }
            ),
            400,
        )
    except UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"user '{user.id}' not found",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success add product to user '{user.id}' cart",
                }
            ),
            201,
        )
