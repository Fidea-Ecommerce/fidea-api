from flask import Blueprint, request, jsonify
from utils import token_required
from databases import ProductCRUD, UserCRUD, CartCRUD, WalletCRUD, StoreCRUD
from utils import UserNotFoundError, ProductFoundError

checkout_router = Blueprint("api ecommerce checkout", __name__)
product_database = ProductCRUD()
user_database = UserCRUD()
cart_database = CartCRUD()
wallet_database = WalletCRUD()
store_database = StoreCRUD()


@checkout_router.post("/fidea/v1/product/checkout")
@token_required()
async def checkout_product():
    user = request.user
    try:
        user_wallet = await wallet_database.get("user_id", user_id=user.id)
        user_cart = await cart_database.get("cart_checkout", user_id=user.id)
    except (UserNotFoundError, ProductFoundError):
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"cart user '{user.id}' not found",
                }
            ),
            404,
        )
    else:
        price = sum(
            [cart.amount * product.price for cart, user, product, store in user_cart]
        )
        if user_wallet.amount < price:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"insufficient funds",
                    }
                ),
                400,
            )
        for item in user_cart:
            cart, user, product, store = item
            await cart_database.delete(user_id=cart.user_id, cart_id=cart.id)
            await product_database.update(
                "checkout",
                seller_id=product.seller_id,
                product_id=product.id,
                amount=(
                    0
                    if product.stock - cart.amount <= 0
                    else product.stock - cart.amount
                ),
            )
            await wallet_database.update(
                "amount",
                user_id=user.id,
                amount=(
                    0
                    if user_wallet.amount - (cart.amount * product.price) <= 0
                    else user_wallet.amount - (cart.amount * product.price)
                ),
            )
            await store_database.update(
                "balance_checkout", user_id=store.id, amount=cart.amount * product.price
            )
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success purchase from cart '{user.id}'",
                }
            ),
            201,
        )
