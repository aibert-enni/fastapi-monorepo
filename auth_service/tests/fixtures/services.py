import pytest_asyncio
from auth_service.app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import AuthRepository


@pytest_asyncio.fixture(scope="function")
async def auth_service(db_session: AsyncSession) -> AuthService:

    repo = AuthRepository(db_session)
    service = AuthService(repo)
    return service
