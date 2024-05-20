from flask import Blueprint, request, jsonify
from databases import StoreCRUD
from sqlalchemy.exc import IntegrityError
from utils import token_required, UserNotFoundError

store_router = Blueprint("api store user", __name__)
seller_database = StoreCRUD()


@store_router.post("/fidea/v1/user/active/seller")
@token_required()
async def active_seller():
    data = request.json
    user = request.user
    store = data.get("store")
    try:
        await seller_database.insert(user.id, store)
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"store {store!r} already active",
                }
            ),
            400,
        )
    except UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"user {user.id} not found",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success active store {store!r}",
                }
            ),
            201,
        )
