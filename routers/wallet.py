from flask import Blueprint, request, jsonify
from utils import token_required, UserNotIsActive
from databases import WalletCRUD
from sqlalchemy.exc import IntegrityError

wallet_router = Blueprint("api ecommerce wallet", __name__)
wallet_database = WalletCRUD()


@wallet_router.post("/fidea/v1/user/active/wallet")
@token_required()
async def active_wallet():
    data = request.json
    user_id = data.get("user_id")
    try:
        await wallet_database.insert(user_id)
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"wallet user '{user_id}' already active",
                }
            ),
            400,
        )
    except UserNotIsActive:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"user '{user_id}' is not active",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success active wallet '{user_id}'",
                }
            ),
            201,
        )
