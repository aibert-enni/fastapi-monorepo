import jwt

from app.core.settings import settings

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.jwt.ALGORITHM,
) -> dict:
    decoded: dict = jwt.decode(token, public_key, algorithms=[algorithm])
    if decoded.get("exp"):
        decoded.update({"exp": str(decoded.get("exp"))})
    return decoded