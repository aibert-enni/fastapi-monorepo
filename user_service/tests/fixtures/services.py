import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import UserRepository
from app.service import UserService


@pytest_asyncio.fixture(scope="function")
async def user_service(db_session: AsyncSession) -> UserService:

    repo = UserRepository(db_session)
    service = UserService(repo)
    return service
