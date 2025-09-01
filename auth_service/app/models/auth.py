
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseOrm
from app.models.mixins import CreateAtMixin, UpdateAtMixin, UuidPkMixin


class AuthOrm(BaseOrm, UuidPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "auth"

    username: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Auth(username={self.username}, email={self.email}, is_active={self.is_active}, is_superuser={self.is_superuser})>"
