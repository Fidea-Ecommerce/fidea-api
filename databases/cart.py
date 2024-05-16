from .config import db_session, init_db
from models import (
    CartDatabase,
    ProductDatabase,
    StoreDatabase,
    UserDatabase,
)
from .database import Database
from sqlalchemy import func, and_, desc
from utils import ProductFoundError, StockNotAvaible, UserNotIsActive, UserNotFoundError
import datetime


class CartCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, user_id, amount, product_id, **kwargs):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if result := (
            db_session.query(CartDatabase, UserDatabase, ProductDatabase, StoreDatabase)
            .select_from(CartDatabase)
            .join(UserDatabase)
            .join(ProductDatabase)
            .join(StoreDatabase)
            .filter(
                and_(
                    CartDatabase.user_id == user_id,
                    CartDatabase.product_id == product_id,
                )
            )
            .order_by(desc(CartDatabase.created_at))
            .first()
        ):
            cart, user, product, store = result
            if not user.is_active:
                raise UserNotIsActive
            if product.stock < amount:
                raise StockNotAvaible
            cart.amount += amount
            if cart.amount > product.stock:
                raise StockNotAvaible
            cart.updated_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
            db_session.commit()
            return
        if (
            data_user := UserDatabase.query.filter(
                UserDatabase.id == user_id,
            )
            .order_by(desc(UserDatabase.created_at))
            .first()
        ):
            if (
                product_data := ProductDatabase.query.filter(
                    ProductDatabase.id == product_id,
                )
                .order_by(desc(ProductDatabase.created_at))
                .first()
            ):
                if not data_user.is_active:
                    raise UserNotIsActive
                if product_data.stock < amount:
                    raise StockNotAvaible
                product_result = CartDatabase(
                    user_id,
                    amount,
                    product_id,
                    created_at,
                    created_at,
                )
                db_session.add(product_result)
                db_session.commit()
                return
            raise ProductFoundError
        raise UserNotFoundError

    async def delete(self, user_id, cart_id):
        if result := (
            CartDatabase.query.filter(
                and_(
                    CartDatabase.user_id == user_id,
                    CartDatabase.id == cart_id,
                )
            )
            .order_by(desc(CartDatabase.created_at))
            .first()
        ):
            db_session.delete(result)
            db_session.commit()
            return
        raise ProductFoundError

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        cart_id = kwargs.get("cart_id")
        if category == "cart":
            if (
                cart_item := db_session.query(
                    CartDatabase, UserDatabase, ProductDatabase, StoreDatabase
                )
                .select_from(CartDatabase)
                .join(UserDatabase)
                .join(ProductDatabase)
                .join(StoreDatabase)
                .filter(CartDatabase.user_id == user_id)
                .order_by(desc(CartDatabase.created_at))
                .all()
            ):
                return cart_item
            else:
                raise ProductFoundError
        elif category == "cart_checkout":
            if (
                cart_item := db_session.query(
                    CartDatabase, UserDatabase, ProductDatabase, StoreDatabase
                )
                .select_from(CartDatabase)
                .join(UserDatabase)
                .join(ProductDatabase)
                .join(StoreDatabase)
                .filter(
                    and_(CartDatabase.user_id == user_id, CartDatabase.mark == True)
                )
                .order_by(desc(CartDatabase.created_at))
                .all()
            ):
                return cart_item
            else:
                raise ProductFoundError
        elif category == "cart_id":
            if (
                cart_item := db_session.query(
                    CartDatabase, UserDatabase, ProductDatabase, StoreDatabase
                )
                .select_from(CartDatabase)
                .join(UserDatabase)
                .join(ProductDatabase)
                .join(StoreDatabase)
                .filter(
                    and_(CartDatabase.user_id == user_id, CartDatabase.id == cart_id)
                )
                .order_by(desc(CartDatabase.created_at))
                .first()
            ):
                return cart_item
            else:
                raise ProductFoundError

    async def update(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        cart_id = kwargs.get("cart_id")
        amount = kwargs.get("amount")
        mark = kwargs.get("mark")
        if category == "amount":
            if (
                data := CartDatabase.query.filter(
                    and_(CartDatabase.user_id == user_id, CartDatabase.id == cart_id)
                )
                .order_by(desc(CartDatabase.created_at))
                .first()
            ):
                data.amount = amount
                data.updated_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
            else:
                raise ProductFoundError
        elif category == "tick":
            if (
                data := CartDatabase.query.filter(
                    and_(
                        CartDatabase.user_id == user_id,
                        CartDatabase.id == cart_id,
                    )
                )
                .order_by(desc(CartDatabase.created_at))
                .first()
            ):
                data.mark = not data.mark
                data.updated_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
            else:
                raise ProductFoundError
        elif category == "all_tick":
            if (
                data := CartDatabase.query.filter(CartDatabase.user_id == user_id)
                .order_by(desc(CartDatabase.created_at))
                .all()
            ):
                for i in data:
                    i.mark = mark
                    i.updated_at = datetime.datetime.now(
                        datetime.timezone.utc
                    ).timestamp()
                db_session.commit()
                return
            raise ProductFoundError
