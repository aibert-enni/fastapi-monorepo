from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.db import SessionDep
from app.exceptions.custom_exceptions import AuthorizationError, CredentialError
from app.repository import AuthRepository
from app.schemas.auth import AuthS
from app.services.auth_service import AuthService
from app.services.brokers.rabbit.main import rabbit_broker_service
from app.utils.jwt import TokenType, decode_jwt


def get_auth_repository(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(auth_repository=auth_repository, broker=rabbit_broker_service)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

# current user dependencies

http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
    credential: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> dict:
    """
    Retrieve the payload from the JWT token provided in the HTTP authorization credentials.
    """
    if credential is None:
        raise CredentialError
    try:
        token = credential.credentials
        payload = decode_jwt(token)
    except Exception:
        raise CredentialError
    return payload


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    payload: dict = Depends(get_current_token_payload),
) -> AuthS:
    """
    Retrieve the current user based on the provided HTTP authorization credentials.
    """
    user = await auth_service.get_auth_by_token(payload)

    if user is None:
        raise CredentialError

    if not user.is_active:
        raise CredentialError(message="Account not activated")

    return user


async def get_current_user_by_refresh(
    request: Request, auth_service: AuthService = Depends(get_auth_service)
) -> AuthS:
    """
    Retrieve the current user based on the refresh token stored in cookies.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise CredentialError
    try:
        payload = decode_jwt(refresh_token)
    except Exception:
        raise CredentialError

    user = await auth_service.get_auth_by_token(payload, token_type=TokenType.REFRESH)

    if user is None:
        raise CredentialError

    return user


async def get_current_superuser(
    current_user: AuthS = Depends(get_current_user),
) -> AuthS:
    """
    Ensure the current user is a superuser.
    """
    if not current_user:
        raise AuthorizationError
    return current_user


GetCurrentUserDep = Annotated[AuthS, Depends(get_current_user)]
GetCurrentUserByRefreshDep = Annotated[AuthS, Depends(get_current_user_by_refresh)]

GetCurrentSuperUserDep = Annotated[AuthS, Depends(get_current_superuser)]
