from unittest.mock import AsyncMock

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import AuthRepository
from app.services.auth_service import AuthService


@pytest_asyncio.fixture(scope="function")
async def auth_service(db_session: AsyncSession) -> AuthService:
    repo = AuthRepository(db_session)
    broker = AsyncMock()
    service = AuthService(auth_repository=repo, broker=broker)
    return service
