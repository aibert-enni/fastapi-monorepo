from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.core.db import session_maker
from app.services.user_service import UserService
from app.repository import UserRepository

@asynccontextmanager
async def get_user_service() -> AsyncIterator[UserService]:
    async with session_maker() as db:
        repo = UserRepository(db)
        yield UserService(repo)