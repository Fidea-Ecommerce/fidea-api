from .token import Token
from itsdangerous.url_safe import URLSafeSerializer
from config import reset_password_key


class TokenResetPassword(Token):
    @staticmethod
    async def insert(user_id, email):
        s = URLSafeSerializer(reset_password_key, salt="reset_password")
        token = s.dumps({"user_id": user_id, "email": email})
        return token

    @staticmethod
    async def get(token):
        s = URLSafeSerializer(reset_password_key, salt="reset_password")
        try:
            s.loads(token)["user_id"]
            s.loads(token)["email"]
        except:
            return None
        else:
            return s.loads(token)
