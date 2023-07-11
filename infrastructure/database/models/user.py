""" User model file """
import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, TableNameMixin, TimestampMixin


class User(TableNameMixin, Base, TimestampMixin):
    """
    User model
    """

    user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(sa.String(length=60), nullable=True)
    username: Mapped[str] = mapped_column(sa.String(length=100), nullable=True)
    language: Mapped[str] = mapped_column(sa.String, nullable=False)

    def __repr__(self):
        return f'{self.user_id} | {self.name} | {self.username} | {self.language}'