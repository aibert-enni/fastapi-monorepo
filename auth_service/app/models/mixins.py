from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UuidPkMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class IntPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class CreateAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )


class UpdateAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=datetime.now(timezone.utc),
        server_onupdate=func.now(),
    )
