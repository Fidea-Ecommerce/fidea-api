from flask import Blueprint, jsonify, request
from utils import token_required
import jwt
from config import refresh_token_key, access_token_key, algorithm
from databases import StoreCRUD
import datetime

refresh_token_router = Blueprint("api refresh token", __name__)
seller_database = StoreCRUD()


@refresh_token_router.post("/fidea/v1/user/refresh-token")
@token_required()
async def refresh_token():
    data = request.json
    refresh_token = data.get("refresh_token")
    try:
        decoded_token = jwt.decode(
            refresh_token, refresh_token_key, algorithms=["HS256"]
        )
    except:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": {"token": refresh_token},
                    "message": f"token invalid",
                }
            ),
            400,
        )
    else:
        is_seller = await seller_database.get(
            "is_seller", user_id=decoded_token["user_id"]
        )
        access_token = jwt.encode(
            {
                "user_id": decoded_token["user_id"],
                "username": decoded_token["username"],
                "email": decoded_token["email"],
                "is_active": decoded_token["is_active"],
                "is_admin": decoded_token["is_admin"],
                "is_seller": True if is_seller else False,
                "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                + datetime.timedelta(minutes=5).total_seconds(),
            },
            access_token_key,
            algorithm=algorithm,
        )
        refresh_token = jwt.encode(
            {
                "user_id": decoded_token["user_id"],
                "username": decoded_token["username"],
                "email": decoded_token["email"],
                "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                + datetime.timedelta(days=30).total_seconds(),
            },
            refresh_token_key,
            algorithm=algorithm,
        )
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": {
                        "token": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                        }
                    },
                    "message": f"token is valid",
                }
            ),
            201,
        )
