from flask import Blueprint, jsonify, request
from utils import token_required
import jwt
from config import refresh_token_key

refresh_token_router = Blueprint("api refresh token", __name__)


@refresh_token_router.post("/fidea/v1/user/refresh-token")
@token_required()
async def refresh_token():
    data = request.json
    refresh_token = data.get("refresh_token")
    try:
        decoded_token = jwt.decode(
            refresh_token, refresh_token_key, algorithms=["HS256"]
        )
        print(f"token valid {decoded_token}")
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
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": {"token": refresh_token},
                    "message": f"token is valid",
                }
            ),
            200,
        )
