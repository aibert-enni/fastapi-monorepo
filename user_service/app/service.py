from sqlalchemy.exc import IntegrityError as SAIntegrityError

from app.repository import UserRepository
from app.schemas.user import UserS, UserCreateS
from app.utils.user import hash_password
from app.exceptions.custom_exceptions import IntegrityError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, schema: UserCreateS) -> UserS:
        hashed_password = hash_password(schema.password)
        user_schema = UserS(
            **schema.model_dump(exclude={"password"}), hashed_password=hashed_password
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

        return UserS.model_validate(db_user)
