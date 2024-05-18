from .config import db_session, init_db
from models import WalletDatabase, UserDatabase
from sqlalchemy import and_, func, or_, desc
from .database import Database
import datetime
from utils import UserNotFoundError, UserNotIsActive


class WalletCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if (
            user := UserDatabase.query.filter(UserDatabase.id == user_id)
            .order_by(desc(UserDatabase.created_at))
            .first()
        ):
            user = WalletDatabase(user_id, created_at, created_at)
            db_session.add(user)
            db_session.commit()

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "user_id":
            if (
                wallet := WalletDatabase.query.filter(WalletDatabase.user_id == user_id)
                .order_by(desc(WalletDatabase.created_at))
                .first()
            ):
                return wallet
            raise UserNotFoundError

    async def update(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        amount = kwargs.get("amount")
        if category == "amount":
            if (
                wallet := WalletDatabase.query.filter(WalletDatabase.user_id == user_id)
                .order_by(desc(WalletDatabase.created_at))
                .first()
            ):
                wallet.amount = amount
                db_session.commit()
                return
            raise UserNotFoundError

    async def delete(self):
        pass
