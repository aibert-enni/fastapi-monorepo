from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.core.db import session_maker
from app.repository import AuthRepository
from app.services.auth_service import AuthService
from app.services.brokers.rabbit.main import rabbit_broker_service


@asynccontextmanager
async def get_auth_service() -> AsyncIterator[AuthService]:
    async with session_maker() as db:
        auth_repository = AuthRepository(db)
        yield AuthService(auth_repository, broker=rabbit_broker_service)