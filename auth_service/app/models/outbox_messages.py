from datetime import datetime
from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseOrm
from app.models.mixins import CreateAtMixin, UpdateAtMixin, IntPkMixin


class OutboxMessagesOrm(BaseOrm, IntPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "outbox_messages"

    data: Mapped[str] = mapped_column(Text, nullable=False)
    routing_key: Mapped[str] = mapped_column(Text, nullable=False)
    broker_name: Mapped[str] = mapped_column(Text, nullable=False)

    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)