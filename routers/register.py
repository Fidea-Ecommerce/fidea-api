from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from databases import UserCRUD
from utils import (
    Miscellaneous,
)
from sqlalchemy.exc import IntegrityError

register_router = Blueprint("api user register", __name__)
bcrypt = Bcrypt()
user_database = UserCRUD()


@register_router.post("/fidea/v1/user/register")
async def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    if password != confirm_password:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"password and confirm password are not the same",
                }
            ),
            400,
        )
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    try:
        if password_secure := await Miscellaneous.check_password_strength(password):
            await user_database.insert(
                username=username,
                email=email,
                password=hashed_password,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": "password not secure",
                    }
                ),
                400,
            )
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"failed register {username!r}",
                }
            ),
            400,
        )
    except Exception:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": "bad request",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success register {username!r}",
                }
            ),
            201,
        )
