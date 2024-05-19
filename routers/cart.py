from flask import Blueprint, request, jsonify, abort
from databases import CartCRUD
from utils import (
    ProductFoundError,
    StockNotAvaible,
    token_required,
    NumberMoreThan0,
    UserNotIsActive,
    UserNotFoundError,
)
from sqlalchemy.exc import IntegrityError, DataError, StatementError, ProgrammingError

cart_router = Blueprint("api cart user", __name__)
cart_database = CartCRUD()


@cart_router.get("/fidea/v1/cart/<int:user_id>")
@token_required()
async def get_product(user_id):
    try:
        result = await cart_database.get("cart", user_id=user_id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user_id}' not found",
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
                    "message": f"cart user '{user_id}' was found",
                    "result": [
                        {
                            "store_id": store.id,
                            "cart_id": cart.id,
                            "product_id": product.id,
                            "description": product.description,
                            "stock": product.stock,
                            "amount": cart.amount,
                            "mark": cart.mark,
                            "title": product.title,
                            "price": product.price,
                            "image_url": product.image_url,
                            "created_at": product.created_at,
                            "total_price": cart.amount * product.price,
                        }
                        for cart, user, product, store in result
                    ],
                }
            ),
            200,
        )


@cart_router.get("/fidea/v1/cart/<int:user_id>/<int:cart_id>")
@token_required()
async def get_product_cart_id(user_id, cart_id):
    try:
        result = await cart_database.get("cart_id", user_id=user_id, cart_id=cart_id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user_id}' not found",
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
                    "message": f"cart user '{user_id}' was found",
                    "result": {
                        "store_id": store.id,
                        "cart_id": cart.id,
                        "product_id": product.id,
                        "description": product.description,
                        "stock": product.stock,
                        "amount": cart.amount,
                        "mark": cart.mark,
                        "title": product.title,
                        "price": product.price,
                        "image_url": product.image_url,
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
    user_id = data.get("user_id")
    mark = data.get("mark")
    try:
        await cart_database.update("all_tick", user_id=user_id, mark=mark)
    except (DataError, StatementError):
        abort(415)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user '{user_id}' not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success update mark cart user '{user_id}'",
                }
            ),
            201,
        )


@cart_router.get("/fidea/v1/cart/checkout/<int:user_id>")
@token_required()
async def get_cart_checkout(user_id):
    try:
        result = await cart_database.get("cart_checkout", user_id=user_id)
    except ProductFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user_id}' not found",
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
                    "store_id": store.id,
                    "cart_id": cart.id,
                    "product_id": product.id,
                    "description": product.description,
                    "stock": product.stock,
                    "amount": cart.amount,
                    "mark": cart.mark,
                    "title": product.title,
                    "price": product.price,
                    "image_url": product.image_url,
                    "created_at": product.created_at,
                }
                for cart, user, product, store in result
            ],
        )
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"cart user '{user_id}' was found",
                    "result": {"item": arr, "total_price": price},
                }
            ),
            200,
        )


@cart_router.put("/fidea/v1/cart/tick/cart-id")
@token_required()
async def put_cart_bill_tick():
    data = request.json
    cart_id = data.get("cart_id")
    user_id = data.get("user_id")
    try:
        await cart_database.update("tick", user_id=user_id, cart_id=cart_id)
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
    user_id = data.get("user_id")
    cart_id = data.get("cart_id")
    amount = data.get("amount")
    try:
        await cart_database.update(
            "amount", user_id=user_id, cart_id=cart_id, amount=amount
        )
    except (DataError, ProgrammingError):
        abort(415)
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
    user_id = data.get("user_id")
    cart_id = data.get("cart_id")
    try:
        await cart_database.delete(user_id, cart_id)
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
                    "message": f"success delete cart to user '{user_id}' cart",
                }
            ),
            201,
        )


@cart_router.post("/fidea/v1/cart")
@token_required()
async def add_cart():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    product_id = data.get("product_id")
    try:
        await cart_database.insert(user_id, amount, product_id)
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
                    "message": f"user '{user_id}' not found",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success add product to user '{user_id}' cart",
                }
            ),
            201,
        )
