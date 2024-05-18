from functools import wraps
from flask import request, jsonify, abort
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
                abort(401)
            try:
                user_decoded = jwt.decode(token, jwt_key, algorithms=[algorithm])
            except jwt.exceptions.DecodeError:
                abort(401)
            except jwt.exceptions.ExpiredSignatureError:
                abort(401)
            else:
                from databases import UserCRUD

                user_database = UserCRUD()
                try:
                    user = await user_database.get("login", email=user_decoded["email"])
                except:
                    abort(401)
                else:
                    if user.is_active:
                        return await f(*args, **kwargs)
                    else:
                        abort(403)

        return __token_required

    return _token_required
