from .config import db_session, init_db
from models import AccountActiveDatabase
from .database import Database
from sqlalchemy import and_, desc
from utils import UserNotFoundError
import datetime


class AccountActiveCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, token, created_at, expired_at):
        reset_password = AccountActiveDatabase(user_id, token, created_at, expired_at)
        db_session.add(reset_password)
        db_session.commit()

    async def delete(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "user_id":
            user_token = (
                AccountActiveDatabase.query.filter(
                    AccountActiveDatabase.user_id == user_id
                )
                .order_by(desc(AccountActiveDatabase.created_at))
                .first()
            )
            db_session.delete(user_token)
            db_session.commit()

    async def get(self, category, **kwargs):
        token = kwargs.get("token")
        user_id = kwargs.get("user_id")
        if category == "token":
            if (
                token := AccountActiveDatabase.query.filter(
                    and_(
                        AccountActiveDatabase.user_id == user_id,
                        AccountActiveDatabase.token == token,
                        datetime.datetime.now(datetime.timezone.utc).timestamp()
                        < AccountActiveDatabase.expired_at,
                    )
                )
                .order_by(desc(AccountActiveDatabase.created_at))
                .first()
            ):
                return token
            raise UserNotFoundError

    async def update(self, category, **kwargs):
        pass
