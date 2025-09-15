from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import grpc

from app.core.settings import settings
from app.exceptions.custom_exceptions import AuthorizationError, CredentialError
from app.utils.jwt import decode_jwt
from app.schemas.auth import AuthS
from proto.auth import auth_pb2_grpc, auth_pb2

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
    payload: dict = Depends(get_current_token_payload),
) -> AuthS:
    """
    Retrieve the current user based on the provided HTTP authorization credentials.
    """
    async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        request = auth_pb2.CurrentUserRequest(payload=payload)
        response = await stub.CurrentUser(request)

    user = response.user

    user = AuthS(id=user.id, username=user.username, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser)

    if user is None:
        raise CredentialError

    if not user.is_active:
        raise CredentialError(message="Account not activated")

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

GetCurrentSuperUserDep = Annotated[AuthS, Depends(get_current_superuser)]