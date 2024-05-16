from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    ForeignKey,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class CartDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, amount, product_id, created_at, updated_at):
        self.user_id = user_id
        self.amount = amount
        self.product_id = product_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Cart {self.user_id!r}>"


cart_table = Table(
    "cart",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("amount", Integer, nullable=False),
    Column("mark", Boolean, default=True),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("product_id >= 0", name="positive_product_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint("amount >= 0", name="positive_amount"),
)


mapper_registry.map_imperatively(CartDatabase, cart_table)
