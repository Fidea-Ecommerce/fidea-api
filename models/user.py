from sqlalchemy import Table, Column, Integer, String, Boolean, Float, CheckConstraint
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class UserDatabase:
    query = db_session.query_property()

    def __init__(self, username, email, password, created_at, updated_at):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<User {self.username!r}>"


user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(collation="C"), unique=True, nullable=False),
    Column("email", String(collation="C"), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("is_active", Boolean, default=False),
    Column("banned_at", Float, default=None),
    Column("unbanned_at", Float, default=None),
    Column("is_admin", Boolean, default=False),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint(
        "(banned_at >= 0) OR (banned_at IS NULL)", name="positive_banned_at_or_null"
    ),
    CheckConstraint(
        "(unbanned_at >= 0) OR (unbanned_at IS NULL)",
        name="positive_un_banned_at_or_null",
    ),
)

mapper_registry.map_imperatively(UserDatabase, user_table)
