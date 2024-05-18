from functools import wraps
from flask import request, jsonify, abort
import jwt
from config import jwt_key, algorithm
import datetime


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
                    if (
                        user.is_active
                        and user.unbanned_at == None
                        and user.banned_at == None
                    ):
                        return await f(*args, **kwargs)
                    if not user.is_active or user.unbanned_at:
                        try:
                            if (
                                user.unbanned_at
                                < datetime.datetime.now(
                                    datetime.timezone.utc
                                ).timestamp()
                            ):
                                abort(403)
                            else:
                                await user_database.update(
                                    "unbanned", unbanned_at=None, email=user.email
                                )
                                return await f(*args, **kwargs)
                        except:
                            abort(403)
                    abort(403)

        return __token_required

    return _token_required
