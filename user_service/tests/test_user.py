import pytest
from pydantic import ValidationError

from app.exceptions.custom_exceptions import IntegrityError
from app.schemas.user import UserCreateS
from app.service import UserService


@pytest.mark.asyncio
async def test_create_user(user_service: UserService) -> None:
    with pytest.raises(ValidationError):
        UserCreateS(
            username="test", fullname="test", password="test", email="test@mail"
        )

    test_user = UserCreateS(
        username="test", fullname="test", password="test", email="test@mail.ru"
    )
    db_user = await user_service.create_user(test_user)

    assert db_user.id is not None
    assert test_user.username == db_user.username
    assert test_user.password != db_user.hashed_password
    assert db_user.is_active is False

    with pytest.raises(IntegrityError):
        await user_service.create_user(test_user)
