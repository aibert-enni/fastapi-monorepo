from datetime import datetime, timedelta, timezone
from enum import Enum

import jwt

from app.core.settings import settings

TOKEN_TYPE_FIELD = "type"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.jwt.ALGORITHM,
    expires_delta: timedelta | None = None,
    expire_minutes: int = settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.jwt.ALGORITHM,
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def create_jwt(
    token_type: TokenType,
    payload: dict,
    expires_delta: timedelta | None = None,
    expire_minutes: int = settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type.value,
    }

    jwt_payload.update(payload)

    return encode_jwt(
        payload=jwt_payload, expires_delta=expires_delta, expire_minutes=expire_minutes
    )


def create_access_token(payload: dict) -> str:
    return create_jwt(
        token_type=TokenType.ACCESS,
        payload=payload,
    )


def create_refresh_token(payload: dict) -> str:
    return create_jwt(
        token_type=TokenType.REFRESH,
        payload=payload,
        expires_delta=timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
    )
