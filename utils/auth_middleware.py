from functools import wraps
from flask import request, jsonify
import jwt
from config import jwt_key, algorithm


def token_required():
    def _token_required(f):
        @wraps(f)
        async def __token_required(*args, **kwargs):
            authorization_header = request.headers
            try:
                token = authorization_header["Authorization"].split(" ")[1]
            except:
                return (
                    jsonify({"message": "Authorization header is missing or invalid"}),
                    401,
                )
            try:
                user = jwt.decode(token, jwt_key, algorithms=[algorithm])
            except jwt.exceptions.DecodeError:
                return (
                    jsonify({"message": "Authorization token is invalid"}),
                    401,
                )
            except jwt.exceptions.ExpiredSignatureError:
                    return (
                        jsonify({"message": "Authorization Invalid"}),
                        401,
                    )
            else:
                from databases import UserCRUD

                user_database = UserCRUD()
                try:
                    await user_database.get("login", email=user["email"])
                except:
                    return (
                        jsonify({"message": "Authorization Invalid"}),
                        401,
                    )
                else:
                    return await f(*args, **kwargs)

        return __token_required

    return _token_required
