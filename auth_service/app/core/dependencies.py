from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.core.db import session_maker
from app.repositories.auth_repository import AuthRepository
from app.repositories.outbox_messages_repository import OutboxMessagesRepository
from app.services.outbox_messages import OutboxMessagesService
from app.services.auth_service import AuthService
from app.services.brokers.broker_manager import get_broker_manager

@asynccontextmanager
async def get_auth_service() -> AsyncIterator[AuthService]:
    async with session_maker() as db:
        auth_repository = AuthRepository(db)
        broker_manager = get_broker_manager()
        yield AuthService(auth_repository, broker=broker_manager.get_broker())

@asynccontextmanager
async def get_outbox_messages_service() -> AsyncIterator[OutboxMessagesService]:
    async with session_maker() as db:
        outbox_repository = OutboxMessagesRepository(db)
        yield OutboxMessagesService(outbox_messages_repository=outbox_repository)

