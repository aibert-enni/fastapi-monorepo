from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox_messages import OutboxMessagesOrm
from app.schemas.outbox_messages import OutboxMessagesCreateS, OutboxMessagesS


class OutboxMessagesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, outbox_message: OutboxMessagesCreateS) -> OutboxMessagesS:
        db_outbox_message = OutboxMessagesOrm(**outbox_message.model_dump())
        self.session.add(db_outbox_message)
        await self.session.flush()
        await self.session.refresh(db_outbox_message)
        return OutboxMessagesS.model_validate(db_outbox_message)