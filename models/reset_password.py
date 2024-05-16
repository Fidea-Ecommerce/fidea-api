from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class ResetPasswordDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, token, created_at, expired_at):
        self.user_id = user_id
        self.token = token
        self.created_at = created_at
        self.expired_at = expired_at

    def __repr__(self):
        return f"<Reset Password {self.user_id!r}>"


reset_password_table = Table(
    "reset_password",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column("token", String, unique=True, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("expired_at", Float, nullable=False),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("expired_at >= 0", name="positive_expired_at"),
)

mapper_registry.map_imperatively(ResetPasswordDatabase, reset_password_table)
