from flask import Blueprint, request, jsonify
from databases import UserCRUD
import databases

user_router = Blueprint("api ecommerce user", __name__)
user_database = UserCRUD()


@user_router.post("/fidea/v1/user/balance")
async def add_balance():
    data = request.json
    username = data.get("username")
    balance = data.get("balance")
    try:
        result = await user_database.update(
            "balance", username=username, balance=balance
        )
    except databases.user.UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success update balance {username!r}",
                }
            ),
            201,
        )


@user_router.get("/fidea/v1/user/balance/<string:username>")
async def get_balance(username):
    try:
        result = await user_database.get("coba", username=username)
    except databases.user.UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success update balance {username!r}",
                }
            ),
            201,
        )
