from sqlalchemy.exc import IntegrityError as SAIntegrityError

from app.exceptions.custom_exceptions import IntegrityError, NotFoundError
from app.repository import UserRepository
from app.schemas.user import UserCreateS, UserS, UserUpdateS


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, schema: UserCreateS) -> UserS:
        user_schema = UserS(**schema.model_dump())
        try:
            user = await self.user_repository.save(user_schema)
        except SAIntegrityError as e:
            detail = str(e.orig)
            if "id" in detail:
                raise IntegrityError(
                    "User with this id already exist",
                )
            else:
                raise IntegrityError("Unique constraint violation")

        return user

    async def update_user(self, schema: UserUpdateS) -> UserS:
        user_schema = UserS(**schema.model_dump())
        user = await self.user_repository.update(user_schema)
        if not user:
            raise NotFoundError("User not found")
        return user
