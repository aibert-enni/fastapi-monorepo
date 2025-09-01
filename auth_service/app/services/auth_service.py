from sqlalchemy.exc import IntegrityError as SAIntegrityError

from app.exceptions.custom_exceptions import IntegrityError
from app.repository import AuthRepository
from app.schemas.auth import AuthCreateS, AuthS
from app.services.rabbit.publishers import publish_create_user
from app.utils.password import hash_password


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def create_auth(self, schema: AuthCreateS) -> AuthS:
        hashed_password = hash_password(schema.password)
        user_schema = AuthS(
            **schema.model_dump(exclude={"password"}), hashed_password=hashed_password
        )
        try:
            user = await self.auth_repository.save(user_schema)
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
        await publish_create_user(user)
        return user
