from .config import db_session, init_db
from models import UserDatabase
from sqlalchemy import and_, func, or_, desc
from .database import Database
from utils import UserNotFoundError, UserIsActive
import datetime
from sqlalchemy.orm import selectinload


class UserCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, **kwargs):
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        user = UserDatabase(username, email, password, created_at, created_at)
        db_session.add(user)
        db_session.commit()

    async def get(self, category, **kwargs):
        username = kwargs.get("username")
        email = kwargs.get("email")
        user_id = kwargs.get("user_id")
        password = kwargs.get("password")
        if category == "email":
            if (
                user := UserDatabase.query.filter(
                    func.lower(UserDatabase.email) == email.lower()
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                return user
            else:
                raise UserNotFoundError
        elif category == "username":
            if (
                user := UserDatabase.query.filter(
                    func.lower(UserDatabase.username) == username.lower()
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                return user
            else:
                raise UserNotFoundError
        elif category == "login":
            if (
                user := UserDatabase.query.filter(
                    func.lower(UserDatabase.email) == email.lower()
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                return user
            raise UserNotFoundError
        elif category == "register":
            return (
                UserDatabase.query.filter(
                    or_(
                        func.lower(UserDatabase.username) == username.lower(),
                        func.lower(UserDatabase.email) == email.lower(),
                    )
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            )
        elif category == "account_active":
            if (
                data := UserDatabase.query.filter(
                    and_(
                        func.lower(UserDatabase.email) == email.lower(),
                        UserDatabase.id == user_id,
                    )
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                return data
            else:
                raise UserNotFoundError

    async def update(self, category, **kwargs):
        username = kwargs.get("username")
        email = kwargs.get("email")
        balance = kwargs.get("balance")
        password = kwargs.get("password")
        new_password = kwargs.get("new_password")
        if category == "buy":
            if (
                user := UserDatabase.query.filter(
                    func.lower(UserDatabase.username) == username.lower()
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                user.balance -= balance
                db_session.commit()
                return user
            else:
                raise UserNotFoundError
        elif category == "is_active":
            if (
                user := UserDatabase.query.filter(
                    func.lower(UserDatabase.email) == email.lower()
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                if user.is_active:
                    raise UserIsActive
                user.is_active = True
                user.updated_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
            else:
                raise UserNotFoundError
        elif category == "password":
            if (
                user := UserDatabase.query.filter(
                    and_(
                        func.lower(UserDatabase.email) == email.lower(),
                        UserDatabase.password == password,
                    )
                )
                .order_by(desc(UserDatabase.created_at))
                .first()
            ):
                user.password = new_password
                user.update_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
            else:
                raise UserNotFoundError

    async def delete(self):
        pass
