from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseOrm
from app.models.mixins import CreateAtMixin, UpdateAtMixin, UuidPkMixin


class UserOrm(BaseOrm, UuidPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)

    def __repr__(self):
        return f"<User(firstname={self.first_name}, lastname={self.last_name})>"
