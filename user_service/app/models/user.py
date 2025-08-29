from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseOrm
from app.models.mixins import CreateAtMixin, UpdateAtMixin, UuidPkMixin


class UserOrm(BaseOrm, UuidPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, fullname={self.fullname})>"
