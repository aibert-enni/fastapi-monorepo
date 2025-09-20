from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repository import UserRepository
from app.services.user_service import UserService


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
