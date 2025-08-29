from uuid import UUID

from sqlalchemy import UUID as SaUUID, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseOrm
from app.models.mixins import CreateAtMixin, UpdateAtMixin, UuidPkMixin


class AuthOrm(BaseOrm, UuidPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "auth"

    user_id: Mapped[UUID] = mapped_column(
        SaUUID(as_uuid=True), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Auth(used_id={self.user_id}, is_active={self.is_active}, is_superuser={self.is_superuser})>"
