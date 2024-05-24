from .config import db_session, init_db
from models import FavoriteDatabase, ProductDatabase, StoreDatabase
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
        if (
            data := ProductDatabase.query.filter(
                and_(
                    ProductDatabase.id == product_id,
                    ProductDatabase.seller_id == seller_id,
                )
            )
            .order_by(desc(ProductDatabase.created_at))
            .first()
        ):
            favorite_item = FavoriteDatabase(
                user_id, seller_id, product_id, created_at, created_at
            )
            db_session.add(favorite_item)
            db_session.commit()
            return
        raise ProductFoundError

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        seller_id = kwargs.get("seller_id")
        product_id = kwargs.get("product_id")
        favorite_id = kwargs.get("favorite_id")
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
        elif category == "all":
            if (
                data := db_session.query(
                    FavoriteDatabase, ProductDatabase, StoreDatabase
                )
                .select_from(FavoriteDatabase)
                .join(ProductDatabase)
                .join(StoreDatabase)
                .filter(FavoriteDatabase.user_id == user_id)
                .order_by(desc(FavoriteDatabase.created_at))
                .all()
            ):
                return data
            raise ProductFoundError
        elif category == "favorite_id":
            if (
                data := db_session.query(
                    FavoriteDatabase, ProductDatabase, StoreDatabase
                )
                .select_from(FavoriteDatabase)
                .join(ProductDatabase)
                .join(StoreDatabase)
                .filter(
                    and_(
                        FavoriteDatabase.user_id == user_id,
                        FavoriteDatabase.id == favorite_id,
                    )
                )
                .order_by(desc(FavoriteDatabase.created_at))
                .first()
            ):
                return data
            raise ProductFoundError

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
