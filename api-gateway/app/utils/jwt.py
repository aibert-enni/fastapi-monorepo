import jwt

from app.core.settings import settings


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.jwt.ALGORITHM,
) -> dict:
    payload: dict = jwt.decode(token, public_key, algorithms=[algorithm])
    payload_str = {k: str(v) for k, v in payload.items()}
    return payload_str