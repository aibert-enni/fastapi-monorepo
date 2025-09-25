from typing import Annotated

from fastapi import Depends

from app.core.db import SessionDep
from auth_service.app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.services.brokers.broker_manager import get_broker_manager


def get_auth_repository(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    broker_manager = get_broker_manager()
    return AuthService(auth_repository=auth_repository, broker=broker_manager.get_broker())


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]