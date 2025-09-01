from uuid import uuid4

import pytest
from user_service.app.services.user_service import UserService

from app.exceptions.custom_exceptions import IntegrityError
from app.schemas.user import UserCreateS


@pytest.mark.asyncio
async def test_create_user(user_service: UserService) -> None:
    test_user = UserCreateS(id=uuid4(), first_name="cho-to", last_name="cho-to")
    db_user = await user_service.create_user(test_user)

    assert db_user.id is not None
    assert test_user.first_name == db_user.first_name
    assert test_user.last_name == db_user.last_name

    with pytest.raises(IntegrityError):
        await user_service.create_user(test_user)
