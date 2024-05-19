from .config import db_session, init_db
from models import FavoriteDatabase
from sqlalchemy import and_, desc
from .database import Database
import datetime
from utils import ProductFoundError


class FavoriteCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, seller_id, product_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        reset_password = FavoriteDatabase(
            user_id, seller_id, product_id, created_at, created_at
        )
        db_session.add(reset_password)
        db_session.commit()

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        seller_id = kwargs.get("seller_id")
        product_id = kwargs.get("product_id")
        if category == "is_favorite":
            if (
                data := FavoriteDatabase.query.filter(
                    and_(
                        FavoriteDatabase.user_id == user_id,
                        FavoriteDatabase.seller_id == seller_id,
                        FavoriteDatabase.product_id == product_id,
                    )
                )
                .order_by(desc(FavoriteDatabase.created_at))
                .first()
            ):
                return True
        return False

    async def update(self, category, **kwargs):
        pass

    async def delete(self, user_id, seller_id, product_id):
        if (
            data := FavoriteDatabase.query.filter(
                and_(
                    FavoriteDatabase.user_id == user_id,
                    FavoriteDatabase.seller_id == seller_id,
                    FavoriteDatabase.product_id == product_id,
                )
            )
            .order_by(desc(FavoriteDatabase.created_at))
            .first()
        ):
            db_session.delete(data)
            db_session.commit()
            return
        raise ProductFoundError
