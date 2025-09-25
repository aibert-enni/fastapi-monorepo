from sqlalchemy.exc import IntegrityError as SQLIntegrityError

from app.repositories.outbox_messages_repository import OutboxMessagesRepository
from app.schemas.outbox_messages import OutboxMessagesCreateS, OutboxMessagesS
from app.exceptions.custom_exceptions import IntegrityError

class OutboxMessagesService:
    def __init__(self, outbox_messages_repository: OutboxMessagesRepository) -> None:
        self.outbox_messages_repository = outbox_messages_repository

    async def create(self, create_schema: OutboxMessagesCreateS) -> OutboxMessagesS:
        outbox_message = await self.outbox_messages_repository.save(create_schema)
        await self.outbox_messages_repository.session.commit()
        return outbox_message