from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Boolean,
    ARRAY,
    CheckConstraint,
)
from sqlalchemy.orm import registry, relationship
from databases import metadata, db_session

mapper_registry = registry()


class ProductDatabase:
    query = db_session.query_property()

    def __init__(
        self,
        seller_id,
        description,
        title,
        price,
        tags,
        image_url,
        stock,
        created_at,
        updated_at,
    ):
        self.seller_id = seller_id
        self.description = description
        self.title = title
        self.price = price
        self.tags = tags
        self.image_url = image_url
        self.stock = stock
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Product {self.title!r}>"


product_table = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "seller_id",
        Integer,
        ForeignKey("store.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("description", String, nullable=False),
    Column("title", String, nullable=False, unique=True),
    Column("price", Float, nullable=False),
    Column("tags", ARRAY(String), nullable=False),
    Column("image_url", String, nullable=False),
    Column("stock", Integer, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("recomendation", Boolean, default=False),
    Column("sold", Integer, default=0),
    CheckConstraint("seller_id >= 0", name="positive_seller_id"),
    CheckConstraint("price >= 0", name="positive_price"),
    CheckConstraint("stock >= 0", name="positive_stock"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint("sold >= 0", name="positive_sold"),
)

mapper_registry.map_imperatively(ProductDatabase, product_table)
