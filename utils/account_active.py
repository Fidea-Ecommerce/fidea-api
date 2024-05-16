from .token import Token
from itsdangerous.url_safe import URLSafeSerializer
from config import account_active_key


class AccountActive(Token):
    @staticmethod
    async def insert(user_id, email):
        s = URLSafeSerializer(account_active_key, salt="account_active")
        token = s.dumps({"user_id": user_id, "email": email})
        return token

    @staticmethod
    async def get(token):
        s = URLSafeSerializer(account_active_key, salt="account_active")
        try:
            s.loads(token)["user_id"]
            s.loads(token)["email"]
        except:
            return None
        else:
            return s.loads(token)
