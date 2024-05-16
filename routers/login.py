from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt
from databases import UserCRUD, StoreCRUD
from utils import UserNotFoundError
from config import jwt_key, algorithm
import jwt
import datetime

login_router = Blueprint("api user login", __name__)
bcrypt = Bcrypt()
user_database = UserCRUD()
seller_database = StoreCRUD()


@login_router.get("/fidea/v1/user/login/<string:email>/<string:password>")
async def login(email, password):
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
            expired_at = datetime.datetime.now(datetime.timezone.utc).timestamp() + (
                datetime.timedelta(hours=3).total_seconds()
            )
            is_seller = await seller_database.get("is_seller", user_id=user.id)
            encoded_jwt = jwt.encode(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                    "is_seller": True if is_seller else False,
                    "exp": expired_at,
                },
                jwt_key,
                algorithm=algorithm,
            )
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "result": {"token": encoded_jwt},
                        "message": f"user {email!r} was found",
                    }
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {email!r} not found",
                }
            ),
            404,
        )
