from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from databases import UserCRUD, StoreCRUD
from utils import UserNotFoundError
from config import access_token_key, algorithm, refresh_token_key
import jwt
import datetime

login_router = Blueprint("api user login", __name__)
bcrypt = Bcrypt()
user_database = UserCRUD()
seller_database = StoreCRUD()


@login_router.post("/fidea/v1/user/login")
async def login():
    user_ip = request.headers.get("X-Forwarded-For") or request.remote_addr
    user_agent_string = request.headers.get("User-Agent")
    data = request.json
    email = data.get("email")
    password = data.get("password")
    try:
        user = await user_database.get("login", email=email, password=password)
    except UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {email!r} not found",
                }
            ),
            404,
        )
    else:
        if bcrypt.check_password_hash(user.password, password):
            is_seller = await seller_database.get("is_seller", user_id=user.id)
            access_token = jwt.encode(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                    "is_seller": True if is_seller else False,
                    "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                    + datetime.timedelta(minutes=5).total_seconds(),
                },
                access_token_key,
                algorithm=algorithm,
            )
            refresh_token = jwt.encode(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                    + datetime.timedelta(days=30).total_seconds(),
                },
                refresh_token_key,
                algorithm=algorithm,
            )
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "result": {
                            "token": {
                                "access_token": access_token,
                                "refresh_token": refresh_token,
                            }
                        },
                        "message": f"user {email!r} was found",
                    }
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": None,
                    "message": f"user {email!r} not found",
                }
            ),
            404,
        )
