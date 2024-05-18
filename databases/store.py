from .config import db_session, init_db
from models import StoreDatabase, UserDatabase
from sqlalchemy import and_, func, or_, desc
from .database import Database
import datetime
from utils import UserNotIsActive, UserNotFoundError


class StoreCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, seller):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if (
            user := UserDatabase.query.filter(UserDatabase.id == user_id)
            .order_by(desc(UserDatabase.created_at))
            .first()
        ):
            store = StoreDatabase(user.id, seller, created_at, created_at)
            db_session.add(store)
            db_session.commit()
            return
        raise UserNotFoundError

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "is_seller":
            return (
                StoreDatabase.query.filter(StoreDatabase.user_id == user_id)
                .order_by(desc(StoreDatabase.created_at))
                .first()
            )

    async def update(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        amount = kwargs.get("amount")
        if category == "balance_checkout":
            if user := (
                StoreDatabase.query.filter(StoreDatabase.id == user_id)
                .order_by(desc(StoreDatabase.created_at))
                .first()
            ):
                user.amount += amount
                db_session.commit()

    async def delete(self):
        pass
