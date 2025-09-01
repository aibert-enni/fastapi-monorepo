from uuid import uuid4

import pytest

from app.exceptions.custom_exceptions import IntegrityError
from app.schemas.auth import AuthCreateS
from app.services.auth_service import AuthService
from app.utils.password import verify_password


@pytest.mark.asyncio
async def test_create_user(auth_service: AuthService) -> None:
    test_auth = AuthCreateS(
        user_id=uuid4(), is_active=True, is_superuser=False, password="1234qwer"
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
