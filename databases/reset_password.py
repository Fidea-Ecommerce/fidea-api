from .config import db_session, init_db
from models import ResetPasswordDatabase
from .database import Database
from sqlalchemy import and_, desc
import datetime
from utils import UserNotFoundError


class ResetPasswordCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, token, created_at, expired_at):
        reset_password = ResetPasswordDatabase(user_id, token, created_at, expired_at)
        db_session.add(reset_password)
        db_session.commit()

    async def delete(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "user_id":
            user_token = (
                ResetPasswordDatabase.query.filter(
                    ResetPasswordDatabase.user_id == user_id
                )
                .order_by(desc(ResetPasswordDatabase.created_at))
                .first()
            )
            db_session.delete(user_token)
            db_session.commit()

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        token = kwargs.get("token")
        if category == "token":
            if data := (
                ResetPasswordDatabase.query.filter(
                    and_(
                        ResetPasswordDatabase.user_id == user_id,
                        ResetPasswordDatabase.token == token,
                        datetime.datetime.now(datetime.timezone.utc).timestamp()
                        < ResetPasswordDatabase.expired_at,
                    )
                )
                .order_by(desc(ResetPasswordDatabase.created_at))
                .first()
            ):
                return data
            raise UserNotFoundError

    async def update(self, category, **kwargs):
        pass
