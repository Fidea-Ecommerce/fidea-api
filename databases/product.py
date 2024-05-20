from .config import db_session, init_db
from models import ProductDatabase, StoreDatabase, UserDatabase
from .database import Database
from sqlalchemy import and_, desc
from utils import (
    UserNotFoundError,
    ProductFoundError,
    UserNotIsActive,
    SellerNotIsActive,
)
import datetime


class ProductCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(
        self,
        user_id,
        description,
        title,
        price,
        tags,
        image_url,
        stock,
    ):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if (
            data := db_session.query(StoreDatabase, UserDatabase)
            .select_from(StoreDatabase)
            .join(UserDatabase)
            .filter(UserDatabase.id == user_id)
            .order_by(desc(StoreDatabase.created_at))
            .first()
        ):
            store, user = data
            if not store.is_active:
                raise SellerNotIsActive
            product = ProductDatabase(
                store.id,
                description,
                title,
                price,
                tags,
                image_url,
                stock,
                created_at,
                created_at,
            )
            db_session.add(product)
            db_session.commit()
            return
        raise UserNotFoundError

    async def delete(self, category, **kwargs):
        seller_id = kwargs.get("seller_id")
        id = kwargs.get("id")
        if category == "product":
            if product := (
                ProductDatabase.query.filter(
                    and_(
                        ProductDatabase.seller_id == seller_id,
                        ProductDatabase.id == id,
                    )
                )
                .order_by(desc(ProductDatabase.created_at))
                .first()
            ):
                db_session.delete(product)
                db_session.commit()
                return product
            else:
                raise ProductFoundError

    async def get(self, category, **kwargs):
        seller_id = kwargs.get("seller_id")
        seller = kwargs.get("seller")
        product_id = kwargs.get("product_id")
        title = kwargs.get("title")
        user_id = kwargs.get("user_id")
        if category == "product":
            if product := (
                db_session.query(ProductDatabase, StoreDatabase)
                .select_from(ProductDatabase)
                .join(StoreDatabase)
                .filter(
                    and_(
                        ProductDatabase.seller_id == seller_id,
                        StoreDatabase.seller == seller,
                    )
                )
                .order_by(desc(ProductDatabase.created_at))
                .all()
            ):
                return product
            else:
                raise ProductFoundError
        elif category == "product_id":
            if product := (
                db_session.query(ProductDatabase, StoreDatabase)
                .select_from(ProductDatabase)
                .join(StoreDatabase)
                .filter(
                    and_(
                        ProductDatabase.seller_id == seller_id,
                        StoreDatabase.seller == seller,
                        ProductDatabase.id == product_id,
                    )
                )
                .order_by(desc(ProductDatabase.created_at))
                .first()
            ):
                return product
            raise ProductFoundError
        elif category == "title":
            if product := (
                db_session.query(ProductDatabase, StoreDatabase)
                .select_from(ProductDatabase)
                .join(StoreDatabase)
                .filter(ProductDatabase.title.ilike(f"%{title}%"))
                .order_by(desc(ProductDatabase.created_at))
                .all()
            ):
                return product
            raise ProductFoundError
        elif category == "all":
            if product := (
                db_session.query(ProductDatabase, StoreDatabase)
                .select_from(ProductDatabase)
                .join(StoreDatabase)
                .order_by(desc(ProductDatabase.created_at))
                .all()
            ):
                return product
            raise ProductFoundError
        elif category == "title_product_seller":
            if product := (
                db_session.query(ProductDatabase, StoreDatabase)
                .select_from(ProductDatabase)
                .join(StoreDatabase)
                .filter(
                    and_(
                        ProductDatabase.title.ilike(f"%{title}%"),
                        ProductDatabase.seller_id == seller_id,
                        StoreDatabase.seller == seller,
                    )
                )
                .order_by(desc(ProductDatabase.created_at))
                .all()
            ):
                return product
            raise ProductFoundError

    async def update(self, category, **kwargs):
        seller_id = kwargs.get("seller_id")
        product_id = kwargs.get("product_id")
        amount = kwargs.get("amount")
        if category == "checkout":
            if product := (
                ProductDatabase.query.filter(
                    and_(
                        ProductDatabase.seller_id == seller_id,
                        ProductDatabase.id == product_id,
                    )
                )
                .order_by(desc(ProductDatabase.created_at))
                .all()
            ):
                for p in product:
                    p.stock = amount
                    p.sold += amount
                    p.updated_at = datetime.datetime.now(
                        datetime.timezone.utc
                    ).timestamp()
                db_session.commit()
            else:
                raise ProductFoundError
