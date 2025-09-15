from typing import Annotated

from fastapi import Depends

from app.core.db import SessionDep
from app.repository import AuthRepository
from app.services.auth_service import AuthService
from app.services.brokers.rabbit.main import rabbit_broker_service


def get_auth_repository(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(auth_repository=auth_repository, broker=rabbit_broker_service)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]