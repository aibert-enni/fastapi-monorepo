from sqlalchemy.exc import IntegrityError as SAIntegrityError

from app.exceptions.custom_exceptions import IntegrityError
from app.repository import UserRepository
from app.schemas.user import UserBaseS, UserCreateS, UserS
from app.services.rabbit.publishers import publish_user_created


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, schema: UserCreateS) -> UserS:
        user_schema = UserBaseS(
            username=schema.username, fullname=schema.fullname, email=schema.email
        )
        try:
            db_user = await self.user_repository.save(user_schema)
        except SAIntegrityError as e:
            detail = str(e.orig)
            if "username" in detail:
                raise IntegrityError(
                    "User with this username already exist",
                )
            elif "email" in detail:
                raise IntegrityError(
                    "User with this email already exist",
                )
            else:
                raise IntegrityError("Unique constraint violation")

        user = UserS(**schema.model_dump(), id=db_user.id)

        await publish_user_created(user)

        return user
