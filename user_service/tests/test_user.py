import pytest
from pydantic import ValidationError
from user_service.app.services.user_service import UserService

from app.exceptions.custom_exceptions import IntegrityError
from app.schemas.user import UserBaseS


@pytest.mark.asyncio
async def test_create_user(user_service: UserService) -> None:
    with pytest.raises(ValidationError):
        UserBaseS(username="test", fullname="test", email="test@mail")

    test_user = UserBaseS(username="test", fullname="test", email="test@mail.ru")
    db_user = await user_service.create_user(test_user)

    assert db_user.id is not None
    assert test_user.username == db_user.username

    with pytest.raises(IntegrityError):
        await user_service.create_user(test_user)
