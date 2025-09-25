from datetime import datetime
from sqlalchemy import select, update
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
    
    async def get_all(self) -> list[OutboxMessagesS]:
        stmt = select(OutboxMessagesOrm)
        result = await self.session.execute(stmt)
        db_outbox_messages = result.scalars().all()
        return [OutboxMessagesS.model_validate(db_outbox_message) for db_outbox_message in db_outbox_messages]
    
    async def get_all_by_is_not_sent(self) -> list[OutboxMessagesS]:
        stmt = select(OutboxMessagesOrm).where(OutboxMessagesOrm.sent_at == None)
        result = await self.session.execute(stmt)
        db_outbox_messages = result.scalars().all()
        return [OutboxMessagesS.model_validate(db_outbox_message) for db_outbox_message in db_outbox_messages]

    async def update_sent_at_by_id(self, id: int, sent_at: datetime) -> None:
        stmt = update(OutboxMessagesOrm).where(OutboxMessagesOrm.id == id).values(sent_at=sent_at)
        await self.session.execute(stmt)

    async def update_sent_at_by_ids(self, ids: list[int], sent_at: datetime) -> None:
        stmt = update(OutboxMessagesOrm).where(OutboxMessagesOrm.id.in_(ids)).values(sent_at=sent_at)
        await self.session.execute(stmt)