from sqlalchemy.exc import IntegrityError as SAIntegrityError

from app.exceptions.custom_exceptions import (
    AuthorizationError,
    CredentialError,
    IntegrityError,
    NotFoundError,
)
from app.repository import AuthRepository
from app.schemas.auth import AuthCreateS, AuthLoginS, AuthS
from app.schemas.jwt_token import JWT_TokenS
from app.services.brokers.base import BaseBrokerService
from app.utils.jwt import (
    TOKEN_TYPE_FIELD,
    TokenType,
    create_access_token,
    create_refresh_token,
)
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(self, auth_repository: AuthRepository, broker: BaseBrokerService):
        self.auth_repository = auth_repository
        self.broker = broker

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
        await self.broker.publish_user_created(user.model_dump(mode="json"))
        return user

    async def authenticate_user(self, schema: AuthLoginS) -> AuthS:
        user = await self.auth_repository.get_by_username(schema.username)
        if user is None:
            raise NotFoundError(message="User not found")
        if not user.is_active:
            raise AuthorizationError(message="User is not active")
        if not verify_password(schema.password, user.hashed_password):
            raise AuthorizationError(message="Invalid password")
        return user

    async def login_user(self, schema: AuthLoginS) -> JWT_TokenS:
        user = await self.authenticate_user(schema)
        jwt_dict = {"sub": user.username}
        access_token = create_access_token(jwt_dict)
        refresh_token = create_refresh_token(jwt_dict)
        return JWT_TokenS(access_token=access_token, refresh_token=refresh_token)

    async def get_auth_by_token(
        self,
        payload: dict,
        token_type: TokenType = TokenType.ACCESS,
    ) -> AuthS:
        if payload.get(TOKEN_TYPE_FIELD) != token_type.value:
            raise CredentialError

        username = payload.get("sub")
        if username is None:
            raise CredentialError

        user = await self.auth_repository.get_by_username(username)

        return user
