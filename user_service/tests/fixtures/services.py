import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import UserRepository
from app.services.user_service import UserService


@pytest_asyncio.fixture(scope="function")
async def user_service(db_session: AsyncSession) -> UserService:
    repo = UserRepository(db_session)
    service = UserService(user_repository=repo)
    return service
