import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.app.services.user_service import UserService

from app.repository import UserRepository


@pytest_asyncio.fixture(scope="function")
async def user_service(db_session: AsyncSession) -> UserService:

    repo = UserRepository(db_session)
    service = UserService(repo)
    return service
