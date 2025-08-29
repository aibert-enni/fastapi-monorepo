from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repository import AuthRepository
from app.services.auth_service import AuthService


def get_auth_repository(session: AsyncSession = Depends(get_session)) -> AuthRepository:
    return AuthRepository(session)


def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(auth_repository)
