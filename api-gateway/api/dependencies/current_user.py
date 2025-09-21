from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.exceptions.custom_exceptions import AuthorizationError, CredentialError
from app.schemas.auth import AuthS
from app.utils.jwt import decode_jwt

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
    try:
        user = AuthS(id=payload.get("sub"), username=payload.get("username"), email=payload.get("email"), is_active=payload.get("is_active"), is_superuser=payload.get("is_superuser")) # type: ignore
    except Exception:
        raise CredentialError

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

GetHttpBearerDep = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]

GetCurrentUserDep = Annotated[AuthS, Depends(get_current_user)]

GetCurrentSuperUserDep = Annotated[AuthS, Depends(get_current_superuser)]