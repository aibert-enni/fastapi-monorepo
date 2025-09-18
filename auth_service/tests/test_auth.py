import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import (
    IntegrityError,
    NotFoundError,
)
from app.schemas.auth import AuthCreateS, AuthLoginS
from app.services.auth_service import AuthService
from app.utils.jwt import decode_jwt
from app.utils.password import verify_password

from .factories import AuthFactory


@pytest.mark.asyncio
async def test_create_user(auth_service: AuthService) -> None:
    test_auth = AuthCreateS(
        username="test",
        email="test@gmail.com",
        is_active=True,
        is_superuser=False,
        password="1234qwer",
    )
    db_auth = await auth_service.create_auth(test_auth)

    assert db_auth.id is not None
    assert test_auth.username == db_auth.username
    assert test_auth.email == db_auth.email
    assert db_auth.is_active == test_auth.is_active
    assert db_auth.is_superuser == test_auth.is_superuser

    assert verify_password(test_auth.password, db_auth.hashed_password)

    with pytest.raises(IntegrityError):
        await auth_service.create_auth(test_auth)


@pytest.mark.asyncio
async def test_login_user(auth_service: AuthService, db_session: AsyncSession) -> None:
    test_auth = await AuthFactory.create(session=db_session)

    with pytest.raises(NotFoundError):
        await auth_service.login_user(
            AuthLoginS(username="dasdasd", password="21312dsadas")
        )

    tokens = await auth_service.login_user(
        AuthLoginS(username=test_auth.username, password="1234qwer")
    )

    assert tokens.access_token is not None
    assert tokens.refresh_token is not None

    payload = decode_jwt(tokens.access_token)

    user = await auth_service.get_auth_by_token(payload)

    assert user is not None
    assert user.username == test_auth.username
    assert user.email == test_auth.email
