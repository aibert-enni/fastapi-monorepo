from typing import Annotated

from fastapi import Depends

from app.core.db import SessionDep
from app.repository import AuthRepository
from app.services.auth_service import AuthService


def get_auth_repository(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    user_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(user_repository)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
