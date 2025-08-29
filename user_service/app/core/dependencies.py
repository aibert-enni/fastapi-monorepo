from typing import Annotated

from fastapi import Depends

from app.core.db import SessionDep
from app.repository import UserRepository
from app.services.user_service import UserService


def get_user_repository(db: SessionDep) -> UserRepository:
    return UserRepository(db)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
